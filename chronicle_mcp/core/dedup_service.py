"""Deduplication service for browser history.

Provides duplicate detection and deletion functionality.
"""

from difflib import SequenceMatcher
from typing import Any

from chronicle_mcp.core._connection import with_connection
from chronicle_mcp.core.validation import (
    validate_browser,
    validate_fuzzy_threshold,
    validate_limit,
)
from chronicle_mcp.database import detect_schema


class DedupService:
    """Service for finding and removing duplicate history entries."""

    @classmethod
    def find_duplicate_entries(
        cls,
        browser: str,
        similarity_threshold: float = 0.9,
        limit: int = 100,
    ) -> dict[str, Any]:
        """Find potential duplicate history entries.

        Args:
            browser: Browser to analyze
            similarity_threshold: URL similarity threshold (0.0-1.0)
            limit: Maximum number of duplicate groups to return

        Returns:
            Dictionary with duplicate groups and statistics
        """
        browser_lower = validate_browser(browser)
        validate_limit(limit, 1, 1000)
        validate_fuzzy_threshold(similarity_threshold)

        def normalize_url_for_comparison(url: str) -> str:
            """Normalize URL for comparison (strip http/https, www, trailing slashes)."""
            url_clean = url.strip().lower()
            if url_clean.startswith("http://"):
                url_clean = url_clean[7:]
            elif url_clean.startswith("https://"):
                url_clean = url_clean[8:]
            if url_clean.startswith("www."):
                url_clean = url_clean[4:]
            url_clean = url_clean.rstrip("/")
            return url_clean

        def url_similarity(url1: str, url2: str) -> float:
            """Calculate similarity between two URLs."""
            url1_clean = normalize_url_for_comparison(url1)
            url2_clean = normalize_url_for_comparison(url2)
            if url1_clean == url2_clean:
                return 1.0
            return SequenceMatcher(None, url1_clean, url2_clean).ratio()

        duplicates: list[dict[str, Any]] = []
        seen_urls: list[tuple[str, str, int]] = []

        def get_entries(conn: Any) -> list[Any]:
            """Get history entries for comparison."""
            cursor = conn.cursor()
            schema = detect_schema(conn)
            if schema == "chrome":
                cursor.execute(
                    "SELECT title, url, visit_count FROM urls WHERE visit_count > 0 ORDER BY visit_count DESC LIMIT 500"
                )
            elif schema == "firefox":
                cursor.execute(
                    "SELECT COALESCE(title, ''), url, visit_count FROM moz_places WHERE visit_count > 0 ORDER BY visit_count DESC LIMIT 500"
                )
            elif schema == "safari":
                cursor.execute(
                    "SELECT title, url, visit_count FROM history_items WHERE visit_count > 0 ORDER BY visit_count DESC LIMIT 500"
                )
            return cursor.fetchall()  # type: ignore[no-any-return]

        entries: list[tuple[str, str, int]] = with_connection(browser_lower, get_entries)

        for url, title, visit_count in entries:
            if not url:
                continue
            url_duplicates: list[dict[str, Any]] = []
            for existing_url, existing_title, existing_count in seen_urls:
                sim = url_similarity(url, existing_url)
                if sim >= similarity_threshold:
                    url_duplicates.append(
                        {
                            "url": existing_url,
                            "title": existing_title,
                            "visit_count": existing_count,
                            "similarity": round(sim, 3),
                        }
                    )
            if url_duplicates:
                duplicates.append(
                    {
                        "url": url,
                        "title": title,
                        "visit_count": visit_count,
                        "similar_to": url_duplicates[:5],
                    }
                )
            seen_urls.append((url, title, visit_count))
            if len(duplicates) >= limit:
                break

        return {
            "browser": browser_lower,
            "similarity_threshold": similarity_threshold,
            "duplicate_groups": duplicates,
            "total_duplicates": len(duplicates),
            "total_entries_analyzed": len(entries),
        }

    @classmethod
    def delete_duplicates(
        cls,
        browser: str,
        similarity_threshold: float = 0.9,
        keep_strategy: str = "most_visits",
        confirm: bool = False,
        _preview_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Delete duplicate history entries.

        Args:
            browser: Browser to clean
            similarity_threshold: URL similarity threshold for duplicates
            keep_strategy: Which entry to keep ('most_visits', 'most_recent', 'first')
            confirm: Must be True to actually delete; False returns preview
            _preview_result: Internal use - preview result from first call to avoid double computation

        Returns:
            Dictionary with deletion results or preview
        """
        browser_lower = validate_browser(browser)
        valid_strategies = ["most_visits", "most_recent", "first"]
        if keep_strategy not in valid_strategies:
            raise ValueError(f"Invalid keep_strategy. Must be one of: {valid_strategies}")

        if not confirm:
            preview_result = cls.find_duplicate_entries(
                browser=browser_lower,
                similarity_threshold=similarity_threshold,
                limit=100,
            )
            return {
                "preview": True,
                "message": f"Found {preview_result['total_duplicates']} duplicate groups",
                "duplicate_groups": preview_result["duplicate_groups"][:10],
                "total_duplicates": preview_result["total_duplicates"],
            }

        if _preview_result is None:
            preview_result = cls.find_duplicate_entries(
                browser=browser_lower,
                similarity_threshold=similarity_threshold,
                limit=100,
            )
        else:
            preview_result = _preview_result

        to_delete: list[tuple[str, str]] = []
        for group in preview_result["duplicate_groups"]:
            original_url = group["url"]
            for similar in group.get("similar_to", []):
                to_delete.append((similar["url"], original_url))

        if not to_delete:
            return {
                "preview": False,
                "deleted_count": 0,
                "total_pairs_checked": 0,
                "message": "No duplicate entries to delete",
            }

        def batch_delete(conn: Any) -> int:
            """Batch delete duplicate URLs using SQL IN clause with chunking."""
            cursor = conn.cursor()
            urls_to_delete = [url for url, _ in to_delete]
            if not urls_to_delete:
                return 0

            BATCH_SIZE = 500
            total_deleted = 0
            for i in range(0, len(urls_to_delete), BATCH_SIZE):
                batch = urls_to_delete[i : i + BATCH_SIZE]
                placeholders = ",".join("?" * len(batch))
                cursor.execute(f"DELETE FROM urls WHERE url IN ({placeholders})", batch)
                total_deleted += cursor.rowcount

            conn.commit()
            return total_deleted

        deleted_count = with_connection(browser_lower, batch_delete)

        return {
            "preview": False,
            "deleted_count": deleted_count,
            "total_pairs_checked": len(to_delete),
            "message": f"Deleted {deleted_count} duplicate entries",
        }
