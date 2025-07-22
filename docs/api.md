# API Reference

## Command Line Interface

### Main Commands

#### `autopep723 [SCRIPT]`
Run a script with automatically detected dependencies (default behavior).

**Arguments:**
- `SCRIPT` - Path to Python script to execute

**Example:**
```bash
autopep723 script.py
```

#### `autopep723 check [OPTIONS] SCRIPT`
Analyze script and print PEP 723 metadata to stdout.

**Arguments:**
- `SCRIPT` - Path to Python script to analyze

**Options:**
- `--python-version TEXT` - Python version requirement (default: `>=3.9`)

**Example:**
```bash
autopep723 check --python-version ">=3.11" script.py
```

#### `autopep723 add [OPTIONS] SCRIPT`
Update script file with PEP 723 metadata in-place.

**Arguments:**
- `SCRIPT` - Path to Python script to update

**Options:**
- `--python-version TEXT` - Python version requirement (default: `>=3.9`)

**Example:**
```bash
autopep723 add --python-version ">=3.12" script.py
```

### Global Options

#### `--version`
Display version information and exit.

#### `--help`
Show help message and exit.



## Import Name Mappings

Common mappings where import name differs from package name:

```python
PACKAGE_MAPPINGS = {
    "bs4": "beautifulsoup4",
    "PIL": "Pillow", 
    "cv2": "opencv-python",
    "yaml": "PyYAML",
    "sklearn": "scikit-learn",
    "jwt": "PyJWT",
    "dotenv": "python-dotenv",
    # ... and 35+ more
}
```

## Exit Codes

- `0` - Success
- `1` - General error (file not found, syntax error, etc.)
- `2` - Missing `uv` dependency

## Requirements

- Python 3.9+
- `uv` installed and available in PATH (for script execution)
- `rich` dependency (only runtime dependency)

## Limitations

- Only analyzes static imports (not dynamic `importlib` usage)
- Cannot detect conditional imports 
- Works only with `.py` files
- Requires `uv` for script execution mode