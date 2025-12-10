# Soren Plugin Development Template - AI Prompt

Use this template to generate a complete Soren plugin for any API integration (Jira, GitHub, Slack, etc.). This template is based on the Soren Python SDK structure.

## Plugin Structure Overview

A Soren plugin consists of:
1. **Plugin Introduction** - Name, version, author
2. **Settings** - Global configuration and credentials (stored in Soren web panel)
3. **Actions** - Operations the plugin can perform (with form parameters)
4. **Handlers** - Functions that execute when actions are triggered

## Template Code Structure

```python
"""
[PLUGIN_NAME] Plugin for Soren Platform
Example: Jira Integration Plugin, GitHub Integration Plugin, etc.
"""

import asyncio
import json
import os
import uuid
from dotenv import load_dotenv

from pysdk import (
    NewFromEnv,
    Plugin,
    PluginIntro,
    Settings,
    Action,
    ActionFormBuilder,
    Icon,
    EventLogger,
    LogLevel,
    Frame,
    JobProgress,
    Command,
)

# Global plugin instance - accessible from all handlers
# Other files can import this: from [your_file] import plugin
plugin: Plugin = None


# ============================================================================
# SETTINGS HANDLER - Manages global configuration and credentials
# ============================================================================

async def settings_update_handler(msg):
    """
    Handle settings update from Soren web panel.
    Settings are stored as global configuration for the plugin.
    This is where you save credentials, API keys, base URLs, etc.
    """
    print(f"Settings updated: {msg.data.decode()}")
    settings = json.loads(msg.data.decode())
    
    try:
        # Save settings to file or database
        # Example: Save to JSON file
        with open("plugin_settings.json", "w") as f:
            json.dump(settings, f)
        
        # Or save to environment variables
        # Or save to database
        # Or validate and store in memory
        
        await msg.respond(json.dumps({"status": "accepted"}).encode())
    except Exception as e:
        print(f"Error saving settings: {e}")
        await msg.respond(json.dumps({"status": "error", "message": str(e)}).encode())


def get_default_settings():
    """
    Load previously saved settings (credentials, config, etc.)
    This allows the plugin to remember user's configuration.
    """
    try:
        with open("plugin_settings.json", "r") as f:
            return json.load(f)
    except Exception:
        return None


# ============================================================================
# ACTION HANDLERS - Functions that execute when actions are triggered
# ============================================================================

async def action_handler_example(msg):
    """
    Handler function for an action.
    This is where you implement the actual API integration logic.
    
    Args:
        msg: NATS message containing action parameters from the form
    """
    try:
        # Parse the action parameters from the message
        action_data = json.loads(msg.data.decode())
        
        # Extract parameters (these come from the form the user filled)
        param1 = action_data.get("param1")
        param2 = action_data.get("param2")
        
        # Load settings (credentials, API keys, etc.)
        settings = get_default_settings()
        api_key = settings.get("api_key")
        base_url = settings.get("base_url")
        
        # Generate job ID for tracking
        job_id = str(uuid.uuid4())
        
        # Respond immediately with job ID
        await msg.respond(json.dumps({"jobId": job_id}).encode())
        
        # Perform the actual work (API call, processing, etc.)
        # Example: Call external API
        # result = await call_external_api(api_key, base_url, param1, param2)
        
        # Update progress (optional)
        # await plugin.progress(job_id, Command.PROGRESS, JobProgress(...))
        
        # Mark job as done
        await plugin.done(job_id, {
            "status": "success",
            "result": "Action completed successfully"
        })
        
    except Exception as e:
        print(f"Error in action_handler_example: {e}")
        await msg.respond(json.dumps({
            "error": "service unavailable",
            "message": str(e)
        }).encode())


# ============================================================================
# MAIN FUNCTION - Plugin initialization and setup
# ============================================================================

async def main():
    """Main function - Initialize plugin and connect to Soren platform"""
    
    # Load environment variables from .env file
    # These are provided by Soren web panel:
    # - AGENT_URI: NATS server URI
    # - PLUGIN_ID: Your plugin identifier
    # - SOREN_AUTH_KEY: Authentication key
    load_dotenv(".env")
    
    # Create SDK instance from environment variables
    sdk_instance = NewFromEnv()
    print(f"SDK Config - Agent URI: {sdk_instance.config.agent_uri}")
    print(f"SDK Config - Plugin ID: {sdk_instance.config.plugin_id}")
    
    # Connect to NATS
    await sdk_instance.connect()
    
    # Verify connection
    if sdk_instance.conn is None or sdk_instance.conn.is_closed or not sdk_instance.conn.is_connected:
        print("ERROR: NATS connection failed")
        return
    
    print("NATS connection verified successfully")
    
    try:
        # Set global plugin instance so handlers can access it
        global plugin
        plugin = Plugin(sdk_instance)
        
        # ====================================================================
        # 1. SET PLUGIN INTRODUCTION
        # ====================================================================
        plugin.set_intro(
            PluginIntro(
                name="[Your Plugin Name]",  # e.g., "Jira Integration"
                version="1.0.0",
                author="[Your Name/Team]",
            ),
            None,  # Optional requirements handler
        )
        
        # ====================================================================
        # 2. SET PLUGIN SETTINGS (Global Configuration & Credentials)
        # ====================================================================
        # Settings are shown in Soren web panel for users to configure
        # Use JSONSchema for validation and JsonUI (formjson.io) for UI
        
        plugin.set_settings(
            Settings(
                # Load previously saved settings (if any)
                data=get_default_settings(),
                
                # JsonUI - Defines the form layout (formjson.io format)
                # This creates the UI in Soren web panel
                jsonui={
                    "type": "VerticalLayout",
                    "elements": [
                        {
                            "type": "Control",
                            "scope": "#/properties/api_key",  # Maps to jsonschema property
                        },
                        {
                            "type": "Control",
                            "scope": "#/properties/base_url",
                        },
                        {
                            "type": "Control",
                            "scope": "#/properties/username",
                        },
                        # Add more form fields as needed
                    ],
                },
                
                # JSONSchema - Defines the data structure and validation
                # This validates the settings data
                jsonschema={
                    "type": "object",
                    "properties": {
                        "api_key": {
                            "type": "string",
                            "title": "API Key",
                            "description": "Your API key for authentication",
                            "format": "password",  # Hides input
                        },
                        "base_url": {
                            "type": "string",
                            "title": "Base URL",
                            "description": "API base URL (e.g., https://api.example.com)",
                            "format": "uri",
                        },
                        "username": {
                            "type": "string",
                            "title": "Username",
                            "description": "Your username",
                        },
                        # Add more properties as needed
                    },
                    "required": ["api_key", "base_url"],  # Required fields
                },
            ),
            settings_update_handler,  # Handler function for settings updates
        )
        
        # ====================================================================
        # 3. ADD ACTIONS (Operations the plugin can perform)
        # ====================================================================
        # Each action has:
        # - method: Unique identifier (e.g., "create.issue", "get.project")
        # - title: Display name in UI
        # - form: Parameters the user needs to provide (using formjson.io)
        # - request_handler: Function that executes when action is triggered
        
        plugin.add_actions([
            Action(
                method="create.issue",  # Unique action identifier
                title="Create Issue",   # Display name
                description="Create a new issue in the system",
                form=ActionFormBuilder(
                    # JsonUI - Form layout for action parameters
                    jsonui={
                        "type": "VerticalLayout",
                        "elements": [
                            {
                                "type": "Control",
                                "scope": "#/properties/title",
                            },
                            {
                                "type": "Control",
                                "scope": "#/properties/description",
                            },
                            {
                                "type": "Control",
                                "scope": "#/properties/priority",
                            },
                        ],
                    },
                    # JSONSchema - Parameter validation
                    jsonschema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "title": "Issue Title",
                                "description": "Enter the issue title",
                            },
                            "description": {
                                "type": "string",
                                "title": "Description",
                                "description": "Enter issue description",
                                "format": "textarea",  # Multi-line input
                            },
                            "priority": {
                                "type": "string",
                                "title": "Priority",
                                "description": "Select priority level",
                                "enum": ["low", "medium", "high", "critical"],
                                "enumNames": ["Low", "Medium", "High", "Critical"],
                            },
                        },
                        "required": ["title", "description"],
                    },
                ),
                request_handler=action_handler_example,  # Handler function
            ),
            # Add more actions as needed
            # Action(
            #     method="get.issues",
            #     title="Get Issues",
            #     form=ActionFormBuilder(...),
            #     request_handler=get_issues_handler,
            # ),
        ])
        
        # ====================================================================
        # 4. START PLUGIN
        # ====================================================================
        event = EventLogger(sdk_instance)
        await event.log("plugin-name", LogLevel.INFO, "Plugin started", None)
        
        await plugin.start()
        
        # Keep running
        await asyncio.Event().wait()
        
    finally:
        await sdk_instance.close()


if __name__ == "__main__":
    asyncio.run(main())
```

