"""CLI module for autopep723 - handles argument parsing and command setup."""

import argparse
import sys


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Auto-generate PEP 723 metadata for Python scripts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  autopep723 script.py                   # Run script (default behavior)
  autopep723 check script.py             # Print metadata to stdout
  autopep723 upgrade script.py           # Update file with metadata

Shebang usage:
  #!/usr/bin/env autopep723
  import requests
  print("Hello world!")
        """,
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    # Create subparsers
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Check command
    check_parser = subparsers.add_parser(
        "check", help="Analyze script and print metadata"
    )
    check_parser.add_argument("script", help="Path to Python script")
    check_parser.add_argument(
        "--python-version",
        default=">=3.13",
        help="Required Python version (default: >=3.13)",
    )

    # Upgrade command
    upgrade_parser = subparsers.add_parser(
        "upgrade", help="Update script with metadata"
    )
    upgrade_parser.add_argument("script", help="Path to Python script")
    upgrade_parser.add_argument(
        "--python-version",
        default=">=3.13",
        help="Required Python version (default: >=3.13)",
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
    subcommands = ["check", "upgrade"]
    help_flags = ["--help", "--version", "-h"]

    return first_arg not in subcommands and first_arg not in help_flags


def get_script_path_from_args() -> str:
    """Get script path from command line arguments for default run command."""
    return sys.argv[1]
