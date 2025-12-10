# Soren Python SDK

Python SDK for integrating with the Soren platform, mirroring the functionality of the Go SDK.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

See `main_test.py` for a complete example of how to use the SDK.

### Basic Setup

```python
import asyncio
from pysdk import NewFromEnv, Plugin, PluginIntro, Settings, Action, ActionFormBuilder

async def main():
    # Create SDK instance from environment variables
    sdk = NewFromEnv()
    await sdk.connect()
    
    # Create plugin
    plugin = Plugin(sdk)
    
    # Set intro
    plugin.set_intro(PluginIntro(
        name="My Plugin",
        version="1.0.0",
        author="Author Name"
    ))
    
    # Set settings with JSONSchema and JsonUI (for jsonForm.io)
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

- `AGENT_URI`: NATS server URI
- `PLUGIN_ID`: Plugin identifier
- `SOREN_AUTH_KEY`: Authentication key
- `SOREN_EVENT_CHANNEL`: Event channel name
- `SOREN_STORE`: Store channel name


