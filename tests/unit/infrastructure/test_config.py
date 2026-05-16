"""Tests for configuration module.

This module tests configuration loading, environment overrides,
and logging setup.
"""

import json
import logging

import pytest

from chronicle_mcp.config import (
    AdvancedConfig,
    CacheConfig,
    Config,
    JSONFormatter,
    LoggingConfig,
    SecurityConfig,
    apply_env_overrides,
    get_env_override,
    get_version,
    load_config,
    setup_logging,
)


class TestGetVersion:
    """Tests for get_version function."""

    def test_get_version_from_package(self):
        """Test getting version from installed package."""
        version = get_version()
        assert isinstance(version, str)
        assert len(version) > 0

    def test_get_version_fallback(self, monkeypatch):
        """Test version fallback when package not installed."""
        import importlib.metadata

        def mock_get_version(name):
            raise importlib.metadata.PackageNotFoundError()

        monkeypatch.setattr(importlib.metadata, "version", mock_get_version)

        # Create a temporary pyproject.toml
        version = get_version()
        # Should return default version
        assert isinstance(version, str)


class TestLoggingConfig:
    """Tests for LoggingConfig dataclass."""

    def test_default_values(self):
        """Test default logging configuration."""
        config = LoggingConfig()
        assert config.level == "INFO"
        assert config.format == "default"
        assert config.json_format is False
        assert config.file_path is None

    def test_custom_values(self):
        """Test custom logging configuration."""
        config = LoggingConfig(
            level="DEBUG",
            format="detailed",
            json_format=True,
            file_path="/var/log/app.log",
        )
        assert config.level == "DEBUG"
        assert config.format == "detailed"
        assert config.json_format is True
        assert config.file_path == "/var/log/app.log"


class TestCacheConfig:
    """Tests for CacheConfig dataclass."""

    def test_default_values(self):
        """Test default cache configuration."""
        config = CacheConfig()
        assert config.enabled is True
        assert config.ttl_seconds == 300
        assert config.max_entries == 1000

    def test_custom_values(self):
        """Test custom cache configuration."""
        config = CacheConfig(enabled=False, ttl_seconds=600, max_entries=500)
        assert config.enabled is False
        assert config.ttl_seconds == 600
        assert config.max_entries == 500


class TestSecurityConfig:
    """Tests for SecurityConfig dataclass."""

    def test_default_values(self):
        """Test default security configuration."""
        config = SecurityConfig()
        assert config.sanitize_urls is True
        assert isinstance(config.sensitive_params, list)
        assert "token" in config.sensitive_params
        assert "password" in config.sensitive_params
        assert "api_key" in config.sensitive_params

    def test_custom_sensitive_params(self):
        """Test custom sensitive parameters."""
        config = SecurityConfig(sensitive_params=["custom_token", "secret_key"])
        assert config.sensitive_params == ["custom_token", "secret_key"]


class TestAdvancedConfig:
    """Tests for AdvancedConfig dataclass."""

    def test_default_values(self):
        """Test default advanced configuration."""
        config = AdvancedConfig()
        assert config.use_regex is False
        assert config.fuzzy_threshold == 0.6
        assert config.parallel_queries is True
        assert config.max_query_limit == 1000

    def test_custom_values(self):
        """Test custom advanced configuration."""
        config = AdvancedConfig(
            use_regex=True, fuzzy_threshold=0.8, parallel_queries=False, max_query_limit=500
        )
        assert config.use_regex is True
        assert config.fuzzy_threshold == 0.8
        assert config.parallel_queries is False
        assert config.max_query_limit == 500


