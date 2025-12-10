"""
Type definitions for Soren Python SDK
"""

from enum import Enum


class Command(str, Enum):
    """Command types for job progress updates"""
    PROGRESS = "progress"
    STOP = "stop"
    CONTEXT_CURRENT = "context/current"
    CONTEXT_PATH = "context/path"


class EventType(str, Enum):
    """Event types for plugin events"""
    LOG = "log"


class LogLevel(str, Enum):
    """Log levels for plugin events"""
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


