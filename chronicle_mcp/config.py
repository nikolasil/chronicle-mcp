import logging
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Configuration settings for ChronicleMCP."""

    default_browser: str = "chrome"
    default_limit: int = 5
    default_format: str = "markdown"
    log_level: str = "INFO"


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
            import tomli as tomllib
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

        logger.info(f"Loaded configuration from {config_path}")
    except Exception as e:
        logger.warning(f"Failed to load config from {config_path}: {e}")

    return config


def setup_logging(level: str | None = None) -> None:
    """
    Set up logging for ChronicleMCP.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL). If None, reads from config.
    """
    config = load_config()

    if level is None:
        level = config.log_level

    log_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger.debug("Logging initialized")