class TestConfig:
    """Tests for Config dataclass."""

    def test_default_values(self):
        """Test default configuration."""
        config = Config()
        assert config.default_browser == "chrome"
        assert config.default_limit == 5
        assert config.default_format == "markdown"
        assert config.log_level == "INFO"
        assert isinstance(config.logging, LoggingConfig)
        assert isinstance(config.cache, CacheConfig)
        assert isinstance(config.security, SecurityConfig)
        assert isinstance(config.advanced, AdvancedConfig)

    def test_custom_values(self):
        """Test custom configuration."""
        config = Config(
            default_browser="firefox",
            default_limit=10,
            default_format="json",
            log_level="DEBUG",
        )
        assert config.default_browser == "firefox"
        assert config.default_limit == 10
        assert config.default_format == "json"
        assert config.log_level == "DEBUG"


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_config_no_file(self, monkeypatch, tmp_path):
        """Test loading config when no file exists."""
        # Change to temp dir with no config file
        monkeypatch.chdir(tmp_path)
        config = load_config()
        assert isinstance(config, Config)
        assert config.default_browser == "chrome"

    def test_load_config_from_env(self, monkeypatch, tmp_path):
        """Test loading config from environment variable path."""
        config_file = tmp_path / "config.toml"
        config_file.write_text(
            '[default]\nbrowser = "firefox"\nlimit = 10\nformat = "json"\nlog_level = "DEBUG"\n'
        )

        monkeypatch.setenv("CHRONICLE_CONFIG", str(config_file))
        config = load_config()
        assert config.default_browser == "firefox"
        assert config.default_limit == 10
        assert config.default_format == "json"
        assert config.log_level == "DEBUG"

    def test_load_config_full_toml(self, monkeypatch, tmp_path):
        """Test loading full TOML configuration."""
        config_file = tmp_path / "chronicle.toml"
        config_file.write_text(
            """
[default]
browser = "edge"
limit = 20
format = "json"
log_level = "WARNING"

[logging]
level = "ERROR"
format = "detailed"
json_format = true
file_path = "/var/log/chronicle.log"

[cache]
enabled = false
ttl_seconds = 600
max_entries = 500

[security]
sanitize_urls = false
sensitive_params = ["token", "secret"]

[advanced]
use_regex = true
fuzzy_threshold = 0.8
parallel_queries = false
max_query_limit = 2000
"""
        )

        monkeypatch.chdir(tmp_path)
        config = load_config()

        assert config.default_browser == "edge"
        assert config.default_limit == 20
        assert config.default_format == "json"
        assert config.log_level == "WARNING"
        assert config.logging.level == "ERROR"
        assert config.logging.json_format is True
        assert config.logging.file_path == "/var/log/chronicle.log"
        assert config.cache.enabled is False
        assert config.cache.ttl_seconds == 600
        assert config.cache.max_entries == 500
        assert config.security.sanitize_urls is False
        assert config.advanced.use_regex is True
        assert config.advanced.fuzzy_threshold == 0.8

    def test_load_config_invalid_toml(self, monkeypatch, tmp_path, caplog):
        """Test loading invalid TOML file."""
        config_file = tmp_path / "chronicle.toml"
        config_file.write_text("invalid toml content [[[")

        monkeypatch.chdir(tmp_path)
        config = load_config()
        assert isinstance(config, Config)
        # Should use defaults and log warning

    def test_load_config_missing_tomllib(self, monkeypatch, tmp_path):
        """Test loading when tomllib is not available."""
        config_file = tmp_path / "chronicle.toml"
        config_file.write_text('[default]\nbrowser = "firefox"\n')

        monkeypatch.chdir(tmp_path)

        # Mock missing tomllib
        import sys

        # Remove tomllib from available modules
        monkeypatch.setitem(sys.modules, "tomllib", None)
        if "tomli" in sys.modules:
            monkeypatch.setitem(sys.modules, "tomli", None)

        config = load_config()
        assert isinstance(config, Config)


class TestGetEnvOverride:
    """Tests for get_env_override function."""

    def test_env_not_set(self):
        """Test when environment variable is not set."""
        result = get_env_override("test_var", "default_value")
        assert result == "default_value"

    def test_env_set_string(self, monkeypatch):
        """Test string environment variable."""
        monkeypatch.setenv("CHRONICLE_BROWSER", "firefox")
        result = get_env_override("browser", "chrome")
        assert result == "firefox"

    def test_env_set_int(self, monkeypatch):
        """Test integer environment variable."""
        monkeypatch.setenv("CHRONICLE_LIMIT", "10")
        result = get_env_override("limit", 5, int)
        assert result == 10

    def test_env_invalid_int(self, monkeypatch, caplog):
        """Test invalid integer conversion."""
        monkeypatch.setenv("CHRONICLE_LIMIT", "not_a_number")
        result = get_env_override("limit", 5, int)
        assert result == 5  # Should return default
        assert "Failed to convert" in caplog.text


