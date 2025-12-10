# Soren Python SDK (v2)

Python SDK for creating plugins that implement the Sorenv2 protocol. This SDK provides a simple way to create plugins that can be integrated with the Soren platform.

## Installation

### From Git Repository

```bash
# Install from GitHub
pip install --force-reinstall git+https://github.com/SorenHQ/py-plugin-sdk.git

# Or from a specific branch/tag
pip install --force-reinstall  git+https://github.com/SorenHQ/py-plugin-sdk.git@v0.0.6
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

- `AGENT_URI`: NATS server URI (e.g., `nats://localhost:4222` or `localhost:2022`)
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
- Soren Agent running

## Example

See `main_test.py` for a complete working example.

## Plugin Development Template

**New to plugin development?** Check out [README-VIBE-CODE.md](README-VIBE-CODE.md) - a comprehensive AI-friendly template that helps you generate complete plugins for any API integration (Jira, GitHub, Slack, etc.).

The template includes:
- **Complete code structure** - Full plugin template based on best practices
- **Settings configuration** - How to define global credentials and configuration
- **Action handlers** - Step-by-step guide for implementing plugin operations
- **FormJSON.io integration** - How to create user-friendly forms with JsonUI and JSONSchema
- **Environment setup** - Guide for using environment variables from Soren web panel
- **Real-world examples** - Jira integration example and common patterns
- **Development checklist** - Everything you need to build a complete plugin

Perfect for AI-assisted development or as a learning resource for building your first plugin!
