"""
Example test file showing how to use the Python SDK
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
    Requirements,
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


async def settings_update_handler(msg):
    """Handle settings update"""
    print("New Update As Settings : ", msg.data.decode())
    settings = json.loads(msg.data.decode())
    
    try:
        with open("my_database.json", "w") as f:
            json.dump(settings, f)
        return {"status": "accepted"}
    except Exception as e:
        print(f"Error Writing Settings to File: {e}")
        return {"status": "not_accepted", "error": str(e)}


def get_default_settings():
    """Get default settings from my_database.json"""
    try:
        with open("my_database.json", "r") as f:
            return json.load(f)
    except Exception:
        return None


def make_enums_project():
    """Make enum list for project"""
    try:
        with open("my_database.json", "r") as f:
            saved_settings = json.load(f)
            if "project" in saved_settings:
                return [saved_settings["project"]]
    except Exception:
        pass
    return []


async def prepare_handler(msg):
    """Handle prepare action"""
    # data = msg.data
    # for example in this step we register a job in local database or external system - make a scan in Joern
    try:
        job_id = str(uuid.uuid4())
        return {"jobId": job_id}
    except Exception:
        return {"details": {"error": "service unavailable"}}


async def scan_gen_graph_handler(msg):
    """Handle scan.gen.graph action"""
    # for example in this step we register a job in local database or external system - make a scan in Joern
    try:
        job_id = str(uuid.uuid4())
        return {"jobId": job_id}
    except Exception:
        return {"details": {"error": "service unavailable"}}


async def main():
    """Main test function"""
    load_dotenv(".env")
    
    sdk_instance = NewFromEnv()
    print(f"SDK Config - Agent URI: {sdk_instance.config.agent_uri}")
    print(f"SDK Config - Plugin ID: {sdk_instance.config.plugin_id}")
    
    await sdk_instance.connect()
    
    # Verify connection
    if sdk_instance.conn is None:
        print("ERROR: NATS connection is None")
        return
    
    if sdk_instance.conn.is_closed:
        print("ERROR: NATS connection is closed")
        return
    
    if not sdk_instance.conn.is_connected:
        print("ERROR: NATS connection is not connected")
        return
    
    print("NATS connection verified successfully")
    
    try:
        plugin = Plugin(sdk_instance)
        
        plugin.set_intro(
            PluginIntro(
                name="Code Analysis Plugin",
                version="1.1.1",
                author="Soren Team",
            ),
            None,
        )
        
        plugin.set_settings(
            Settings(
    
                data=get_default_settings(),
                jsonui={
                    "type": "VerticalLayout",
                    "elements": [
                        {
                            "type": "Control",
                            "scope": "#/properties/project",
                        },
                        {
                            "type": "Control",
                            "scope": "#/properties/repository_name",
                        },
                        {
                            "type": "Control",
                            "scope": "#/properties/access_token",
                        },
                    ],
                },
                jsonschema={
                    "type": "object",
                    "properties": {
                        "project": {
                            "type": "string",
                            "title": "Your Project Name",
                            "description": "Project Name",
                        },
                        "repository_name": {
                            "type": "string",
                            "title": "Your Repository Name",
                            "description": "Github Repository name",
                        },
                        "access_token": {
                            "type": "string",
                            "title": "Fine Grained Access Token",
                            "description": "Github FineGrained Access Token",
                        },
                    },
                    "required": ["repository_name", "access_token", "project"],
                },
            ),
            settings_update_handler,
        )
        
        plugin.add_actions([
            Action(
                method="prepare",
                title="Clone/Pull Repo",
                form=ActionFormBuilder(
                    jsonui={"type": "Control", "scope": "#/properties/project"},
                    jsonschema={
                        "properties": {
                            "project": {"enum": make_enums_project()}
                        }
                    },
                ),
                request_handler=prepare_handler,
            ),
            Action(
                method="scan.gen.graph",
                title="Scan Code And Create Graph",
                form=ActionFormBuilder(
                    jsonui={"type": "Control", "scope": "#/properties/reponame"},
                    jsonschema={
                        "properties": {
                            "reponame": {"type": "string"}
                        }
                    },
                ),
                request_handler=scan_gen_graph_handler,
            ),
        ])
        
        event = EventLogger(sdk_instance)
        await event.log("remote-mate-pc", LogLevel.INFO, "start plugin", None)
        
        await plugin.start()
        
        # Keep running
        await asyncio.Event().wait()
        
    finally:
        await sdk_instance.close()


if __name__ == "__main__":
    asyncio.run(main())


