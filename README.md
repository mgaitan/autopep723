# autopep723

A **zero-dependency** CLI tool that dynamically generates [PEP 723](https://peps.python.org/pep-0723/) metadata for Python scripts by analyzing their imports. Forget about manually managing dependencies for simple scripts!

Simply run your script via `autopep723`:

```bash
# Run directly without installing
uvx autopep723 script.py
```

`autopep723` analyzes scripts (statically, using `ast`) to detect third-party imports and generates PEP 723 inline script metadata to pass to `uv run`.

To install it permanently:

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

**Note**: The `-S` flag is required for `env` to properly handle arguments with spaces.

## Commands

```bash
# Check what metadata would be generated
autopep723 check script.py

# Add/update PEP 723 metadata in the script
autopep723 upgrade script.py
```


## Features

- ⚡ **Zero dependencies** - uses only Python standard library
- 🪶 **Minimal footprint** - perfect as `uv run` wrapper
- 🔍 **Automatic dependency detection** via AST analysis
- ✅ **PEP 723 compliant** metadata generation

For detailed usage see the [documentation](https://autopep723.readthedocs.io/).

## License

MIT - see [LICENSE](LICENSE) file for details.
