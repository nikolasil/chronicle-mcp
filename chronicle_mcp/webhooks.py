import asyncio
import logging
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import httpx

logger = logging.getLogger(__name__)


@dataclass
class Webhook:
    id: str
    url: str
    events: list[str]
    created_at: datetime
    enabled: bool = True
    secret: str | None = None
    failure_count: int = 0
    last_triggered: datetime | None = None


@dataclass
class WebhookEvent:
    id: str
    event_type: str
    payload: dict[str, Any]
    timestamp: datetime
    webhook_id: str


class WebhookManager:
    def __init__(self) -> None:
        self.webhooks: dict[str, Webhook] = {}
        self.event_queue: asyncio.Queue[WebhookEvent] = asyncio.Queue()
        self._running = False
        self._worker_task: asyncio.Task | None = None

    def register_webhook(
        self,
        url: str,
        events: list[str],
        secret: str | None = None,
    ) -> Webhook:
        webhook = Webhook(
            id=str(uuid.uuid4()),
            url=url,
            events=events,
            created_at=datetime.now(timezone.utc),
            secret=secret,
        )
        self.webhooks[webhook.id] = webhook
        logger.info(f"Registered webhook: {webhook.id} for events: {events}")
        return webhook

    def unregister_webhook(self, webhook_id: str) -> bool:
        if webhook_id in self.webhooks:
            del self.webhooks[webhook_id]
            logger.info(f"Unregistered webhook: {webhook_id}")
            return True
        return False

    def get_webhook(self, webhook_id: str) -> Webhook | None:
        return self.webhooks.get(webhook_id)

    def list_webhooks(self) -> list[Webhook]:
        return list(self.webhooks.values())

    def trigger_event(self, event_type: str, payload: dict[str, Any]) -> None:
        for webhook in self.webhooks.values():
            if webhook.enabled and event_type in webhook.events:
                event = WebhookEvent(
                    id=str(uuid.uuid4()),
                    event_type=event_type,
                    payload=payload,
                    timestamp=datetime.now(timezone.utc),
                    webhook_id=webhook.id,
                )
                self.event_queue.put_nowait(event)

    async def _send_webhook(self, webhook: Webhook, event: WebhookEvent) -> bool:
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Event": event.event_type,
            "X-Webhook-ID": webhook.id,
            "X-Event-ID": event.id,
        }

        if webhook.secret:
            import base64
            import hashlib
            import hmac

            payload_sig = f"{event.id}.{event.timestamp.isoformat()}.{event.payload}"
            signature = hmac.new(
                webhook.secret.encode(),
                payload_sig.encode(),
                hashlib.sha256,
            ).digest()
            headers["X-Signature"] = base64.b64encode(signature).decode()

        payload = {
            "event": event.event_type,
            "event_id": event.id,
            "timestamp": event.timestamp.isoformat(),
            "data": event.payload,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(webhook.url, json=payload, headers=headers)
                if response.status_code < 400:
                    webhook.failure_count = 0
                    webhook.last_triggered = datetime.now(timezone.utc)
                    logger.debug(f"Webhook {webhook.id} sent successfully")
                    return True
                else:
                    webhook.failure_count += 1
                    logger.warning(
                        f"Webhook {webhook.id} failed with status: {response.status_code}"
                    )
                    return False
        except Exception as e:
            webhook.failure_count += 1
            logger.error(f"Webhook {webhook.id} error: {e}")
            return False

    async def _worker(self) -> None:
        while self._running:
            try:
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                webhook = self.webhooks.get(event.webhook_id)
                if webhook and webhook.enabled:
                    await self._send_webhook(webhook, event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Webhook worker error: {e}")

    def start(self) -> None:
        if not self._running:
            self._running = True
            self._worker_task = asyncio.create_task(self._worker())
            logger.info("Webhook manager started")

    async def stop(self) -> None:
        if self._running:
            self._running = False
            if self._worker_task:
                self._worker_task.cancel()
                try:
                    await self._worker_task
                except asyncio.CancelledError:
                    pass
            logger.info("Webhook manager stopped")


webhook_manager = WebhookManager()


def notify_new_history(browser: str, entry: dict[str, Any]) -> None:
    """Send webhook notification for new history entry."""
    webhook_manager.trigger_event(
        "history.new",
        {
            "browser": browser,
            "entry": entry,
        },
    )


def notify_history_deleted(browser: str, query: str, count: int) -> None:
    """Send webhook notification for deleted history entries."""
    webhook_manager.trigger_event(
        "history.deleted",
        {
            "browser": browser,
            "query": query,
            "count": count,
        },
    )
