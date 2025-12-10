# Installation Guide for Soren Python SDK

## Install from Git Repository

### Direct Installation
```bash
pip install git+https://github.com/SorenHQ/py-plugin-sdk.git
```

### Install from Specific Branch/Tag
```bash
pip install git+https://github.com/SorenHQ/py-plugin-sdk.git@main
pip install git+https://github.com/SorenHQ/py-plugin-sdk.git@v1.0.0
```

## Install from Local Directory

### Development Installation (Editable)
```bash
cd /path/to/py-plugin-sdk
pip install -e .
```

### Regular Installation
```bash
cd /path/to/py-plugin-sdk
pip install .
```

## Build Distribution Packages

```bash
# Install build tools
pip install build wheel

# Build source distribution and wheel
python -m build

# The built packages will be in dist/
# dist/soren-python-sdk-1.0.0.tar.gz
# dist/soren_python_sdk-1.0.0-py3-none-any.whl
```

## Install from Built Wheel

```bash
pip install dist/soren_python_sdk-1.0.0-py3-none-any.whl
```

## Verify Installation

```python
python3 -c "from pysdk import Plugin, SorenSDK; print('SDK installed successfully!')"
```

## Usage After Installation

```python
from pysdk import NewFromEnv, Plugin, PluginIntro, Settings

# Your plugin code here
```

## Troubleshooting

### If installation fails:
1. Make sure you have Python 3.8 or higher
2. Ensure `setuptools`, `wheel`, and `build` are installed
3. Check that all dependencies are available (nats-py, python-dotenv)

### For development:
```bash
pip install -e ".[dev]"  # Includes dev dependencies
```
