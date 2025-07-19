# autopep723

A CLI tool that automatically generates PEP 723 metadata for Python scripts by analyzing their imports and dependencies.

## Overview

`autopep723` parses Python scripts using AST (Abstract Syntax Tree) analysis to detect third-party package imports and generates the appropriate PEP 723 inline script metadata. This metadata can be used by tools like `uv run` to automatically install and manage dependencies when executing scripts.

## Features

- **Automatic dependency detection**: Analyzes Python scripts to identify third-party packages
- **Import name mapping**: Handles cases where import names differ from package names (e.g., `import PIL` → `pillow`)
- **Multiple output modes**: Print metadata, update files in-place, or run scripts directly
- **PEP 723 compliant**: Generates properly formatted inline script metadata
- **Built-in module filtering**: Automatically excludes standard library modules
- **Syntax error handling**: Gracefully handles files with syntax errors

## Installation

```bash
# Install from source
git clone <repository-url>
cd autopep723
uv sync
```

## Usage

### Basic Usage

```bash
# Run script with uv and detected dependencies (default)
autopep723 script.py

# Print PEP 723 metadata to stdout
autopep723 check script.py

# Update the script file with metadata
autopep723 upgrade script.py
```

### Advanced Options

```bash
# Specify Python version requirement when checking
autopep723 check --python-version ">=3.11" script.py

# Update file with custom Python version
autopep723 upgrade --python-version ">=3.12" script.py

# Check version
autopep723 --version
```

## Examples

### Example 1: Simple Script Analysis

Given a script `example.py`:

```python
import requests
from bs4 import BeautifulSoup
import json

response = requests.get("https://example.com")
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.title)
```

Running `autopep723 check example.py` outputs:

```toml
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "beautifulsoup4",
#     "requests",
# ]
# ///
```

### Example 2: Updating a Script

Running `autopep723 upgrade example.py` modifies the file to:

```python
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "beautifulsoup4",
#     "requests",
# ]
# ///

import requests
from bs4 import BeautifulSoup
import json

response = requests.get("https://example.com")
soup = BeautifulSoup(response.content, 'html.parser')
print(soup.title)
```

### Example 3: Running with Dependencies

`autopep723 example.py` executes:

```bash
uv run --with beautifulsoup4 --with requests example.py
```

## Import Name Mapping

The tool includes a comprehensive mapping for packages where the import name differs from the installation name:

| Import Name | Package Name |
|-------------|--------------|
| `bs4` | `beautifulsoup4` |
| `PIL` | `Pillow` |
| `cv2` | `opencv-python` |
| `yaml` | `PyYAML` |
| `sklearn` | `scikit-learn` |
| `dateutil` | `python-dateutil` |
| `jwt` | `PyJWT` |
| `dotenv` | `python-dotenv` |
| `fitz` | `PyMuPDF` |
| ... and 35+ more mappings |

## Shebang Integration

You can use `autopep723` directly as a shebang:

```python
#!/usr/bin/env autopep723
import requests
import numpy as np

# Your script here...
```

This allows you to run scripts without explicitly declaring dependencies in PEP 723 format. The tool will automatically detect dependencies and run the script with `uv run`.

If the script already contains PEP 723 metadata, autopep723 will use the existing dependencies instead of analyzing imports.

## CLI Reference

### Commands

```
autopep723 [SCRIPT]                    # Run script (default behavior)
autopep723 check [OPTIONS] SCRIPT      # Analyze and print metadata
autopep723 upgrade [OPTIONS] SCRIPT    # Update script with metadata

Global Options:
  --version              Show version
  --help                 Show help message

Command Options:
  --python-version TEXT  Required Python version (default: >=3.13)
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=autopep723

# Run specific test file
uv run pytest tests/test_autopep723.py

# Quick test
uv run pytest -q
```

### Project Structure

```
autopep723/
├── src/
│   └── autopep723/
│       └── __init__.py          # Main module
├── tests/
│   ├── test_autopep723.py       # Core functionality tests
│   └── test_cli.py              # CLI tests
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

## How It Works

1. **AST Parsing**: The script is parsed using Python's `ast` module to extract import statements
2. **Import Analysis**: All `import` and `from ... import` statements are analyzed
3. **Filtering**: Built-in and standard library modules are filtered out
4. **Mapping**: Import names are mapped to their corresponding package names using the built-in dictionary
5. **Metadata Generation**: PEP 723 compliant metadata is generated with the detected dependencies

## Limitations

- Only analyzes static imports (not dynamic imports using `importlib`)
- Import name mapping only includes packages where import name differs from install name
- Cannot detect conditional imports that depend on runtime conditions
- Requires `uv` to be installed for script execution (shows helpful error if missing)
- Only works with Python scripts (`.py` files)
- Shebang usage requires autopep723 to be installed globally or in PATH

## Error Handling

- **Missing `uv`**: If `uv` is not installed, autopep723 shows an error with installation instructions
- **Existing metadata**: If a script already has PEP 723 metadata, autopep723 uses existing dependencies instead of analyzing imports
- **Syntax errors**: Scripts with syntax errors are handled gracefully, returning empty dependency lists
- **Non-existent files**: Clear error messages for missing files
- **Permission errors**: Proper error handling for file access issues

## Installation

To use autopep723 as a shebang, install it globally:

```bash
# Install globally with uv
uv tool install autopep723

# Or install in your PATH however you prefer
pipx install autopep723
```

Then you can use it in shebangs:

```python
#!/usr/bin/env autopep723
import requests
print("This will run with requests automatically installed!")
```

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is open source. See the license file for details.

## Related Projects

- [PEP 723](https://peps.python.org/pep-0723/) - Inline script metadata specification
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver