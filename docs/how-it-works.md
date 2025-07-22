# How It Works

This section explains the internal mechanics of `autopep723` and how the different execution modes function.

## Overview

`autopep723` analyzes Python scripts using Abstract Syntax Tree (AST) parsing to detect third-party imports, then either generates PEP 723 metadata or executes the script with automatic dependency management.

## Execution Flow

```{mermaid}
flowchart TD
    A[User runs: uvx autopep723 script.py] --> B{uvx available?}
    B -->|No| C[Error: Install uv]
    B -->|Yes| D[uvx creates ephemeral venv]
    D --> E[uvx installs autopep723 in venv]
    E --> F[autopep723 starts execution]
    F --> G{Script exists?}
    G -->|No| H[Error: File not found]
    G -->|Yes| I[Read script content]
    I --> J{Has PEP 723 metadata?}
    J -->|Yes| K[Extract existing dependencies]
    J -->|No| L[Parse with AST]
    L --> M[Extract import statements]
    M --> N[Filter stdlib modules]
    N --> O[Map import names to packages]
    O --> P[Generate dependency list]
    K --> Q[uv run --with deps script.py]
    P --> Q
    Q --> R[Script executes with dependencies]
    R --> S[Clean up ephemeral venv]
```

## Mode-Specific Behavior

### Run Mode (Default)

When you execute `autopep723 script.py`:

1. **Script Analysis**: Parses the Python file using AST
2. **Dependency Detection**: Identifies third-party imports
3. **Execution**: Runs `uv run --with <deps> script.py`

### Check Mode

When you execute `autopep723 check script.py`:

1. **Script Analysis**: Same parsing process
2. **Metadata Generation**: Creates PEP 723 format
3. **Output**: Prints metadata to stdout (no execution)

### Add Mode

When you execute `autopep723 add script.py`:

1. **Script Analysis**: Same parsing process
2. **File Modification**: Adds metadata block to top of file
3. **Safety Check**: Skips if metadata already exists

## Import Analysis Process

```{mermaid}
flowchart LR
    A[Python Script] --> B[AST Parser]
    B --> C[Extract Imports]
    C --> D{Import Type}
    D -->|import module| E[Direct Import]
    D -->|from module import| F[From Import]
    E --> G[Module Name]
    F --> G
    G --> H{Standard Library?}
    H -->|Yes| I[Skip]
    H -->|No| J{In Mapping Table?}
    J -->|Yes| K[Use Mapped Name]
    J -->|No| L[Use Original Name]
    K --> M[Final Package List]
    L --> M
    I --> N[End]
```

## Import Name Mapping

The tool maintains a mapping table for packages where the import name differs from the package name:

```python
# Examples from the mapping table
"bs4": "beautifulsoup4",
"PIL": "Pillow", 
"cv2": "opencv-python",
"sklearn": "scikit-learn"
```

This handles the common discrepancy between `pip install package-name` and `import module_name`.

## uvx Integration

### What uvx Does

When you run `uvx autopep723`:

1. **Environment Creation**: Creates a temporary virtual environment
2. **Tool Installation**: Installs `autopep723` and its dependencies (`rich`)
3. **Execution**: Runs the tool in the isolated environment
4. **Cleanup**: Removes the environment after execution

### Why This Works

- ✅ **No system pollution**: Tools don't interfere with system Python
- ✅ **Dependency isolation**: Each execution is clean
- ✅ **Always fresh**: Latest version of the tool
- ✅ **No conflicts**: No dependency version conflicts

## Shebang Mechanics

### Unix/Linux/macOS

The shebang `#!/usr/bin/env -S uvx autopep723` works by:

1. **Shell interpretation**: Shell reads the shebang line
2. **Command execution**: Runs `uvx autopep723 script.py`
3. **File as argument**: The script file becomes the argument

**Note**: The `-S` flag is required for `env` to properly handle arguments with spaces. This flag is available in most modern Unix systems (GNU coreutils 8.30+, macOS 10.15+). For older systems, consider using permanent installation with `uv tool install autopep723` and the simpler shebang `#!/usr/bin/env autopep723`.

### Windows Compatibility

**Traditional shebangs don't work on Windows**, but there are alternatives:

#### Option 1: Python Launcher (py.exe)

Windows Python installations include `py.exe` which can handle shebangs:

```python
#!python
# /// script
# dependencies = ["requests"]
# ///
import subprocess
import sys

# Run through autopep723
subprocess.run([sys.executable, "-m", "uvx", "autopep723", __file__])
```

#### Option 2: Batch File Wrapper

Create `script.bat`:

```batch
@echo off
uvx autopep723 %~dp0script.py
```

#### Option 3: PowerShell Script

Create `script.ps1`:

```powershell
uvx autopep723 "$PSScriptRoot\script.py"
```

#### Best Practice for Cross-Platform

For maximum compatibility, use explicit execution rather than shebangs:

```bash
# Unix/Linux/macOS
uvx autopep723 script.py

# Windows (same command)
uvx autopep723 script.py
```

## Error Handling Flow

```{mermaid}
flowchart TD
    A[Start] --> B{File exists?}
    B -->|No| C[FileNotFoundError]
    B -->|Yes| D{Valid Python syntax?}
    D -->|No| E[Return empty deps]
    D -->|Yes| F{uv available?}
    F -->|No| G[Installation error]
    F -->|Yes| H[Process normally]
    C --> I[Exit code 1]
    E --> J[Continue with empty list]
    G --> K[Exit code 2]
    H --> L[Success]
```

## Performance Characteristics

### Analysis Speed
- **AST parsing**: ~1-5ms for typical scripts
- **Import detection**: Linear with number of imports
- **No network calls**: All analysis is local and fast

### Memory Footprint
- **Minimal usage**: Processes one script at a time
- **No persistent state**: Each run is independent
- **Clean execution**: No background processes

### Caching Strategy
- **No caching**: Each execution analyzes fresh
- **Intentional design**: Ensures accuracy over speed
- **Fast enough**: Analysis is already very fast

## Integration Points

### With uv
`autopep723` leverages `uv`'s capabilities:
- Fast dependency resolution
- Isolated execution environments
- Cross-platform compatibility

### With PEP 723
Generates compliant metadata:
- Proper TOML format in comments
- Standard field names (`requires-python`, `dependencies`)
- Tool-agnostic specification

### With Python Ecosystem
Works with standard tools:
- AST module for parsing
- Standard library for most functionality
- Minimal external dependencies