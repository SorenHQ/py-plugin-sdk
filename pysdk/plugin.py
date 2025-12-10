"""
Plugin management for Soren SDK
"""

import json
import logging
from typing import List, Optional, Callable, Any, Dict
import asyncio

from nats.errors import NoRespondersError

from .sorenv import SorenSDK
from .models import PluginIntro, Settings, Action, Command, JobProgress, Frame

logger = logging.getLogger("SOREN-SDK")


class Plugin:
    """Plugin represents a Soren plugin instance"""
    
    def __init__(self, sdk: SorenSDK):
        logging.basicConfig(level=logging.INFO)
        self.sdk = sdk
        self.intro: Optional[PluginIntro] = None
        self.settings: Optional[Settings] = None
        self.actions: List[Action] = []
    
    def set_intro(
        self,
        intro: PluginIntro,
        handler: Optional[Callable[[Any], Any]] = None
    ):
        """Set the plugin introduction"""
        self.intro = intro
        if self.intro.requirements and handler:
            self.intro.requirements.handler = handler
    
    def set_settings(
        self,
        settings: Settings,
        handler: Optional[Callable[[Any], Any]] = None
    ):
        """Set the plugin settings"""
        self.settings = settings
        if handler:
            self.settings.handler = handler
    
    def set_actions(self, actions: List[Action]):
        """Set the plugin actions"""
        self.actions = actions
    
    def add_actions(self, actions: List[Action]):
        """Add actions to the plugin"""
        self.actions.extend(actions)
    
    async def start(self):
        """Start the plugin and register all handlers"""
        await self.intro_handler()
        await self.settings_handler()
        await self.actions_handler()
        logger.info(f"Plugin started: {self.intro.name if self.intro else 'Unknown'}")
    
    async def intro_handler(self):
        """Handle intro requests"""
        if not self.intro:
            return
        
        subject = self.sdk.make_intro_subject()
        
        async def intro_callback(msg):
            intro_dict = {
                "name": self.intro.name,
                "author": self.intro.author,
                "version": self.intro.version,
            }
            if self.intro.requirements:
                intro_dict["requirements"] = {
                    "replyTo": self.intro.requirements.reply_to,
                    "jsonui": self.intro.requirements.jsonui,
                    "jsonschema": self.intro.requirements.jsonschema,
                }
            
            intro_bytes = json.dumps(intro_dict).encode()
            await msg.respond(intro_bytes)
        
        async def msg_handler(msg):
            await intro_callback(msg)
        
        sub = await self.sdk.conn.subscribe(subject, cb=msg_handler)
        logger.info(f"Subscribed to intro: {subject}")
        
        # Handle requirements if present
        if self.intro.requirements and self.intro.requirements.reply_to:
            req_subject = self.sdk.make_subject(self.intro.requirements.reply_to)
            
            async def req_callback(msg):
                if self.intro.requirements.handler:
                    result = self.intro.requirements.handler(msg)
                    if result:
                        if asyncio.iscoroutine(result):
                            result = await result
                        result_bytes = json.dumps(result).encode() if isinstance(result, dict) else str(result).encode()
                        await msg.respond(result_bytes)
                else:
                    await msg.respond(b'{"status":"not implemented"}')
            
            async def req_msg_handler(msg):
                await req_callback(msg)
            
            await self.sdk.conn.subscribe(req_subject, cb=req_msg_handler)
            logger.info(f"Subscribed to requirements: {req_subject}")
    
    async def settings_handler(self):
        """Handle settings requests"""
        # Show settings form handler
        subject = self.sdk.make_settings_subject()
        
        async def settings_callback(msg):
            logger.info("Settings Called")
            if not self.settings:
                await msg.respond(b"null")
                return
            
            # Use default reply_to if empty or not set
            reply_to = self.settings.reply_to if self.settings.reply_to else "_settings.config.submit"
            
            settings_dict = {
                "replyTo": reply_to,
                "jsonui": self.settings.jsonui,
                "jsonschema": self.settings.jsonschema,
            }
            if self.settings.data:
                settings_dict["data"] = self.settings.data
            
            settings_bytes = json.dumps(settings_dict).encode()
            await msg.respond(settings_bytes)
        
        async def settings_msg_handler(msg):
            await settings_callback(msg)
        
        await self.sdk.conn.subscribe(subject, cb=settings_msg_handler)
        logger.info(f"Subscribed to settings: {subject}")
        
        # Settings submit handler
        if self.settings:
            # Use default reply_to if empty or not set
            reply_to = self.settings.reply_to if self.settings.reply_to else "_settings.config.submit"
            submit_subject = self.sdk.make_subject(reply_to)
            
            async def submit_callback(msg):
                if self.settings.handler:
                    result = self.settings.handler(msg)
                    if result:
                        if asyncio.iscoroutine(result):
                            result = await result
                        result_bytes = json.dumps(result).encode() if isinstance(result, dict) else str(result).encode()
                        await msg.respond(result_bytes)
                else:
                    await msg.respond(b'{"status":"not implemented"}')
            
            async def submit_msg_handler(msg):
                await submit_callback(msg)
            
            await self.sdk.conn.subscribe(submit_subject, cb=submit_msg_handler)
            logger.info(f"Subscribed to settings submit: {submit_subject}")
    
    async def actions_handler(self):
        """Handle actions requests"""
        # Actions list handler
        list_subject = self.sdk.make_actions_list_subject()
        
        async def list_callback(msg):
            actions_list = []
            for action in self.actions:
                action_dict = {
                    "method": action.method,
                    "title": action.title,
                    "description": action.description,
                    "icon": {
                        "ref": action.icon.ref,
                        "icon": action.icon.icon,
                    },
                }
                actions_list.append(action_dict)
            
            list_bytes = json.dumps(actions_list).encode()
            await msg.respond(list_bytes)
        
        async def list_msg_handler(msg):
            await list_callback(msg)
        
        await self.sdk.conn.subscribe(list_subject, cb=list_msg_handler)
        logger.info(f"Subscribed to actions list: {list_subject}")
        
        # Individual action handlers
        for action in self.actions:
            # Form handler
            form_subject = self.sdk.make_form_subject(action.method)
            
            async def form_callback(msg, act=action):
                if not act.form:
                    await msg.respond(b"{}")
                    return
                
                form_dict = {
                    "jsonui": act.form.jsonui,
                    "jsonschema": act.form.jsonschema,
                }
                form_bytes = json.dumps(form_dict).encode()
                await msg.respond(form_bytes)
            
            async def form_msg_handler(msg, act=action):
                await form_callback(msg, act)
            
            await self.sdk.conn.subscribe(form_subject, cb=form_msg_handler)
            logger.info(f"Form Builder Service: {form_subject}")
            
            # Request handler
            cpu_subject = self.sdk.make_action_cpu(action.method)
            
            async def request_callback(msg, act=action):
                if act.request_handler:
                    result = act.request_handler(msg)
                    if result:
                        if asyncio.iscoroutine(result):
                            result = await result
                        result_bytes = json.dumps(result).encode() if isinstance(result, dict) else str(result).encode()
                        await msg.respond(result_bytes)
            
            async def request_msg_handler(msg, act=action):
                await request_callback(msg, act)
            
            await self.sdk.conn.subscribe(cpu_subject, cb=request_msg_handler)
            logger.info(f"Subscribed Action: {cpu_subject}")
            
    async def done(self, job_id :str ,data :Dict[str, Any]) -> Any:
        return await self.progress(job_id,Command.PROGRESS,JobProgress(progress=100,frame=Frame(title="Completed", content="Job completed successfully"),details=data))
        
    async def progress(
        self,
        job_id: str,
        command: Command,
        data: JobProgress
    ) -> Any:
        """Send progress update for a job"""
        sub = self.sdk.make_job_subject(job_id, command.value)
        
        data_dict = {
            "progress": data.progress,
            "frame": {
                "title": data.frame.title,
                "content": data.frame.content,
            },
        }
        if data.details:
            data_dict["details"] = data.details
        
        data_bytes = json.dumps(data_dict).encode()
        max_retries = 3
        for attempt in range(max_retries):
            try:
                msg = await self.sdk.conn.request(sub, data_bytes, timeout=3)
                await self.sdk.conn.flush()
                logger.info(f"Progress sent: {msg.data.decode() if msg.data else 'No response'}")
                return msg
            except NoRespondersError as e:
                if attempt < max_retries - 1:
                    # Only log on retries, not on the first attempt failure (attempt 0)
                    # attempt 0 = first try (no log), attempt 1+ = retries (log)
                    if attempt >= 1:
                        logger.warning(f"Progress command {command} no responder error (retry {attempt}/{max_retries - 1}): {e}. Retrying in 1 second...")
                    await asyncio.sleep(1)
                    continue
                else:
                    logger.error(f"Progress command {command} no responder error after {max_retries} attempts: {e}")
                    return e
            except Exception as e:
                logger.error(f"Progress command {command} error: {e}")
                return e
