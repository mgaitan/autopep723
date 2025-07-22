# autopep723


[![PyPI](https://img.shields.io/pypi/v/autopep723.svg)](https://pypi.org/project/autopep723/)
[![Changelog](https://img.shields.io/github/v/release/mgaitan/autopep723?include_prereleases&label=changelog)](https://github.com/mgaitan/autopep723/releases)
[![CI](https://github.com/mgaitan/honeycomb-cleaner/actions/workflows/ci.yml/badge.svg)](https://github.com/mgaitan/honeycomb-cleaner/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/mgaitan/honeycomb-cleaner/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/mgaitan/autopep723/blob/main/LICENSE)


A **zero-dependency** CLI tool that dynamically generates [PEP 723](https://peps.python.org/pep-0723/) metadata for Python scripts by analyzing their imports. Forget about manually managing dependencies for simple scripts!

Simply run your script via `autopep723`:

```bash
# Run directly without installing
uvx autopep723 script.py

# Run remote scripts directly from URLs
uvx autopep723 https://gist.githubusercontent.com/user/repo/script.py
```

`autopep723` analyzes scripts (statically, using `ast`) to detect third-party imports and generates PEP 723 inline script metadata to pass to `uv run`.

To install it permanently:

```bash
uv tool install autopep723
autopep723 script.py

# Works with remote scripts too
autopep723 https://gist.githubusercontent.com/mgaitan/8fb70482b46454cc22cb6f2417afb8ea/raw/757a8a27b96ed17fde37cc908d07a2c471937b3c/autopep723_example.py
```

## Shebang Integration

You can use `autopep723` directly as a shebang:

```python
#!/usr/bin/env -S uvx autopep723
import requests
import numpy as np

# Your script here...
```


## Commands

```bash
# Add/update PEP 723 metadata in the script
autopep723 add script.py

# Check what metadata would be generated
autopep723 check script.py

# Works with remote scripts (downloads to temp file)
autopep723 check https://example.com/script.py

# Use verbose mode to see detailed progress
autopep723 -v script.py
autopep723 check -v script.py
autopep723 add -v script.py
autopep723 add https://example.com/script.py  # Note: updates local temp file only

# Run remote scripts directly
autopep723 https://raw.githubusercontent.com/user/repo/script.py
```

The `add` command is analogous to `uv add --script script.py 'dep1' 'dep2'`, but with automatic dependency detection - you don't need to manually specify which packages to add.

## Remote Scripts

`autopep723` can download and execute Python scripts directly from URLs, just like `uv run` does:

```bash
# Download and run a remote script with automatic dependency detection
autopep723 https://gist.githubusercontent.com/user/repo/script.py

# Check what dependencies would be detected for a remote script
autopep723 check https://example.com/script.py
```

When working with remote scripts:
- Scripts are downloaded to temporary files in `/tmp`
- All dependency detection works the same as with local files
- The `add` command works but only updates the temporary local copy
- Supports any URL that returns a Python script (GitHub raw, gists, etc.)


## Features

- ⚡ **Zero dependencies** - uses only Python standard library
- 🪶 **Minimal footprint** - perfect as `uv run` wrapper
- 🔍 **Automatic dependency detection** via AST analysis
- ✅ **PEP 723 compliant** metadata generation
- 🌐 **Remote script support** - run scripts directly from URLs

For detailed usage see the [documentation](https://autopep723.readthedocs.io/).

## License

MIT - see [LICENSE](LICENSE) file for details.
