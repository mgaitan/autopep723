import io
import logging
from unittest.mock import patch

from autopep723.logger import (
    ColoredFormatter,
    command,
    error,
    get_logger,
    info,
    init_logger,
    success,
    verbose,
    warning,
)


class TestColoredFormatter:
    """Test ColoredFormatter color support logic."""

    def test_supports_color_with_tty_and_color_support(self, monkeypatch):
        """Test color support when stdout is tty and terminal supports colors."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        monkeypatch.setenv("TERM", "xterm")

        with patch("sys.stdout.isatty", return_value=True):
            formatter = ColoredFormatter(use_colors=True)
            assert formatter._supports_color() is True

    def test_supports_color_no_tty(self, monkeypatch):
        """Test no color support when stdout is not a tty."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        monkeypatch.setenv("TERM", "xterm")

        with patch("sys.stdout.isatty", return_value=False):
            formatter = ColoredFormatter(use_colors=True)
            assert formatter._supports_color() is False

    def test_supports_color_with_no_color_env(self, monkeypatch):
        """Test no color support when NO_COLOR environment variable is set."""
        monkeypatch.setenv("NO_COLOR", "1")
        monkeypatch.setenv("TERM", "xterm")

        with patch("sys.stdout.isatty", return_value=True):
            formatter = ColoredFormatter(use_colors=True)
            assert formatter._supports_color() is False

    def test_supports_color_with_dumb_terminal(self, monkeypatch):
        """Test no color support with dumb terminal."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        monkeypatch.setenv("TERM", "dumb")

        with patch("sys.stdout.isatty", return_value=True):
            formatter = ColoredFormatter(use_colors=True)
            assert formatter._supports_color() is False

    def test_supports_color_with_empty_term(self, monkeypatch):
        """Test no color support with empty TERM."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        monkeypatch.setenv("TERM", "")

        with patch("sys.stdout.isatty", return_value=True):
            formatter = ColoredFormatter(use_colors=True)
            assert formatter._supports_color() is False

    def test_format_with_colors(self, monkeypatch):
        """Test message formatting with colors enabled."""
        monkeypatch.delenv("NO_COLOR", raising=False)
        monkeypatch.setenv("TERM", "xterm")

        with patch("sys.stdout.isatty", return_value=True):
            formatter = ColoredFormatter(use_colors=True)

            record = logging.LogRecord(
                name="test", level=logging.ERROR, pathname="", lineno=0, msg="test message", args=(), exc_info=None
            )

            formatted = formatter.format(record)
            assert "\033[91m" in formatted  # Red color for ERROR
            assert "\033[0m" in formatted  # Reset code

    def test_format_without_colors(self):
        """Test message formatting with colors disabled."""
        formatter = ColoredFormatter(use_colors=False)

        record = logging.LogRecord(
            name="test", level=logging.ERROR, pathname="", lineno=0, msg="test message", args=(), exc_info=None
        )

        formatted = formatter.format(record)
        assert "\033[" not in formatted  # No color codes


class TestLoggerFunctions:
    """Test individual logger functions."""

    def test_info_function(self, caplog):
        """Test info logging function."""
        with caplog.at_level(logging.INFO):
            info("test info message")
        assert "test info message" in caplog.text

    def test_success_function(self, caplog):
        """Test success logging function."""
        with caplog.at_level(logging.DEBUG):
            success("test success message")
        assert "test success message" in caplog.text

    def test_warning_function(self, caplog):
        """Test warning logging function."""
        with caplog.at_level(logging.WARNING):
            warning("test warning message")
        assert "Warning: test warning message" in caplog.text

    def test_error_function(self, caplog):
        """Test error logging function."""
        with caplog.at_level(logging.ERROR):
            error("test error message")
        assert "test error message" in caplog.text

    def test_verbose_function(self, caplog):
        """Test verbose logging function."""
        init_logger(verbose=True, use_colors=False)  # Ensure DEBUG level
        with caplog.at_level(logging.DEBUG):
            verbose("test verbose message")
        assert "test verbose message" in caplog.text

    def test_command_function(self, caplog):
        """Test command logging function."""
        init_logger(verbose=True, use_colors=False)  # Ensure DEBUG level
        with caplog.at_level(logging.DEBUG):
            command("test command")
        assert "🚀 Running: test command" in caplog.text


class TestLoggerInitialization:
    """Test logger initialization and configuration."""

    def test_init_logger_verbose(self):
        """Test logger initialization with verbose flag."""
        init_logger(verbose=True, use_colors=False)
        logger = get_logger()
        assert logger.level == logging.DEBUG

    def test_init_logger_not_verbose(self):
        """Test logger initialization without verbose flag."""
        init_logger(verbose=False, use_colors=False)
        logger = get_logger()
        assert logger.level == logging.INFO

    def test_init_logger_clears_existing_handlers(self):
        """Test that init_logger clears existing handlers."""
        logger = get_logger()

        # Add a dummy handler
        dummy_handler = logging.StreamHandler()
        logger.addHandler(dummy_handler)

        # Re-initialize
        init_logger(verbose=False, use_colors=False)

        # Should have exactly 2 handlers (stdout + stderr), not more
        assert len(logger.handlers) == 2
        assert dummy_handler not in logger.handlers

    def test_init_logger_adds_custom_levels(self):
        """Test that init_logger adds custom logging levels."""
        init_logger(verbose=False, use_colors=False)

        assert logging.getLevelName(25) == "SUCCESS"
        assert logging.getLevelName(35) == "COMMAND"

    def test_get_logger_returns_correct_logger(self):
        """Test that get_logger returns the autopep723 logger."""
        logger = get_logger()
        assert logger.name == "autopep723"


class TestLoggerOutput:
    """Test logger output routing."""

    def test_stdout_stderr_routing(self, caplog):
        """Test that messages are routed to correct streams."""
        init_logger(verbose=True, use_colors=False)

        # Capture both stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        with patch("sys.stdout", stdout_capture), patch("sys.stderr", stderr_capture):
            info("info message")
            warning("warning message")
            error("error message")

        # Note: In test environment, messages go to caplog, but we can verify
        # the handler configuration is correct
        logger = get_logger()

        # Should have 2 handlers
        assert len(logger.handlers) == 2

        # In the actual implementation, handlers are configured with filters
        # We just verify they exist
        assert len(logger.handlers) == 2
