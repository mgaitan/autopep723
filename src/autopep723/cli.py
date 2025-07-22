"""CLI module for autopep723 - handles argument parsing and command setup."""

import argparse
import sys
from importlib.metadata import version


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Auto-generate PEP 723 metadata for Python scripts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  autopep723 script.py                   # Run script (default behavior)
  autopep723 https://example.com/script.py  # Run remote script
  autopep723 check script.py             # Print metadata to stdout
  autopep723 add script.py               # Update file with metadata

Shebang usage:
  #!/usr/bin/env autopep723
  import requests
  print("Hello world!")
        """,
    )

    try:
        package_version = version("autopep723")
    except Exception:
        package_version = "unknown"

    parser.add_argument("--version", action="version", version=f"%(prog)s {package_version}")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show verbose output including download progress and commands"
    )

    # Create subparsers
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Check command
    check_parser = subparsers.add_parser("check", help="Analyze script and print metadata")
    check_parser.add_argument("script", help="Path to Python script or URL")
    check_parser.add_argument(
        "--python-version",
        default=">=3.13",
        help="Required Python version (default: >=3.13)",
    )
    check_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show verbose output including download progress and commands"
    )

    # Add command
    add_parser = subparsers.add_parser("add", help="Update script with metadata")
    add_parser.add_argument("script", help="Path to Python script or URL")
    add_parser.add_argument(
        "--python-version",
        default=">=3.13",
        help="Required Python version (default: >=3.13)",
    )
    add_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show verbose output including download progress and commands"
    )

    return parser


def should_show_help() -> bool:
    """Check if help should be shown (no arguments provided)."""
    return len(sys.argv) == 1


def is_default_run_command() -> bool:
    """Check if this is a default run command (script execution)."""
    if len(sys.argv) < 2:
        return False

    # Check if first argument is not a subcommand or help flag
    first_arg = sys.argv[1]
    subcommands = ["check", "add"]
    help_flags = ["--help", "--version", "-h"]

    return first_arg not in subcommands and first_arg not in help_flags


def get_script_path_from_args() -> str:
    """Get script path from command line arguments for default run command."""
    # Filter out verbose flags to get the script path
    args = [arg for arg in sys.argv[1:] if arg not in ["-v", "--verbose"]]
    if not args:
        raise ValueError("No script path provided")
    return args[0]


def get_script_args_from_args() -> list[str]:
    """Get additional script arguments from command line arguments for default run command."""
    # Filter out verbose flags to get all arguments
    args = [arg for arg in sys.argv[1:] if arg not in ["-v", "--verbose"]]
    if len(args) <= 1:
        return []
    # Return all arguments after the script path
    return args[1:]