## Key Concepts

### 1. Settings (Global Configuration)
- **Purpose**: Store credentials, API keys, base URLs, and other global settings
- **Location**: Configured in Soren web panel
- **Storage**: Saved via `settings_update_handler` (to file, database, or memory)
- **Access**: Loaded via `get_default_settings()` in action handlers
- **UI**: Defined using JsonUI (formjson.io) and JSONSchema

### 2. Actions (Plugin Operations)
- **Purpose**: Define what operations your plugin can perform
- **Method**: Unique identifier (e.g., "create.issue", "jira.create.task")
- **Form**: Parameters users provide when triggering the action
- **Handler**: Function that executes the action logic

### 3. Form Parameters (formjson.io)
- **JsonUI**: Defines the form layout and UI elements
- **JSONSchema**: Defines data structure, validation, and field types
- **Types**: string, number, boolean, enum, etc.
- **Formats**: password, uri, email, textarea, etc.

### 4. Environment Variables (.env file)
Provided by Soren web panel:
```
AGENT_URI=nats://localhost:4222
PLUGIN_ID=your-plugin-id
SOREN_AUTH_KEY=your-auth-key
SOREN_EVENT_CHANNEL=events
SOREN_STORE=store
```

### 5. Handler Functions
- **Settings Handler**: Saves configuration when user updates settings
- **Action Handlers**: Execute when actions are triggered
- **Message Format**: `msg.data` contains JSON with parameters
- **Response**: Use `msg.respond()` to send immediate response
- **Job Tracking**: Use `plugin.done()` or `plugin.progress()` for async operations

