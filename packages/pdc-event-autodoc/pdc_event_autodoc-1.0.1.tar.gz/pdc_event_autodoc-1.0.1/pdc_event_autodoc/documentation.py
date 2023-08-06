from pydantic import BaseModel, schema_of
from typing import List, Literal, Optional

from .schemas.doc_schema import MainModel

class SocketDocumentation:

    data= {
        'asyncapi': '2.2.0',
        'info': {
            'title': '',
            'version': '',
            'description': ''
        },
        'channels': {},
        'components': {
            'messages': {},
            'schemas': {}
        }
    }

    main_data= MainModel(**data)
    
    def get_channel(self, event_name: str) -> dict:
        try:
            channels= self.main_data.channels[f'{event_name}']
        except KeyError as e:
            self.main_data.channels[f'{event_name}'] = {}
            channels = self.main_data.channels[f'{event_name}']
        return channels

    def create_channels(self, operation: Literal['sub', 'pub'],
                        event_name: str, 
                        tags: Optional[List[str]] = '', 
                        summary: str = '', 
                        description: str = '') -> List[str]:
        channels= self.get_channel(event_name)
        operations_ref= []

        if 'sub' == operation:
            channels['subscribe'] = {
                'summary': summary,
                'description': description,
                'message': {
                    '$ref': '#/components/messages/'+event_name
                }
            }
            channel_tag= channels['subscribe']['tags'] = []
            for tag in tags:
                channel_tag.append({'name': tag})
            operations_ref.append(channels['subscribe']['message']['$ref'])
        else:
            channels['publish'] = {
                'summary': summary,
                'description': description,
                'message': {
                    '$ref': '#/components/messages/'+event_name
                }
            }
            channel_tag= channels['publish']['tags'] = []
            for tag in tags:
                channel_tag.append({'name': tag})
            operations_ref.append(channels['publish']['message']['$ref'])
        
        return operations_ref

    def get_message(self, message_name: str) -> dict:
        try:
            message= self.main_data.components.messages[f'{message_name}']
        except KeyError as e:
            self.main_data.components.messages[f'{message_name}'] = {}
            message = self.main_data.components.messages[f'{message_name}']
        return message

    def create_messages(self, event_name: str):
        messages_content= self.get_message(event_name)
        data_dict= {
            'payload': {}
        }
        messages_content.update(data_dict)
        messages_content['payload'] = {
            '$ref': f'#/components/schemas/{event_name}'
        }
        return messages_content    

    def get_schema(self, schema_name: str) -> dict:
        try:
            schema= self.main_data.components.schemas[f'{schema_name}']
        except KeyError as e:
            self.main_data.components.schemas[f'{schema_name}'] = {}
            schema = self.main_data.components.schemas[f'{schema_name}']
        return schema

    def parse_union_type(self, other_type= None):
        if 'definitions' in other_type:
            if '$ref' in other_type:
                schema_name= other_type['$ref'].split('/')[-1]
                other_type['$ref'] = f'#/components/schemas/{schema_name}'
                self.create_schemas(event_name= schema_name, other_type=other_type['definitions'][schema_name])
                del other_type['definitions']
            if 'anyOf' in other_type:
                for data_dict in other_type['anyOf']:
                    if data_dict == None:
                        continue
                    if '$ref' in data_dict:
                        schema_name= data_dict['$ref'].split('/')[-1]
                        data_dict['$ref'] = f'#/components/schemas/{schema_name}'
                self.create_schemas(event_name= schema_name, other_type=other_type['definitions'][schema_name])
                del other_type['definitions']
        return other_type

    def create_definitions_schema(self, schema: BaseModel = None):
        for key in schema['definitions']:
            if 'properties' in schema['definitions'][key]:
                for item in schema['definitions'][key]['properties']:
                    if 'items' in schema['definitions'][key]['properties'][item]:
                        if '$ref' in schema['definitions'][key]['properties'][item]['items']:
                            schema_name= schema['definitions'][key]['properties'][item]['items']['$ref'].split('/')[-1]
                            schema['definitions'][key]['properties'][item]['items']['$ref'] = f'#/components/schemas/{schema_name}'
                        if 'anyOf' in schema['definitions'][key]['properties'][item]:
                            for data_dict in schema['definitions'][key]['properties'][item]['anyOf']:
                                if data_dict == None:
                                    continue
                                if '$ref' in data_dict:
                                    schema_name= data_dict['$ref'].split('/')[-1]
                                    data_dict['$ref'] = f'#/components/schemas/{schema_name}'
                    if '$ref' in schema['definitions'][key]['properties'][item]:
                        schema_name= schema['definitions'][key]['properties'][item]['$ref'].split('/')[-1]
                        schema['definitions'][key]['properties'][item]['$ref'] = f'#/components/schemas/{schema_name}'
                    if 'anyOf' in schema['definitions'][key]['properties'][item]:
                        for data_dict in schema['definitions'][key]['properties'][item]['anyOf']:
                            if data_dict == None:
                                continue
                            if '$ref' in data_dict:
                                schema_name= data_dict['$ref'].split('/')[-1]
                                data_dict['$ref'] = f'#/components/schemas/{schema_name}'
            self.create_schemas(event_name= key, schema=schema['definitions'][key])
        return schema


    def check_nested_schema(self, schema_name: str = None, schema: BaseModel = None):
        if 'definitions' in schema:
            self.create_definitions_schema(schema= schema)
            if 'properties' in schema:
                for key in schema['properties']:
                    if 'items' in schema['properties'][key]:
                        if '$ref' in schema['properties'][key]['items']:
                            schema_name= schema['properties'][key]['items']['$ref'].split('/')[-1]
                            schema['properties'][key]['items']['$ref'] = f'#/components/schemas/{schema_name}'
                    if '$ref' in schema['properties'][key]:
                        schema_name= schema['properties'][key]['$ref'].split('/')[-1]
                        schema['properties'][key]['$ref'] = f'#/components/schemas/{schema_name}'
                    if 'anyOf' in schema['properties'][key]:
                        for data_dict in schema['properties'][key]['anyOf']:
                            if data_dict == None:
                                continue
                            if '$ref' in data_dict:
                                schema_name= data_dict['$ref'].split('/')[-1]
                                data_dict['$ref'] = f'#/components/schemas/{schema_name}'
                del schema['definitions']
        return schema

    def create_schemas(self, event_name: str, schema: BaseModel = None, other_type= None):
        schema_content= self.get_schema(event_name)
        try:
            if schema_content == {}:
                schema_content.update(schema)
        except:
            if schema_content == {}:
                other_type = self.parse_union_type(other_type= other_type)
                schema_content.update(other_type)
        return schema_content

    def create(self,
        event_name: str,
        operation: Literal['sub', 'pub'],
        tags: Optional[List[str]]= '',
        summary: str = '',
        description: str = ''):

        self.create_channels(operation= operation, 
            tags= tags,
            event_name= event_name, 
            summary= summary, 
            description= description)
        self.create_messages(event_name= event_name)

    def get_schema_params(self, schema: BaseModel = None):
        try:
            schema = schema.schema()
        except AttributeError:
            schema= schema_of(schema)
        return schema

    def verify_schema(self, schema: BaseModel = None, other_schema: BaseModel = None):
        schema = self.get_schema_params(schema= schema)
        other_schema = self.get_schema_params(schema= other_schema)
        if schema != other_schema:
            raise {'message': 'Schema is not same with type parameter'}
        return True

    def create_schema_from_params(self, func, event_name: str):
        keys = func.__annotations__
        for key in keys:
            schema = self.get_schema_params(keys[key])
            schema = self.check_nested_schema(schema= schema)
            self.create_schemas(event_name= event_name, other_type= schema)
            
    def schema_input(self, event_name: str = None, schema: BaseModel = None):
        schema = self.get_schema_params(schema= schema)
        schema = self.check_nested_schema(event_name, schema= schema)
        self.create_schemas(event_name= event_name, schema= schema)
        return schema

    def sub(self,
        event_name: str,
        tags: Optional[List[str]] = '',
        schema: Optional[BaseModel] = None,
        summary: Optional[str] = '',
        description: Optional[str] = ''):
        
        self.create(event_name= event_name, 
                    tags= tags,
                    operation= 'sub', 
                    summary= summary, 
                    description= description)
                    
        if schema != None:
            data_schema= self.get_schema(event_name)
            if data_schema == {}:
                self.schema_input(event_name= event_name, schema= schema)

        def decorator(func):
            schema= self.get_schema(event_name)
            if schema == {}:
                self.create_schema_from_params(func, event_name)
            return func

        return decorator
    
    def pub(self,
        event_name: str,
        tags: Optional[List[str]] = '',
        schema: Optional[BaseModel] = None,
        summary: Optional[str] = '',
        description: Optional[str] = ''):
        self.create(event_name= event_name, 
                    tags= tags,
                    operation= 'pub', 
                    summary= summary, 
                    description= description)
                    
        if schema != None:
            data_schema= self.get_schema(event_name)
            if data_schema == {}:
                self.schema_input(event_name= event_name, schema= schema)
            
        def decorator(func):
            schema= self.get_schema(event_name)
            if schema == {}:
                self.create_schema_from_params(func, event_name)
            return func

        return decorator

    def set_asyncapi_version(self, asyncapi_version: Optional[Literal['2.0.0', '2.1.0', '2.2.0', '2.3.0', '2.4.0']]):
        self.main_data.asyncapi = asyncapi_version
    
    def set_info_app(self, title: str, version: str, description: Optional[str]):
        self.main_data.info.title = title
        self.main_data.info.version = version
        self.main_data.info.description = description

    def reset_documentation(self):
        self.main_data = MainModel(**self.data)