class TestApplyEnvOverrides:
    """Tests for apply_env_overrides function."""

    def test_no_env_vars(self):
        """Test when no environment variables are set."""
        config = Config()
        result = apply_env_overrides(config)
        assert result.default_browser == "chrome"
        assert result.default_limit == 5

    def test_all_env_vars(self, monkeypatch):
        """Test with all environment variables set."""
        monkeypatch.setenv("CHRONICLE_BROWSER", "firefox")
        monkeypatch.setenv("CHRONICLE_LIMIT", "15")
        monkeypatch.setenv("CHRONICLE_FORMAT", "json")
        monkeypatch.setenv("CHRONICLE_LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("CHRONICLE_CACHE_TTL", "600")

        config = Config()
        result = apply_env_overrides(config)

        assert result.default_browser == "firefox"
        assert result.default_limit == 15
        assert result.default_format == "json"
        assert result.log_level == "DEBUG"
        assert result.cache.ttl_seconds == 600


class TestJSONFormatter:
    """Tests for JSONFormatter class."""

    def test_basic_format(self):
        """Test basic log formatting."""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.funcName = "test_function"

        result = formatter.format(record)
        data = json.loads(result)

        assert "timestamp" in data
        assert data["level"] == "INFO"
        assert data["message"] == "Test message"
        assert data["module"] == "test"
        assert data["function"] == "test_function"
        assert data["line"] == 1

    def test_format_with_exception(self):
        """Test formatting with exception."""
        formatter = JSONFormatter()

        try:
            raise ValueError("Test exception")
        except ValueError:
            exc_info = (type(ValueError()), ValueError("Test exception"), None)
            record = logging.LogRecord(
                name="test",
                level=logging.ERROR,
                pathname="test.py",
                lineno=1,
                msg="Error occurred",
                args=(),
                exc_info=exc_info,
            )

            result = formatter.format(record)
            data = json.loads(result)

            assert "exception" in data
            assert "Test exception" in data["exception"]

    def test_format_with_extra_data(self):
        """Test formatting with extra data."""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.extra_data = {"request_id": "12345", "user": "test_user"}

        result = formatter.format(record)
        data = json.loads(result)

        assert data["request_id"] == "12345"
        assert data["user"] == "test_user"


class TestSetupLogging:
    """Tests for setup_logging function.

    Note: These tests configure logging directly and may conflict with
    pytest's log capture. They should be run with -p no:logging if needed.
    """

    def _is_pytest_logging_active(self):
        """Check if pytest's logging plugin is interfering."""
        return any(type(h).__name__ == "LogCaptureHandler" for h in logging.getLogger().handlers)

    def test_setup_logging_basic(self, caplog):
        """Test basic logging setup creates handlers."""
        if self._is_pytest_logging_active():
            pytest.skip("Incompatible with pytest logging capture")
        setup_logging(level="INFO")
        logger = logging.getLogger()
        assert len(logger.handlers) >= 1
        assert logger.level == logging.INFO

    def test_setup_logging_custom_level(self, caplog):
        """Test logging with custom level creates handlers."""
        if self._is_pytest_logging_active():
            pytest.skip("Incompatible with pytest logging capture")
        setup_logging(level="DEBUG")
        logger = logging.getLogger()
        assert len(logger.handlers) >= 1
        assert logger.level == logging.DEBUG

    def test_setup_logging_from_config(self, monkeypatch, tmp_path, caplog):
        """Test logging setup from config file with JSON format."""
        if self._is_pytest_logging_active():
            pytest.skip("Incompatible with pytest logging capture")
        config_file = tmp_path / "chronicle.toml"
        config_file.write_text(
            """
[logging]
level = "ERROR"
json_format = true
"""
        )
        monkeypatch.chdir(tmp_path)
        setup_logging()

        logger = logging.getLogger()
        assert len(logger.handlers) >= 1
        assert logger.level == logging.ERROR

    def test_setup_logging_with_file(self, monkeypatch, tmp_path):
        """Test logging setup with file handler."""
        log_file = tmp_path / "test.log"

        config_file = tmp_path / "chronicle.toml"
        config_file.write_text(
            f"""
[logging]
level = "INFO"
file_path = "{log_file}"
"""
        )

        monkeypatch.chdir(tmp_path)
        setup_logging()

        logger = logging.getLogger("test")
        logger.info("Test message")
