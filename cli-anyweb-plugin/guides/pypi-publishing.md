# PyPI Publishing and Installation (Phase 7)

After building and testing the CLI, make it installable and discoverable.

All cli-anyweb CLIs use **PEP 420 namespace packages** under the shared
`cli_anyweb` namespace. This allows multiple CLI packages to be installed
side-by-side in the same Python environment without conflicts.

## 1. Package Structure

```
agent-harness/
鈹溾攢鈹€ setup.py
鈹斺攢鈹€ cli_anyweb/           # NO __init__.py here (namespace package)
    鈹斺攢鈹€ <software>/         # e.g., gimp, blender, audacity
        鈹溾攢鈹€ __init__.py     # HAS __init__.py (regular sub-package)
        鈹溾攢鈹€ <software>_cli.py
        鈹溾攢鈹€ core/
        鈹溾攢鈹€ utils/
        鈹斺攢鈹€ tests/
```

The key rule: `cli_anyweb/` has **no** `__init__.py`. Each sub-package
(`gimp/`, `blender/`, etc.) **does** have `__init__.py`. This is what
enables multiple packages to contribute to the same namespace.

## 2. setup.py Template

Create `setup.py` in the `agent-harness/` directory:

```python
from setuptools import setup, find_namespace_packages

setup(
    name="cli-anyweb-<software>",
    version="1.0.0",
    packages=find_namespace_packages(include=["cli_anyweb.*"]),
    install_requires=[
        "click>=8.0.0",
        "prompt-toolkit>=3.0.0",
        # Add Python library dependencies here
    ],
    entry_points={
        "console_scripts": [
            "cli-anyweb-<software>=cli_anyweb.<software>.<software>_cli:main",
        ],
    },
    python_requires=">=3.10",
)
```

**Important details:**
- Use `find_namespace_packages`, NOT `find_packages`
- Use `include=["cli_anyweb.*"]` to scope discovery
- Entry point format: `cli_anyweb.<software>.<software>_cli:main`
- The **system package** (LibreOffice, Blender, etc.) is a **hard dependency**
  that cannot be expressed in `install_requires`. Document it in README.md and
  have the backend module raise a clear error with install instructions:
  ```python
  # In utils/<software>_backend.py
  def find_<software>():
      path = shutil.which("<software>")
      if path:
          return path
      raise RuntimeError(
          "<Software> is not installed. Install it with:\n"
          "  apt install <software>   # Debian/Ubuntu\n"
          "  brew install <software>  # macOS"
      )
  ```

## 3. Import Convention

All imports use the `cli_anyweb.<software>` prefix:

```python
from cli_anyweb.gimp.core.project import create_project
from cli_anyweb.gimp.core.session import Session
from cli_anyweb.blender.core.scene import create_scene
```

## 4. Verification Steps

**Test local installation:**
```bash
cd /root/cli-anyweb/<software>/agent-harness
pip install -e .
```

**Verify PATH installation:**
```bash
which cli-anyweb-<software>
cli-anyweb-<software> --help
```

**Run tests against the installed command:**
```bash
cd /root/cli-anyweb/<software>/agent-harness
CLI_ANYTHING_FORCE_INSTALLED=1 python3 -m pytest cli_anyweb/<software>/tests/ -v -s
```
The output must show `[_resolve_cli] Using installed command: /path/to/cli-anyweb-<software>`
confirming subprocess tests ran against the real installed binary, not a module fallback.

**Verify namespace works across packages** (when multiple CLIs installed):
```python
import cli_anyweb.gimp
import cli_anyweb.blender
# Both resolve to their respective source directories
```

## Why Namespace Packages

- Multiple CLIs coexist in the same Python environment without conflicts
- Clean, organized imports under a single `cli_anyweb` namespace
- Each CLI is independently installable/uninstallable via pip
- Agents can discover all installed CLIs via `cli_anyweb.*`
- Standard Python packaging 鈥?no hacks or workarounds

