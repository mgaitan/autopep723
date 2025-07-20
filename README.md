# autopep723

A CLI tool that automatically generates [PEP 723](https://peps.python.org/pep-0723/) metadata for Python scripts by analyzing their imports and dependencies.

## What it does

`autopep723` parses Python scripts to detect third-party package imports and generates the appropriate PEP 723 inline script metadata. This metadata allows tools like `uv run` to automatically install and manage dependencies when executing scripts.

## Installation

You can run the tool directly using `uvx`:

```bash
uvx autopep723
```

To install it permanently:

```bash
uv tool install autopep723
```

## Quick Start

```bash
# Run script with automatically detected dependencies
autopep723 script.py

# Print PEP 723 metadata to stdout  
autopep723 check script.py

# Update the script file with metadata
autopep723 upgrade script.py
```

## Shebang Integration

You can use `autopep723` directly as a shebang:

```python
#!/usr/bin/env -S uvx autopep723
import requests
import numpy as np

# Your script here...
```

**Note**: The `-S` flag is required for `env` to properly handle arguments with spaces. Without it, you'll get an error like `No such file or directory`.

This allows scripts to be executable without explicitly declaring dependencies. The tool detects imports and runs the script using `uv run` with the required packages installed on-the-fly in an ephemeral environment.

## Features

- 🔍 **Automatic dependency detection** via AST analysis
- 📦 **Import name mapping** (e.g., `import PIL` → `pillow`)  
- 🚀 **Multiple output modes** (print, update, or run)
- ✅ **PEP 723 compliant** metadata generation
- 🛡️ **Built-in module filtering** excludes standard library
- 🔧 **Graceful error handling** for syntax errors

## Documentation

For detailed usage, examples, and API reference, see the [full documentation](https://autopep723.readthedocs.io/).

## Related

- [PEP 723](https://peps.python.org/pep-0723/) - Inline script metadata specification
- [uv tools guide](https://docs.astral.sh/uv/guides/tools/) - Using uv for tool management
- [uv issue #6283](https://github.com/astral-sh/uv/issues/6283) - Autodetect dependencies mode proposal

## Contributing

Pull requests are welcome! 🎉

- **One change per PR** - Keep it focused
- **Tests required** - Maintain coverage standards  
- **Follow conventions** - Use pytest and pytest-mock
- **Be thoughtful** - This is a minimal wrapper, new dependencies need strong justification

AI assistance is encouraged (this project is ~100% AI-generated), but contributions must meet quality standards.

We follow a zero-tolerance policy for harassment of any kind. Be respectful and inclusive.

## License

MIT - see [LICENSE](LICENSE) file for details.