# autopep723

A CLI tool that dynamically generates [PEP 723](https://peps.python.org/pep-0723/) metadata for Python scripts by analyzing their imports and dependencies. Just run your script with `autopep723`:

## Quick Start

```bash
# Run directly without installing
uvx autopep723 script.py

# Or install permanently
uv tool install autopep723
autopep723 script.py
```

`autopep723` analyzes Python scripts to detect third-party imports and generates PEP 723 inline script metadata. This enables tools like `uv run` to automatically install dependencies when executing scripts.

**Key Features:**
- ⚡ **Zero dependencies** - uses only Python standard library
- 🪶 **Minimal footprint** - perfect for use as a `uv run` wrapper
- 🔍 **Automatic dependency detection** via AST analysis
- ✅ **PEP 723 compliant** metadata generation

## Shebang Usage

Make your scripts executable with automatic dependency management:

```python
#!/usr/bin/env -S uvx autopep723
import requests
import numpy as np

# Your script runs with dependencies auto-installed!
```

`uvx` installs packages on-the-fly in an ephemeral environment, so no permanent installation is needed.

```{toctree}
:maxdepth: 2
:caption: Documentation

usage
examples
how-it-works
api
contributing
```

## Related Projects

- [PEP 723](https://peps.python.org/pep-0723/) - Inline script metadata specification
- [uv tools guide](https://docs.astral.sh/uv/guides/tools/) - Tool management with uv
- [uv issue #6283](https://github.com/astral-sh/uv/issues/6283) - Autodetect dependencies proposal
