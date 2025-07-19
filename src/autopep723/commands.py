"""Commands module for autopep723 - handles different command implementations."""

import sys
from pathlib import Path

from rich.console import Console
from rich.syntax import Syntax

from . import (
    generate_pep723_metadata,
    get_third_party_imports,
    has_pep723_metadata,
    run_with_uv,
    update_file_with_metadata,
)
from .validation import validate_and_prepare_script, validate_uv_available

console = Console()


def run_script_command(script_path_str: str) -> None:
    """Handle the default script execution command.

    Args:
        script_path_str: Path to the script as string
    """
    script_path = Path(script_path_str)

    # Validate prerequisites
    validate_uv_available()
    validate_and_prepare_script(script_path)

    # Check for existing PEP 723 metadata
    if has_pep723_metadata(script_path):
        console.print("[blue]Script already has PEP 723 metadata. Using existing dependencies.[/blue]")
        run_with_uv(script_path, [])  # Let uv handle dependencies from metadata
    else:
        # Analyze imports and run with detected dependencies
        dependencies = get_third_party_imports(script_path)

        if dependencies:
            console.print(f"[blue]Detected dependencies:[/blue] {', '.join(dependencies)}")
        else:
            console.print("[blue]No third-party dependencies detected.[/blue]")

        run_with_uv(script_path, dependencies)


def check_command(script_path_str: str, python_version: str) -> None:
    """Handle the check command - analyze and print metadata.

    Args:
        script_path_str: Path to the script as string
        python_version: Required Python version
    """
    script_path = Path(script_path_str)

    if not script_path.exists():
        console.print(f"[red]Error: Script '{script_path}' does not exist.[/red]")
        sys.exit(1)

    dependencies = get_third_party_imports(script_path)
    metadata = generate_pep723_metadata(dependencies, python_version)

    syntax = Syntax(metadata, "toml", theme="monokai", line_numbers=False)
    console.print(syntax)


def upgrade_command(script_path_str: str, python_version: str) -> None:
    """Handle the upgrade command - update script with metadata.

    Args:
        script_path_str: Path to the script as string
        python_version: Required Python version
    """
    script_path = Path(script_path_str)

    if not script_path.exists():
        console.print(f"[red]Error: Script '{script_path}' does not exist.[/red]")
        sys.exit(1)

    dependencies = get_third_party_imports(script_path)
    metadata = generate_pep723_metadata(dependencies, python_version)

    update_file_with_metadata(script_path, metadata)
    console.print(f"[green]Updated {script_path} with PEP 723 metadata.[/green]")

    if dependencies:
        console.print(f"[blue]Dependencies:[/blue] {', '.join(dependencies)}")
    else:
        console.print("[blue]No third-party dependencies detected.[/blue]")
