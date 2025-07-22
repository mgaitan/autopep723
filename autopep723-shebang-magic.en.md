---
title: "The magic of executable Python scripts with autopep723"
date: 2024-12-19
tags: python, uv, pep723, dependencies, automation
category: tools
slug: autopep723-shebang-magic
author: Martín Gaitán
---

Ever wished you could run a Python script without worrying about installing its dependencies first? What if I told you there's a way?

Meet [autopep723](https://github.com/mgaitan/autopep723) - a tool that brings magical dependency detection to your Python scripts.

## The problem

We've all been there. You need to hack a little piece of code, or find a useful Python script online, try to run it, and get hit with:

```
ModuleNotFoundError: No module named 'requests'
```

Then begins the dependency hunt: figuring out what packages you need, installing them, dealing with version conflicts, and cluttering your environment.

Consider this data analysis script

```python
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fetch some data and do ML analysis
response = requests.get("https://api.github.com/users/octocat")
data = pd.DataFrame([response.json()])
# ... more complex analysis ...
```

The old-school way involves setting up a virtual environment, activating it, and manually installing each dependency:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install requests pandas matplotlib seaborn scikit-learn
python script.py
```

The situation improves a lot with `uv`,

```bash
uv run --with requests --with pandas --with matplotlib --with seaborn --with scikit-learn script.py
```



As `uv` supports [script]() https://docs.astral.sh/uv/guides/scripts/

## The (magic) solution

And with `autopep723`? **Simply run the script** and let the tool figure out what it needs:

```bash
uvx autopep723 script.py
```
No dependency hunting, no package name guessing.

### autopep723 as shebang

But we can do even better. Turn any script into a self-contained executable:

```python
#!/usr/bin/env -S uvx autopep723
import requests
import pandas as pd
import matplotlib.pyplot as plt

response = requests.get("https://api.github.com/users/octocat")
data = pd.DataFrame([response.json()])
plt.plot(data)
plt.show()
```


After flagging the script executable (i.e. `chmod +x script.py`) just run `./script.py`. Dependencies are detected and installed automatically in an ephemeral environment. Share this script with anyone and it'll just work on their machine too!

## How it works

Behind the scenes, `autopep723` parses your script using AST to detect third-party imports, handles tricky cases where import names differ from package names (e.g. `import PIL` → `pillow`), then runs your script using `uv run` with automatically detected dependencies. Everything happens in a clean, ephemeral environment thanks to `uvx`'s isolation capabilities.

IMHO this approach solves several pain points that plague Python script distribution. Scripts just work out of the box with zero setup friction, while `uvx` ensures no environment pollution since dependencies are installed in isolation. Each script gets its own clean environment preventing version conflicts, making scripts truly portable without installation instructions. The speed of `uv` makes this practical for daily use rather than just a clever demo.

BTW you can also use `autopep723` to add PEP 723 metadata to existing scripts:

```bash
autopep723 add script.py  # Adds metadata to file
```

and then just use `uv run script.py`

## The future

To be honest, I would like this package to not exist, but being a built-in feature of uv.

I tweeted about this idea asking for a `--with-auto` flag that does its best attempt to satisfy missing dependencies:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">how about a --with-auto that does its best attempt to satisfy missing deps? <a href="https://t.co/yYvYXGKZnM">https://t.co/yYvYXGKZnM</a></p>&mdash; Martín Gaitán (@tin_nqn_) <a href="https://twitter.com/tin_nqn_/status/1825970796478738940?ref_src=twsrc%5Etfw">August 21, 2024</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Here is my [open proposal](https://github.com/astral-sh/uv/issues/6283). Until then, `autopep723` bridges the gap, making Python scripts as easy to run as shell scripts.
