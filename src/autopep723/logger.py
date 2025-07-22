"""Simple logging module with ANSI colors for autopep723."""

import logging
import sys
from typing import ClassVar


class ColoredFormatter(logging.Formatter):
    """Formatter that adds ANSI colors to log messages."""

    COLORS: ClassVar = {
        "DEBUG": "\033[90m",  # Gray
        "INFO": "",  # Default
        "WARNING": "\033[93m",  # Bright yellow
        "ERROR": "\033[91m",  # Bright red
        "SUCCESS": "\033[92m",  # Bright green
        "COMMAND": "\033[94m",  # Bright blue
    }
    RESET: ClassVar = "\033[0m"

    def __init__(self, use_colors: bool = True):
        super().__init__("%(message)s")
        self.use_colors = use_colors and self._supports_color()

    def _supports_color(self) -> bool:
        """Check if terminal supports ANSI colors."""
        import os

        if not sys.stdout.isatty():
            return False
        if os.environ.get("NO_COLOR"):
            return False
        term = os.environ.get("TERM", "")
        return term not in ("dumb", "")

    def format(self, record):
        if self.use_colors and record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            record.msg = f"{color}{record.msg}{self.RESET}"
        return super().format(record)


def init_logger(verbose: bool = False, use_colors: bool = True) -> None:
    """Initialize the autopep723 logger."""
    logger = logging.getLogger("autopep723")

    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add stdout handler for info/debug/success
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(ColoredFormatter(use_colors))
    stdout_handler.addFilter(lambda record: record.levelno < logging.WARNING)
    logger.addHandler(stdout_handler)

    # Add stderr handler for warnings/errors
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(ColoredFormatter(use_colors))
    stderr_handler.addFilter(lambda record: record.levelno >= logging.WARNING)
    logger.addHandler(stderr_handler)

    # Set level
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.propagate = True

    # Add custom levels
    logging.addLevelName(25, "SUCCESS")
    logging.addLevelName(35, "COMMAND")


def get_logger():
    """Get the autopep723 logger."""
    return logging.getLogger("autopep723")


# Convenience functions
def info(msg: str) -> None:
    get_logger().info(msg)


def success(msg: str) -> None:
    get_logger().log(25, msg)


def warning(msg: str) -> None:
    get_logger().warning(f"Warning: {msg}")


def error(msg: str) -> None:
    get_logger().error(f"Error: {msg}")


def verbose(msg: str) -> None:
    get_logger().debug(msg)


def command(msg: str) -> None:
    get_logger().debug(f"🚀 Running: {msg}")
