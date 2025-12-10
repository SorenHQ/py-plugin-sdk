# Making pysdk Installable from Git

## ✅ What's Been Set Up

1. **`pyproject.toml`** - Modern Python package configuration
2. **`setup.py`** - Legacy setup file (for compatibility)
3. **`MANIFEST.in`** - Includes necessary files in distribution
4. **`.gitignore`** - Excludes build artifacts

## 📦 Installation Methods

### 1. From Git Repository (Recommended)

```bash
# Install directly from GitHub
pip install git+https://github.com/SorenHQ/py-plugin-sdk.git

# Install from specific branch
pip install git+https://github.com/SorenHQ/py-plugin-sdk.git@main

# Install from specific tag/version
pip install git+https://github.com/SorenHQ/py-plugin-sdk.git@v1.0.0
```

### 2. From Local Directory

```bash
# Development mode (editable install)
cd /path/to/py-plugin-sdk
pip install -e .

# Regular install
cd /path/to/py-plugin-sdk
pip install .
```

### 3. Build and Install Wheel

```bash
# Build distribution packages
python -m build

# Install from wheel
pip install dist/soren_python_sdk-1.0.0-py3-none-any.whl
```

## 🔧 For Developers

### Building the Package

```bash
# Install build tools
pip install build wheel

# Build source and wheel distributions
python -m build

# Output will be in dist/ directory
```

### Testing Installation

```bash
# Test import
python3 -c "from pysdk import Plugin, SorenSDK; print('Success!')"
```

## 📝 Git Repository Setup

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add Python SDK package"
   git push origin main
   ```

2. **Tag a Release:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Users can then install:**
   ```bash
   pip install git+https://github.com/SorenHQ/py-plugin-sdk.git@v1.0.0
   ```

## 🎯 Usage After Installation

```python
# In any Python project
from pysdk import (
    NewFromEnv,
    Plugin,
    PluginIntro,
    Settings,
    Action,
    EventLogger,
    LogLevel
)

# Your plugin code here
```

## 📋 Package Structure

```
py-plugin-sdk/
├── pysdk/              # Main package
│   ├── __init__.py
│   ├── sorenv.py
│   ├── plugin.py
│   ├── events.py
│   └── models/
│       ├── __init__.py
│       ├── models.py
│       └── types.py
├── pyproject.toml      # Package configuration
├── setup.py            # Legacy setup
├── MANIFEST.in         # Include files
├── requirements.txt    # Dependencies
├── main_test.py        # Example/test file
└── README.md           # Documentation
```

## ✨ Next Steps

1. Push your code to GitHub
2. Create a release tag (e.g., `v1.0.0`)
3. Users can install with: `pip install git+https://github.com/SorenHQ/py-plugin-sdk.git`

## 🚀 Publishing to PyPI (Optional)

If you want to publish to PyPI:

1. Create account on [PyPI](https://pypi.org)
2. Get API token
3. Build and upload:
   ```bash
   python -m build
   pip install twine
   twine upload dist/*
   ```

Then users can install with:
```bash
pip install soren-python-sdk
```

