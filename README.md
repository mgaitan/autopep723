# autopep723

[![PyPI](https://img.shields.io/pypi/v/autopep723.svg)](https://pypi.org/project/autopep723/)
[![Read the Docs](https://img.shields.io/readthedocs/autopep723)](https://autopep723.readthedocs.io/en/latest/)
[![Changelog](https://img.shields.io/github/v/release/mgaitan/autopep723?include_prereleases&label=changelog)](https://github.com/mgaitan/autopep723/releases)
[![CI](https://github.com/mgaitan/autopep723/actions/workflows/ci.yml/badge.svg)](https://github.com/mgaitan/autopep723/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/mgaitan/autopep723/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/mgaitan/autopep723/blob/main/LICENSE)


`autopep723` is a tiny wrapper on top of `uv run` that automatically manages third-party dependencies of Python scripts. Forget about manually managing dependencies for simple experiments!

## Quick Start

Run your script using third-party dependencies via `uvx autopep723`:

```bash
# Run directly without installing
uvx autopep723 script.py

# Or remote scripts directly from URLs
uvx autopep723 https://gist.githubusercontent.com/user/repo/script.py
```

To install the tool permanently:

```bash
uv tool install autopep723
autopep723 script.py
```

## Shebang Integration

You can use `autopep723` directly as a shebang:

```python
#!/usr/bin/env -S uvx autopep723
import requests
import numpy as np

# Your script here...
```


## Features

- ⚡ **Zero dependencies** - uses only Python standard library
- 🪶 **Minimal footprint** - perfect as `uv run` wrapper
- 🔍 **Automatic dependency detection** via AST analysis
- ✅ **PEP 723 compliant** metadata generation
- 🌐 **Remote script support** - run scripts directly from URLs

For detailed usage see the [documentation](https://autopep723.readthedocs.io/).

## License

MIT - see [LICENSE](LICENSE) file for details.
