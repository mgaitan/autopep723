# Usage Guide

## Installation

### Direct Execution (Recommended)

Run `autopep723` directly without installation using `uvx`:

```bash
uvx autopep723 script.py
```

This is the simplest way to use the tool and doesn't require any permanent installation.

### Permanent Installation

Install `autopep723` as a tool for repeated use:

```bash
uv tool install autopep723
```

After installation, you can use it directly:

```bash
autopep723 script.py
```

## Commands

### Run Mode (Default)

Execute a script with automatically detected dependencies:

```bash
autopep723 script.py
```

This analyzes the script's imports and runs it using `uv run` with the required packages.

### Check Mode

Analyze a script and print the PEP 723 metadata to stdout:

```bash
autopep723 check script.py
```

Example output:
```toml
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "requests",
#     "beautifulsoup4",
# ]
# ///
```

### Add Mode

Update a script file to include PEP 723 metadata:

```bash
autopep723 add script.py
```

This modifies the file in-place, adding the metadata block at the top. The `add` command is analogous to `uv add --script script.py 'dep1' 'dep2'`, but with automatic dependency detection - you don't need to manually specify which packages to add.

## Options

### Python Version

Specify a custom Python version requirement:

```bash
# For check mode
autopep723 check --python-version ">=3.11" script.py

# For add mode  
autopep723 add --python-version ">=3.12" script.py
```

### Version Information

Display the tool version:

```bash
autopep723 --version
```

### Help

Show available commands and options:

```bash
autopep723 --help
```

## Shebang Usage

### Basic Shebang

Make scripts executable with automatic dependency management:

```python
#!/usr/bin/env -S uvx autopep723
import requests
import pandas as pd

response = requests.get("https://api.example.com/data")
df = pd.DataFrame(response.json())
print(df.head())
```

**Note**: The `-S` flag is required for `env` to properly handle arguments with spaces. Without it, you'll get an error like `No such file or directory`.

Make the script executable and run it:

```bash
chmod +x script.py
./script.py
```

### How It Works

When using the shebang:

1. `uvx` creates an ephemeral virtual environment
2. `autopep723` is installed in that environment  
3. The script is analyzed for imports
4. Dependencies are installed on-the-fly
5. The script runs with all required packages available

This approach means:
- ✅ No permanent installation required
- ✅ No dependency conflicts with your system
- ✅ Clean, isolated execution environment
- ✅ Works on any system with `uv` installed

### Permanent Installation for Shebang

If you prefer, install `autopep723` permanently for shebang use:

```bash
uv tool install autopep723
```

Then use:

```python
#!/usr/bin/env autopep723
```

This doesn't require the `-S` flag since there are no arguments to pass.

## Import Name Mapping

The tool handles cases where import names differ from package names:

| Import Statement | Detected Package |
|------------------|------------------|
| `import PIL` | `Pillow` |
| `from bs4 import BeautifulSoup` | `beautifulsoup4` |
| `import cv2` | `opencv-python` |
| `import yaml` | `PyYAML` |
| `from sklearn import datasets` | `scikit-learn` |
| `import jwt` | `PyJWT` |
| `from dotenv import load_dotenv` | `python-dotenv` |

The tool includes 35+ built-in mappings for common packages.

## Behavior with Existing Metadata

If a script already contains PEP 723 metadata, `autopep723` will:

- **Run mode**: Use existing dependencies instead of analyzing imports
- **Check mode**: Display the existing metadata
- **Add mode**: Skip the file (no changes made)

This prevents overwriting manually curated dependency lists.

## Error Handling

### Missing `uv`

If `uv` is not installed, you'll see:

```
Error: uv is required but not found in PATH
Install it from: https://docs.astral.sh/uv/getting-started/installation/
```

### Syntax Errors

Scripts with syntax errors are handled gracefully:

```bash
autopep723 check broken_script.py
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
```

### File Not Found

Clear error messages for missing files:

```bash
autopep723 nonexistent.py
Error: File 'nonexistent.py' not found
```

## Tips

### Development Workflow

1. Write your script with imports
2. Test it with `autopep723 script.py`
3. If satisfied, add metadata: `autopep723 add script.py`
4. Commit the script with embedded metadata

### CI/CD Integration

Use in CI pipelines to validate dependencies:

```bash
# Check if script metadata is up to date
autopep723 check script.py > expected_deps.toml
# Compare with existing metadata or fail if missing
```

### Performance

Analysis is fast since it only uses AST parsing without network requests. Dependency installation only happens during script execution.