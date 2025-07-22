# Examples

This section demonstrates `autopep723` usage with real examples from the project.

## Simple Demo (No Dependencies)

A basic script that uses only built-in Python modules:

```{literalinclude} examples/simple_demo.py
:language: python
:linenos:
```

**Usage:**
```bash
# Check what dependencies would be detected (should be empty)
autopep723 check examples/simple_demo.py

# Run the script
autopep723 examples/simple_demo.py
```

## Web Scraper

A script that uses external packages (`requests` and `beautifulsoup4`):

```{literalinclude} examples/web_scraper.py
:language: python
:linenos:
```

**Usage:**
```bash
# Check detected dependencies
autopep723 check examples/web_scraper.py

# Update file with PEP 723 metadata
autopep723 add examples/web_scraper.py

# Run with automatic dependency management
autopep723 examples/web_scraper.py
```

**Expected dependencies:**
- `requests` - HTTP library
- `beautifulsoup4` - HTML parsing (from `bs4` import)

## Shebang Example

Demonstrates using `autopep723` as a shebang for executable scripts:

```{literalinclude} examples/shebang_example.py
:language: python
:linenos:
```

**Usage:**
```bash
# Make executable and run directly
chmod +x examples/shebang_example.py
./examples/shebang_example.py
```

The shebang `#!/usr/bin/env autopep723` automatically:
1. Detects the `requests` dependency
2. Creates an isolated environment
3. Installs required packages
4. Executes the script

For `uvx` usage, change the shebang to:
```python
#!/usr/bin/env -S uvx autopep723
```

## Machine Learning Analysis

A comprehensive data science script with multiple dependencies:

```{literalinclude} examples/ml_analysis.py
:language: python
:linenos:
:lines: 1-20
```

This example already includes PEP 723 metadata and demonstrates:
- Data generation and exploration
- Visualization with matplotlib/seaborn
- Machine learning with scikit-learn
- Data manipulation with pandas

**Usage:**
```bash
# Run the complete analysis
autopep723 examples/ml_analysis.py
```

**Dependencies included:**
- `matplotlib` - Plotting library
- `pandas` - Data manipulation
- `scikit-learn` - Machine learning (from `sklearn` import)
- `seaborn` - Statistical visualization

## Import Name Mappings

These examples showcase how `autopep723` handles import name mappings:

| Script Import | Detected Package | Reason |
|---------------|------------------|---------|
| `from bs4 import BeautifulSoup` | `beautifulsoup4` | Import name differs from package |
| `from sklearn import datasets` | `scikit-learn` | Common alias mapping |
| `import requests` | `requests` | Direct mapping |
| `import matplotlib.pyplot` | `matplotlib` | Top-level package detection |

## Testing the Examples

Run all examples to see `autopep723` in action:

```bash
# Check all examples
for script in examples/*.py; do
    echo "=== $script ==="
    autopep723 check "$script"
    echo
done

# Run all examples (be patient with ML example!)
for script in examples/*.py; do
    echo "Running $script..."
    autopep723 "$script"
done
```

## Creating Your Own Scripts

Based on these examples, follow this pattern:

1. **Write your script** with normal import statements
2. **Test detection**: `autopep723 check script.py`
3. **Add metadata**: `autopep723 add script.py`
4. **Make executable** (optional): Add shebang and `chmod +x`

The tool handles the complexity of dependency management automatically!