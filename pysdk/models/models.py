"""
Data models for Soren Python SDK
"""

from typing import Any, Callable, Dict, Optional, Union, Awaitable
from dataclasses import dataclass, field

try:
    from nats.aio.msg import Msg
except ImportError:
    # Fallback for type checking if nats is not installed
    Msg = Any

from .types import EventType, LogLevel


@dataclass
class Icon:
    """Icon representation for an action"""
    ref: str = ""
    icon: str = ""


@dataclass
class Requirements:
    """Plugin requirements configuration"""
    reply_to: str
    jsonui: Dict[str, Any]
    jsonschema: Dict[str, Any]
    handler: Optional[Callable[[Msg], Union[Any, Awaitable[Any]]]] = None


@dataclass
class PluginIntro:
    """Plugin introduction response"""
    name: str
    author: str
    version: str
    requirements: Optional[Requirements] = None


@dataclass
class ActionFormBuilder:
    """Action form configuration"""
    jsonui: Dict[str, Any]
    jsonschema: Dict[str, Any]


@dataclass
class Action:
    """Plugin action definition"""
    method: str
    title: str
    description: str = ""
    icon: Icon = field(default_factory=Icon)
    form: Optional[ActionFormBuilder] = None
    request_handler: Optional[Callable[[Msg], Union[Any, Awaitable[Any]]]] = None


@dataclass
class Settings:
    """Settings form configuration"""
    jsonui: Dict[str, Any]
    jsonschema: Dict[str, Any]
    reply_to: str = "_settings.config.submit"
    data: Optional[Dict[str, Any]] = None
    handler: Optional[Callable[[Msg], Union[Any, Awaitable[Any]]]] = None


@dataclass
class Frame:
    """Frame for job progress"""
    title: str
    content: str


@dataclass
class JobProgress:
    """Job progress update"""
    progress: int
    frame: Frame
    details: Optional[Dict[str, Any]] = None


@dataclass
class JobBodyContent:
    """Job body content"""
    job_id: str
    progress: int
    details: Optional[Dict[str, Any]] = None
    commit_on: Optional[str] = None


@dataclass
class ActionRequestContent:
    """Action request content"""
    _registry: Dict[str, Any]
    body: Dict[str, Any]


@dataclass
class PluginEvent:
    """Plugin event for logging"""
    event: EventType
    level: LogLevel
    source: str
    message: str
    timestamp: int
    details: Optional[Dict[str, Any]] = None

