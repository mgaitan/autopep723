import ast
import pkgutil
import subprocess
import sys
from pathlib import Path

from rich.console import Console

console = Console()

# Mapping for packages where import name differs from install name
IMPORT_TO_PACKAGE_MAP = {
    "PIL": "Pillow",
    "yaml": "PyYAML",
    "bs4": "beautifulsoup4",
    "sklearn": "scikit-learn",
    "skimage": "scikit-image",
    "cv2": "opencv-python",
    "serial": "pyserial",
    "usb": "pyusb",
    "Crypto": "pycryptodome",
    "OpenGL": "PyOpenGL",
    "setuptools_scm": "setuptools-scm",
    "flask_sqlalchemy": "Flask-SQLAlchemy",
    "flask_login": "Flask-Login",
    "flask_migrate": "Flask-Migrate",
    "flask_wtf": "Flask-WTF",
    "flask_mail": "Flask-Mail",
    "flask_cors": "Flask-Cors",
    "flask_jwt_extended": "Flask-JWT-Extended",
    "flask_restful": "Flask-RESTful",
    "flask_bcrypt": "Flask-Bcrypt",
    "psycopg2": "psycopg2-binary",
    "pyside2": "PySide2",
    "win32com": "pywin32",
    "Xlib": "python-xlib",
    "Levenshtein": "python-Levenshtein",
    "dash_bootstrap_components": "dash-bootstrap-components",
    "dash_table": "dash-table",
    "pandas_datareader": "pandas-datareader",
    "jupyter_core": "jupyter-core",
    "jupyter_client": "jupyter-client",
    "prometheus_client": "prometheus-client",
    "sqlalchemy_utils": "SQLAlchemy-Utils",
    "sqlalchemy_mixins": "sqlalchemy-mixins",
    "markdown_it": "markdown-it-py",
    "email_validator": "email-validator",
    "python_jose": "python-jose",
    "jwt": "PyJWT",
    "python_http_client": "python-http-client",
    "dateutil": "python-dateutil",
    "dotenv": "python-dotenv",
    "fitz": "PyMuPDF",
    "ConfigParser": "configparser",
}


def get_builtin_modules() -> set[str]:
    """Get a set of all built-in modules in Python."""
    builtin_modules = set(sys.builtin_module_names)

    # Add standard library modules
    for module_info in pkgutil.iter_modules():
        builtin_modules.add(module_info.name)

    return builtin_modules


def get_third_party_imports(file_path: Path) -> list[str]:
    """Parse a Python file and extract third-party imports.

    Args:
        file_path: Path to the Python file to analyze

    Returns:
        List of third-party package names
    """
    with open(file_path, encoding="utf-8") as file:
        try:
            content = file.read()
            tree = ast.parse(content)
        except SyntaxError as e:
            console.print(f"[red]Error parsing {file_path}: {e}[/red]")
            return []

    builtin_modules = get_builtin_modules()
    all_imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                module_name = name.name.split(".")[0]
                all_imports.add(module_name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            module_name = node.module.split(".")[0]
            all_imports.add(module_name)

    # Filter out built-in modules and convert to package names
    third_party_imports = []
    for imp in sorted(all_imports):
        if imp not in builtin_modules:
            package_name = IMPORT_TO_PACKAGE_MAP.get(imp, imp)
            third_party_imports.append(package_name)

    return sorted(set(third_party_imports))


def generate_pep723_metadata(dependencies: list[str], python_version: str = ">=3.13") -> str:
    """Generate PEP 723 metadata block.

    Args:
        dependencies: List of package dependencies
        python_version: Required Python version

    Returns:
        PEP 723 metadata as string
    """
    if not dependencies:
        metadata = f'''# /// script
# requires-python = "{python_version}"
# ///'''
    else:
        deps_str = ",\n#     ".join(f'"{dep}"' for dep in dependencies)
        metadata = f'''# /// script
# requires-python = "{python_version}"
# dependencies = [
#     {deps_str},
# ]
# ///'''

    return metadata


def has_existing_metadata(content: str) -> bool:
    """Check if the file already has PEP 723 metadata."""
    return "# /// script" in content and "# ///" in content


def extract_existing_metadata(content: str) -> tuple[str, str, str]:
    """Extract existing metadata and return (before, metadata, after) parts."""
    lines = content.splitlines(keepends=True)
    start_idx = None
    end_idx = None

    for i, line in enumerate(lines):
        if "# /// script" in line:
            start_idx = i
        elif start_idx is not None and "# ///" in line and i > start_idx:
            end_idx = i + 1
            break

    if start_idx is not None and end_idx is not None:
        before = "".join(lines[:start_idx])
        metadata = "".join(lines[start_idx:end_idx])
        after = "".join(lines[end_idx:])
        return before, metadata, after

    return content, "", ""


def update_file_with_metadata(file_path: Path, metadata: str) -> None:
    """Update the file with new PEP 723 metadata."""
    with open(file_path, encoding="utf-8") as file:
        content = file.read()

    if has_existing_metadata(content):
        before, _, after = extract_existing_metadata(content)
        new_content = before + metadata + "\n" + after
    else:
        # Add metadata at the beginning, after shebang if present
        lines = content.splitlines(keepends=True)
        if lines and lines[0].startswith("#!"):
            new_content = lines[0] + metadata + "\n" + "".join(lines[1:])
        else:
            new_content = metadata + "\n" + content

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(new_content)


def run_with_uv(script_path: Path, dependencies: list[str]) -> None:
    """Run the script using uv run with dependencies."""
    cmd = ["uv", "run"]

    for dep in dependencies:
        cmd.extend(["--with", dep])

    cmd.append(str(script_path))

    console.print(f"[green]Running:[/green] {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error running script: {e}[/red]")
        sys.exit(1)
    except FileNotFoundError:
        console.print("[red]Error: 'uv' command not found. Please install uv first.[/red]")
        sys.exit(1)


def check_uv_available() -> bool:
    """Check if uv is available in the system."""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def has_pep723_metadata(script_path: Path) -> bool:
    """Check if script already has PEP 723 metadata."""
    try:
        with open(script_path, encoding="utf-8") as f:
            content = f.read()
            return has_existing_metadata(content)
    except Exception:
        return False


def main() -> None:
    """Main entry point for autopep723."""
    from .cli import (
        create_parser,
        get_script_path_from_args,
        is_default_run_command,
        should_show_help,
    )
    from .commands import check_command, run_script_command, upgrade_command

    # Handle help case
    if should_show_help():
        parser = create_parser()
        parser.print_help()
        sys.exit(1)

    # Handle default run command (script execution)
    if is_default_run_command():
        script_path = get_script_path_from_args()
        run_script_command(script_path)
        return

    # Handle subcommands
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "check":
        check_command(args.script, args.python_version)
    elif args.command == "upgrade":
        upgrade_command(args.script, args.python_version)


if __name__ == "__main__":
    main()
