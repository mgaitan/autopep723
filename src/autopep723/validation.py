"""Validation module for autopep723 - handles common validation logic."""

import sys
from pathlib import Path

from rich.console import Console

console = Console()


def validate_script_exists(script_path: Path) -> bool:
    """Validate that the script file exists.

    Args:
        script_path: Path to the script file

    Returns:
        True if script exists, False otherwise (exits with error)
    """
    if not script_path.exists():
        console.print(f"[red]Error: Script '{script_path}' does not exist.[/red]")
        sys.exit(1)
    return True


def check_script_extension(script_path: Path) -> None:
    """Check script extension and warn if not .py.

    Args:
        script_path: Path to the script file
    """
    if script_path.suffix != ".py":
        console.print(
            f"[yellow]Warning: '{script_path}' does not have a .py extension.[/yellow]"
        )


def check_uv_available() -> bool:
    """Check if uv is available in the system."""
    import subprocess

    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def validate_uv_available() -> bool:
    """Validate that uv is available and exit if not.

    Returns:
        True if uv is available, exits with error otherwise
    """
    if not check_uv_available():
        console.print(
            "[red]Error: 'uv' is not installed or not available in PATH.[/red]"
        )
        console.print("Please install uv: https://github.com/astral-sh/uv")
        sys.exit(1)
    return True


def validate_and_prepare_script(script_path: Path) -> None:
    """Perform all common script validations.

    Args:
        script_path: Path to the script file
    """
    validate_script_exists(script_path)
    check_script_extension(script_path)