## Example: Jira Integration Plugin

```python
# Settings would include:
# - jira_url: "https://your-company.atlassian.net"
# - jira_email: "user@example.com"
# - jira_api_token: "your-api-token"

# Actions would include:
# - create.issue: Create a new Jira issue
# - get.issue: Retrieve an issue by key
# - update.issue: Update an existing issue
# - search.issues: Search for issues with JQL

# Action handler example:
async def create_jira_issue_handler(msg):
    data = json.loads(msg.data.decode())
    settings = get_default_settings()
    
    # Use settings (credentials)
    jira_url = settings["jira_url"]
    api_token = settings["jira_api_token"]
    
    # Use action parameters (from form)
    title = data["title"]
    description = data["description"]
    
    # Call Jira API
    # result = await jira_api.create_issue(jira_url, api_token, title, description)
    
    job_id = str(uuid.uuid4())
    await msg.respond(json.dumps({"jobId": job_id}).encode())
    await plugin.done(job_id, {"issue_key": "PROJ-123", "status": "created"})
```

## FormJSON.io Reference

### Common Form Elements

```json
{
  "type": "VerticalLayout",  // or "HorizontalLayout"
  "elements": [
    {
      "type": "Control",
      "scope": "#/properties/field_name"
    }
  ]
}
```

### Common JSONSchema Types

```json
{
  "type": "string",
  "title": "Field Label",
  "description": "Help text",
  "format": "password|uri|email|textarea",
  "enum": ["option1", "option2"],
  "enumNames": ["Option 1", "Option 2"],
  "default": "default value"
}
```

## Development Workflow

1. **Define Settings**: What credentials/config does your plugin need?
2. **Create Actions**: What operations should your plugin perform?
3. **Design Forms**: What parameters does each action need?
4. **Implement Handlers**: Write the actual integration logic
5. **Test**: Use Soren web panel to test your plugin

## Tips

- Settings are **global** - shared across all actions
- Action parameters are **per-action** - specific to each operation
- Use `plugin.done()` for async operations that take time
- Use `plugin.progress()` to update job status
- Import plugin in other files: `from your_file import plugin` (inside functions to avoid circular imports)
- Settings handler should validate and save securely
- Action handlers should handle errors gracefully

## Complete Plugin Checklist

- [ ] Plugin introduction (name, version, author)
- [ ] Settings defined (credentials, config)
- [ ] Settings handler implemented (save/load)
- [ ] Actions defined (methods, titles, forms)
- [ ] Action handlers implemented (API integration logic)
- [ ] Forms designed (JsonUI + JSONSchema)
- [ ] Error handling in place
- [ ] Environment variables documented
- [ ] Plugin tested in Soren web panel

---

**Use this template to generate any plugin integration!** Just replace:
- `[PLUGIN_NAME]` with your plugin name
- Settings properties with your API credentials
- Actions with your API operations
- Handlers with your API integration code

