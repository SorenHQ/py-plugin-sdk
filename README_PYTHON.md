# Soren Python SDK

Python SDK for creating plugins that implement the Sorenv2 protocol. This SDK provides a simple way to create plugins that can be integrated with the Soren platform.

## Installation

### From Git Repository

```bash
# Install from GitHub
pip install git+https://github.com/SorenHQ/py-plugin-sdk.git

# Or from a specific branch/tag
pip install git+https://github.com/SorenHQ/py-plugin-sdk.git@main
```

### From Local Directory

```bash
cd /path/to/py-plugin-sdk
pip install -e .
```

### From PyPI (if published)

```bash
pip install soren-python-sdk
```

## Quick Start

```python
import asyncio
from pysdk import (
    NewFromEnv,
    Plugin,
    PluginIntro,
    Settings,
    Action,
    ActionFormBuilder,
    EventLogger,
    LogLevel,
)

async def main():
    # Create SDK instance
    sdk = NewFromEnv()
    await sdk.connect()
    
    # Create plugin
    plugin = Plugin(sdk)
    
    # Set intro
    plugin.set_intro(PluginIntro(
        name="My Plugin",
        version="1.0.0",
        author="Your Name"
    ))
    
    # Set settings
    plugin.set_settings(Settings(
        reply_to="settings.config.submit",
        jsonui={"type": "VerticalLayout", "elements": [...]},
        jsonschema={"type": "object", "properties": {...}}
    ), settings_handler)
    
    # Add actions
    plugin.add_actions([Action(
        method="my_action",
        title="My Action",
        form=ActionFormBuilder(
            jsonui={"type": "Control", "scope": "#/properties/param"},
            jsonschema={"properties": {"param": {"type": "string"}}}
        ),
        request_handler=action_handler
    )])
    
    # Start plugin
    await plugin.start()
    await asyncio.Event().wait()

asyncio.run(main())
```

## Environment Variables

- `AGENT_URI`: NATS server URI (e.g., `nats://localhost:4222`)
- `PLUGIN_ID`: Plugin identifier
- `SOREN_AUTH_KEY`: Authentication key
- `SOREN_EVENT_CHANNEL`: Event channel name
- `SOREN_STORE`: Store channel name

## Components

### PluginIntro
Plugin introduction with name, version, author, and optional requirements.

### Settings
Plugin settings configuration with JSONSchema and JsonUI (for jsonForm.io).

### Action
Plugin actions with form builders and request handlers.

### EventLogger
Event logging functionality for the Soren platform.

## Requirements

- Python 3.8 or higher
- NATS server running

## Example

See `main_test.py` for a complete working example.

