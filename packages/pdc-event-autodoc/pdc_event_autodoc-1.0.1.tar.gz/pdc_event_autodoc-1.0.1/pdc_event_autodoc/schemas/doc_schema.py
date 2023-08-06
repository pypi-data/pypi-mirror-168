from pydantic import BaseModel
from typing import Any, List, Optional, Dict


class Info(BaseModel):
    title: str
    version: str
    description: str


class TagItems(BaseModel):
    name: str


class Operation(BaseModel):
    message: Optional[Dict[str, Any]]
    summary: Optional[str] = ''
    description: Optional[str] = ''
    tags: Optional[List[TagItems]]


class ChannelItem(BaseModel):
    subscribe: Optional[Operation] = None
    publish: Optional[Operation] = None



class ComponentMessagesItems(BaseModel):
    summary: Optional[str]
    description: Optional[str]
    payload: Optional[Dict[str, Any]]


class SchemaItems(BaseModel):
    type: Optional[str]
    properties: Optional[Dict[str, Any]]
    required: Optional[List[str]]


class Components(BaseModel):
    messages: Optional[Dict[str, ComponentMessagesItems]]
    schemas: Optional[Dict[str, SchemaItems]]


class Tags(BaseModel):
    name: str
    description: str


Channels= Optional[Dict[str, ChannelItem]]


class MainModel(BaseModel):
    asyncapi: str = '2.4.0'
    info: Optional[Info]
    channels: Channels
    components: Optional[Components]