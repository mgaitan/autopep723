"""Commands module for autopep723 - handles different command implementations."""

from . import (
    generate_pep723_metadata,
    get_third_party_imports,
    has_pep723_metadata,
    resolve_script_path,
    run_with_uv,
    update_file_with_metadata,
)
from .logger import success, verbose
from .validation import validate_script_input, validate_uv_available


def run_script_command(script_input: str) -> None:
    """Handle the default script execution command.

    Args:
        script_input: Path to the script or URL as string
    """

    # Validate prerequisites
    validate_uv_available()
    validate_script_input(script_input)

    # Resolve script path (download if URL)
    script_path = resolve_script_path(script_input)

    # Check for existing PEP 723 metadata
    if has_pep723_metadata(script_path):
        verbose("Script already has PEP 723 metadata. Using existing dependencies.")
        run_with_uv(script_path, [])  # Let uv handle dependencies from metadata
    else:
        # Analyze imports and run with detected dependencies
        dependencies = get_third_party_imports(script_path)

        if dependencies:
            verbose(f"📦 Detected dependencies: {', '.join(dependencies)}")
        else:
            verbose("✨ No third-party dependencies detected")

        run_with_uv(script_path, dependencies)


def check_command(script_input: str, python_version: str) -> None:
    """Handle the check command - analyze and print metadata.

    Args:
        script_input: Path to the script or URL as string
        python_version: Required Python version
    """

    # Validate input and resolve path
    validate_script_input(script_input)
    script_path = resolve_script_path(script_input)

    dependencies = get_third_party_imports(script_path)
    metadata = generate_pep723_metadata(dependencies, python_version)

    print(metadata)


def add_command(script_input: str, python_version: str) -> None:
    """Handle the add command - update script with metadata.

    Args:
        script_input: Path to the script or URL as string
        python_version: Required Python version
    """

    # Validate input and resolve path
    validate_script_input(script_input)
    script_path = resolve_script_path(script_input)

    # Note: For URLs, we can't update the original file
    # This will work on the downloaded temporary file
    if script_input != str(script_path):
        from .logger import warning

        warning(f"Working with downloaded script at {script_path}")
        warning("Cannot update original remote script.")

    dependencies = get_third_party_imports(script_path)
    metadata = generate_pep723_metadata(dependencies, python_version)

    update_file_with_metadata(script_path, metadata)
    success(f"✓ Updated {script_path} with PEP 723 metadata")

    if dependencies:
        success(f"Dependencies added: {', '.join(dependencies)}")
    else:
        success("No external dependencies found")
