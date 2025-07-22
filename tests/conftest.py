"""Test configuration for autopep723."""

import sys
from pathlib import Path

import pytest

# Add src to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(autouse=True)
def setup_logger():
    """Initialize logger for all tests with verbose=False and colors=False."""
    from autopep723.logger import init_logger

    # Initialize logger without colors for consistent test output
    init_logger(verbose=False, use_colors=False)
    yield


@pytest.fixture
def setup_verbose_logger():
    """Initialize logger with verbose=True for specific tests."""
    from autopep723.logger import init_logger

    # Initialize logger with verbose mode for specific tests
    init_logger(verbose=True, use_colors=False)
    yield

    # Reset to non-verbose after test
    init_logger(verbose=False, use_colors=False)
