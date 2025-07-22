"""Commands module for autopep723 - handles different command implementations."""

import sys
from pathlib import Path

from . import (
    generate_pep723_metadata,
    get_third_party_imports,
    has_pep723_metadata,
    run_with_uv,
    update_file_with_metadata,
)
from .validation import validate_and_prepare_script, validate_uv_available


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
        print("Script already has PEP 723 metadata. Using existing dependencies.")
        run_with_uv(script_path, [])  # Let uv handle dependencies from metadata
    else:
        # Analyze imports and run with detected dependencies
        dependencies = get_third_party_imports(script_path)

        if dependencies:
            print(f"Detected dependencies: {', '.join(dependencies)}")
        else:
            print("No third-party dependencies detected.")

        run_with_uv(script_path, dependencies)


def check_command(script_path_str: str, python_version: str) -> None:
    """Handle the check command - analyze and print metadata.

    Args:
        script_path_str: Path to the script as string
        python_version: Required Python version
    """
    script_path = Path(script_path_str)

    if not script_path.exists():
        print(f"Error: Script '{script_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    dependencies = get_third_party_imports(script_path)
    metadata = generate_pep723_metadata(dependencies, python_version)

    print(metadata)


def add_command(script_path_str: str, python_version: str) -> None:
    """Handle the add command - update script with metadata.

    Args:
        script_path_str: Path to the script as string
        python_version: Required Python version
    """
    script_path = Path(script_path_str)

    if not script_path.exists():
        print(f"Error: Script '{script_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    dependencies = get_third_party_imports(script_path)
    metadata = generate_pep723_metadata(dependencies, python_version)

    update_file_with_metadata(script_path, metadata)
    print(f"Updated {script_path} with PEP 723 metadata.")

    if dependencies:
        print(f"Dependencies: {', '.join(dependencies)}")
    else:
        print("No third-party dependencies detected.")
