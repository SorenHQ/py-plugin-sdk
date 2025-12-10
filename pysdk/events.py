"""
Event logging for Soren SDK
"""

import json
import time
from typing import Dict, Any, Optional, List

from .sorenv import SorenSDK
from .models import PluginEvent, EventType, LogLevel


class EventLogger:
    """EventLogger handles logging and event emission"""
    
    def __init__(self, sdk: SorenSDK):
        self.sdk = sdk
    
    async def log(
        self,
        source: str,
        level: LogLevel,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Send a log event to the Soren platform"""
        event = PluginEvent(
            event=EventType.LOG,
            level=level,
            source=f"{self.sdk.config.plugin_id} - {source}",
            message=message,
            timestamp=int(time.time()),
            details=details,
        )
        await self.send_event(event)
    
    async def emit_event(
        self,
        event_type: EventType,
        data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Send a custom event to the Soren platform"""
        event = PluginEvent(
            event=event_type,
            level=LogLevel.INFO,
            source=self.sdk.config.plugin_id,
            message=f"Event: {event_type.value}",
            timestamp=int(time.time()),
            details=data,
        )
        await self.send_event(event)
    
    async def send_event(self, event: PluginEvent) -> None:
        """Send an event to the Soren platform"""
        if not self.sdk.config.event_channel:
            # Event channel not configured, skip logging
            return
        
        event_dict = {
            "event": event.event.value,
            "level": event.level.value,
            "source": event.source,
            "message": event.message,
            "timestamp": event.timestamp,
        }
        if event.details:
            event_dict["details"] = event.details
        
        body = json.dumps([event_dict]).encode()
        subject = f"{self.sdk.config.event_channel}.{self.sdk.config.plugin_id}.log"
        
        headers = {}
        if self.sdk.config.auth_key:
            headers["Authorization"] = self.sdk.config.auth_key
        
        try:
            resp = await self.sdk.conn.request(subject, body, timeout=3, headers=headers if headers else None)
            
            if resp and resp.data:
                try:
                    response = json.loads(resp.data.decode())
                    if response.get("result") != "OK":
                        # Log warning but don't raise error
                        print(f"Warning: event sending response: {response.get('result')}")
                except json.JSONDecodeError:
                    # Response is not JSON, that's okay
                    pass
        except Exception as e:
            # Log error but don't raise - event logging should not break the plugin
            print(f"Warning: failed to send event: {e}")
    
    async def send_multiple_events(self, events: List[PluginEvent]) -> None:
        """Send multiple events in a single request"""
        if not self.sdk.config.event_channel:
            # Event channel not configured, skip logging
            return
        
        events_list = []
        for event in events:
            event_dict = {
                "event": event.event.value,
                "level": event.level.value,
                "source": event.source,
                "message": event.message,
                "timestamp": event.timestamp,
            }
            if event.details:
                event_dict["details"] = event.details
            events_list.append(event_dict)
        
        body = json.dumps(events_list).encode()
        subject = f"{self.sdk.config.event_channel}.{self.sdk.config.plugin_id}.log"
        
        headers = {}
        if self.sdk.config.auth_key:
            headers["Authorization"] = self.sdk.config.auth_key
        
        try:
            resp = await self.sdk.conn.request(subject, body, timeout=3, headers=headers if headers else None)
            
            if resp and resp.data:
                try:
                    response = json.loads(resp.data.decode())
                    if response.get("result") != "OK":
                        # Log warning but don't raise error
                        print(f"Warning: events sending response: {response.get('result')}")
                except json.JSONDecodeError:
                    # Response is not JSON, that's okay
                    pass
        except Exception as e:
            # Log error but don't raise - event logging should not break the plugin
            print(f"Warning: failed to send events: {e}")

