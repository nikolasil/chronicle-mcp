import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from importlib.metadata import version as get_package_version
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def get_version() -> str:
    """Get the current version of ChronicleMCP."""
    try:
        return get_package_version("chronicle-mcp")
    except Exception:
        pyproject = Path(__file__).parent.parent.parent / "pyproject.toml"
        if pyproject.exists():
            content = pyproject.read_text()
            for line in content.split("\n"):
                if line.startswith("version"):
                    return line.split("=")[1].strip().strip('"').strip("'")
        return "1.0.0"


@dataclass
class LoggingConfig:
    """Logging configuration."""

    level: str = "INFO"
    format: str = "default"
    json_format: bool = False
    file_path: str | None = None


@dataclass
class CacheConfig:
    """Cache configuration."""

    enabled: bool = True
    ttl_seconds: int = 300
    max_entries: int = 1000


@dataclass
class SecurityConfig:
    """Security configuration."""

    sanitize_urls: bool = True
    sensitive_params: list[str] = field(
        default_factory=lambda: [
            "token",
            "session",
            "key",
            "password",
            "auth",
            "sid",
            "access_token",
            "api_key",
            "apikey",
            "api-secret",
            "secret",
            "api_token",
            "apitoken",
            "bearer",
            "jwt",
            "csrf",
            "xsrf",
            "nonce",
            "salt",
            "hash",
        ]
    )


@dataclass
class AdvancedConfig:
    """Advanced configuration options."""

    use_regex: bool = False
    fuzzy_threshold: float = 0.6
    parallel_queries: bool = True
    max_query_limit: int = 1000


@dataclass
class Config:
    """Configuration settings for ChronicleMCP."""

    default_browser: str = "chrome"
    default_limit: int = 5
    default_format: str = "markdown"
    log_level: str = "INFO"
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    advanced: AdvancedConfig = field(default_factory=AdvancedConfig)


def load_config(config_path: str | None = None) -> Config:
    """
    Load configuration from a TOML file.

    Args:
        config_path: Path to configuration file. If None, checks default locations.

    Returns:
        Config object with settings.
    """
    config = Config()

    if config_path is None:
        config_path = os.environ.get("CHRONICLE_CONFIG")

    if config_path is None:
        home_config = os.path.expanduser("~/.config/chronicle-mcp/config.toml")
        if os.path.exists(home_config):
            config_path = home_config

    if config_path is None:
        local_config = "chronicle.toml"
        if os.path.exists(local_config):
            config_path = local_config

    if config_path is None:
        logger.debug("No config file found, using defaults")
        return config

    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib  # type: ignore[no-redef]
        except ImportError:
            logger.warning("tomli/tomllib not available, skipping config file")
            return config

    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)

        if "default" in data:
            default_section = data["default"]
            if "browser" in default_section:
                config.default_browser = default_section["browser"]
            if "limit" in default_section:
                config.default_limit = default_section["limit"]
            if "format" in default_section:
                config.default_format = default_section["format"]
            if "log_level" in default_section:
                config.log_level = default_section["log_level"]

        if "logging" in data:
            logging_section = data["logging"]
            if "level" in logging_section:
                config.logging.level = logging_section["level"]
            if "format" in logging_section:
                config.logging.format = logging_section["format"]
            if "json_format" in logging_section:
                config.logging.json_format = logging_section["json_format"]
            if "file_path" in logging_section:
                config.logging.file_path = logging_section["file_path"]

        if "cache" in data:
            cache_section = data["cache"]
            if "enabled" in cache_section:
                config.cache.enabled = cache_section["enabled"]
            if "ttl_seconds" in cache_section:
                config.cache.ttl_seconds = cache_section["ttl_seconds"]
            if "max_entries" in cache_section:
                config.cache.max_entries = cache_section["max_entries"]

        if "security" in data:
            security_section = data["security"]
            if "sanitize_urls" in security_section:
                config.security.sanitize_urls = security_section["sanitize_urls"]
            if "sensitive_params" in security_section:
                config.security.sensitive_params = security_section["sensitive_params"]

        if "advanced" in data:
            advanced_section = data["advanced"]
            if "use_regex" in advanced_section:
                config.advanced.use_regex = advanced_section["use_regex"]
            if "fuzzy_threshold" in advanced_section:
                config.advanced.fuzzy_threshold = advanced_section["fuzzy_threshold"]
            if "parallel_queries" in advanced_section:
                config.advanced.parallel_queries = advanced_section["parallel_queries"]
            if "max_query_limit" in advanced_section:
                config.advanced.max_query_limit = advanced_section["max_query_limit"]

        logger.info(f"Loaded configuration from {config_path}")
    except Exception as e:
        logger.warning(f"Failed to load config from {config_path}: {e}")

    return config


def get_env_override(key: str, default: Any = None, type_: type = str) -> Any:
    """
    Get environment variable override.

    Args:
        key: Environment variable name (will be uppercased and prefixed with CHRONICLE_)
        default: Default value if not found
        type_: Type to convert to

    Returns:
        Value from environment or default
    """
    env_key = f"CHRONICLE_{key.upper()}"
    value = os.environ.get(env_key)
    if value is None:
        return default
    try:
        return type_(value)
    except (ValueError, TypeError):
        logger.warning(f"Failed to convert {env_key}='{value}' to {type_.__name__}")
        return default


def apply_env_overrides(config: Config) -> Config:
    """
    Apply environment variable overrides to configuration.

    Args:
        config: Config object to modify

    Returns:
        Modified Config object
    """
    browser = get_env_override("browser", config.default_browser)
    if browser:
        config.default_browser = browser

    limit = get_env_override("limit", config.default_limit, int)
    if limit:
        config.default_limit = limit

    format_ = get_env_override("format", config.default_format)
    if format_:
        config.default_format = format_

    log_level = get_env_override("log_level", config.log_level)
    if log_level:
        config.log_level = log_level

    cache_ttl = get_env_override("cache_ttl", config.cache.ttl_seconds, int)
    if cache_ttl:
        config.cache.ttl_seconds = cache_ttl

    return config


class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra_data"):
            log_entry.update(record.extra_data)

        return json.dumps(log_entry)


def setup_logging(level: str | None = None) -> None:
    """
    Set up logging for ChronicleMCP.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL). If None, reads from config.
    """
    config = load_config()
    config = apply_env_overrides(config)

    if level is None:
        level = config.log_level

    log_level = getattr(logging, level.upper(), logging.INFO)

    if config.logging.json_format:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logging.basicConfig(level=log_level, handlers=[handler])
    else:
        logging.basicConfig(
            level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    if config.logging.file_path:
        file_handler = logging.FileHandler(config.logging.file_path)
        if config.logging.json_format:
            file_handler.setFormatter(JSONFormatter())
        logging.getLogger().addHandler(file_handler)

    logger.debug("Logging initialized")
