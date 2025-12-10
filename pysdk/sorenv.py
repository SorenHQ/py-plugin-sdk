"""
Core SDK for Soren v2 protocol
"""

import os
from typing import Optional
from contextlib import contextmanager
import nats
from nats.aio.client import Client as NATS


class Config:
    """Configuration for the Soren SDK"""
    
    def __init__(
        self,
        agent_uri: Optional[str] = None,
        plugin_id: Optional[str] = None,
        auth_key: Optional[str] = None,
        event_channel: Optional[str] = None,
        store_channel: Optional[str] = None,
    ):
        self.agent_uri = agent_uri or os.getenv("AGENT_URI")
        self.plugin_id = plugin_id or os.getenv("PLUGIN_ID")
        self.auth_key = auth_key or os.getenv("SOREN_AUTH_KEY")
        self.event_channel = event_channel or os.getenv("SOREN_EVENT_CHANNEL")
        self.store_channel = store_channel or os.getenv("SOREN_STORE")


class SorenSDK:
    """SorenSDK represents the main SDK instance for Soren v2 protocol"""
    
    def __init__(self, config: Config):
        if not config.agent_uri:
            raise ValueError("agent URI is required")
        if not config.plugin_id:
            raise ValueError("plugin ID is required")
        
        self.config = config
        self.conn: Optional[NATS] = None
        self._closed = False
    
    async def connect(self):
        """Connect to NATS"""
        if self.conn is None or self.conn.is_closed:
            # Ensure URI has nats:// protocol prefix
            uri = self.config.agent_uri
            if not uri.startswith(('nats://', 'tls://', 'ws://', 'wss://')):
                uri = f"nats://{uri}"
            
            print(f"Connecting to NATS at {uri}...")
            try:
                # Add connection timeout
                import asyncio
                self.conn = await asyncio.wait_for(
                    nats.connect(uri, connect_timeout=5),
                    timeout=10
                )
                if self.conn.is_connected:
                    print(f"Successfully connected to NATS at {uri}")
                else:
                    print(f"Warning: NATS connection established but not connected")
            except asyncio.TimeoutError:
                error_msg = f"Connection timeout: Failed to connect to NATS at {uri} within 10 seconds"
                print(error_msg)
                raise ConnectionError(error_msg)
            except Exception as e:
                error_msg = f"Failed to connect to NATS at {uri}: {e}"
                print(error_msg)
                raise ConnectionError(error_msg) from e
        return self.conn
    
    async def close(self):
        """Close the SDK connection and clean up resources"""
        if self.conn and not self.conn.is_closed:
            await self.conn.close()
        self._closed = True
    
    def get_connection(self) -> Optional[NATS]:
        """Get the underlying NATS connection"""
        return self.conn
    
    def get_plugin_id(self) -> str:
        """Get the plugin ID"""
        return self.config.plugin_id
    
    def make_subject(self, action: str) -> str:
        """Create a subject with the soren.v2 prefix"""
        return f"soren.v2.{self.config.plugin_id}.{action}"
    
    def make_settings_subject(self) -> str:
        """Create a subject for settings"""
        return f"soren.v2.{self.config.plugin_id}.@settings"
    
    def make_actions_list_subject(self) -> str:
        """Create a subject for actions list"""
        return f"soren.v2.{self.config.plugin_id}.@actions"
    
    def make_intro_subject(self) -> str:
        """Create a subject for intro"""
        return f"soren.v2.{self.config.plugin_id}.@intro"
    
    def make_action_cpu(self, action: str) -> str:
        """Create a subject for action execution"""
        return f"soren.cpu.{self.config.plugin_id}.{action}"
    
    def make_job_subject(self, job_id: str, job_update: str) -> str:
        """Create a subject for job updates"""
        return f"soren.cpu.{self.config.plugin_id}.{job_id}.{job_update}"
    
    def make_form_subject(self, action: str) -> str:
        """Create a subject for form requests"""
        return f"soren.v2.{self.config.plugin_id}.{action}.@form"
    
    def make_progress_subject(self, job_id: str) -> str:
        """Create a subject for progress updates"""
        return f"soren.cpu.{self.config.plugin_id}.{job_id}.*"


def NewFromEnv() -> SorenSDK:
    """Create a new Soren SDK instance using environment variables"""
    config = Config()
    return SorenSDK(config)


