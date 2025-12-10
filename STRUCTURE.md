# Python SDK Structure

All Python-related files have been moved to the `sorenv2_py_sdk/` folder.

## Folder Structure

```
sorenv2_py_sdk/
├── pysdk/                    # Main SDK package
│   ├── __init__.py
│   ├── sorenv.py            # Core SDK with NATS connection
│   ├── plugin.py             # Plugin management
│   ├── events.py             # Event logging
│   └── models/               # Data models
│       ├── __init__.py
│       ├── models.py
│       └── types.py
├── main_test.py              # Example/test file
├── pyproject.toml            # Modern package configuration
├── setup.py                  # Legacy setup file
├── requirements.txt          # Dependencies
├── MANIFEST.in               # Package manifest
├── README.md                 # Main documentation
├── README_PYTHON.md          # Detailed Python docs
├── INSTALL.md                # Installation guide
├── PACKAGE_GUIDE.md          # Package distribution guide
└── .github/
    └── workflows/
        └── publish.yml       # GitHub Actions for PyPI

```

## Installation

### From Git
```bash
pip install git+https://github.com/SorenHQ/py-plugin-sdk.git
```

### From Local Directory
```bash
cd sorenv2_py_sdk
pip install -e .
```

## Usage

After installation, import as usual:
```python
from pysdk import Plugin, SorenSDK, NewFromEnv
```

