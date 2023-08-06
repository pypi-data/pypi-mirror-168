# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdc_event_autodoc', 'pdc_event_autodoc.schemas']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'pdc-event-autodoc',
    'version': '1.0.1',
    'description': 'Autodoc for socket',
    'long_description': "# Autodoc for Socketio and Fastapi\n\nCreate autodoc for socketio and access using API Router.\n\nUse decorator and method for describe the event running, Use sub for 'subscribe' and use pub for 'publish'.\nThis code also integrated with pydantic, so it will be detect data model in your params if using pydantic. \nBeside that other type data like array or general type like str, int, etc can be solved. \nOther type from python typing like Optional and Union especially Union with none type can be solved.\n\n\n## Example Using\n\nTo use this import the class SokcetDocumentations, and assign the class to var.\nUse decorator (@) to create documentation. There is two option to create documentation.\nFirst is class method sub to define the event under decorator is subscribe, The second is pub to define the event or method under decorator is to publish. In this bellow is example how to use the code:\n\n```\nfrom pdc_event_autodoc import SocketDocumentation \n\ndoc = SocketDocumentation()\n```\n\nFirst time is set your application info like bellow:\n```\ndoc.set_info_app(title= 'Example App', version= '1.0.0', description= 'This is example documentation of Example App version 1.0.0')\n```\n\n\n\nYou can decla your params using pydantic model:\n```\nclass PydanticModel(BaseModel):\n    id: int\n    name: str\n    address: str\n\n# Example using pydantic model\n@doc.sub(event_name= 'message', \n        tags= ['SubcribeMessage'], \n        schema= PydanticModel, \n        summary= 'ReceiveMessage', \n        description= 'This is event when we receive a message.')\n@sm.on('message')\ndef receive_message(sid, data: PydanticModel):\n    return data.dict()\n```\n\nOr using general type like \n```\n@doc.pub(event_name= 'message', \n        tags= ['PublishMessage'],\n        summary= 'To Send a Message', \n        description= 'This is event when we want to send a message.')\ndef sending_message(sid, data: str):\n    return sm.emit('message', data)\n```\n\nTo preview the documentation, you can using FastAPI or APIRouter.\nThis is an example using APIRouter:\n\n```\nfrom fastapi import APIRouter\nfrom fastapi.encoders import jsonable_encoder\nfrom pydantic import AnyHttpUrl\n\nfrom pdc_event_autodoc import SocketDocumentation, get_asyncapi_html\n\ndoc = SocketDocumentation()\n\nrouter = APIRouter(tags= ['Socket Documentations])\n\n@router.get('/socket.json')\ndef get_socket_json():\n    return jsonable_encoder(doc.main_data)\n\n@router.get('/socket_doc')\ndef get_socket_documentation():\n    async_url= AnyHttpUrl('/socket.json', scheme= 'http')\n    return get_asyncapi_html(asyncapi_url= async_url, title= 'Notification Service')\n```\nIn AnyHttpUrl if you using prefix, don't forget to include your prefix.!\n\nThe documentattion can be access in path '/socket_doc'.\n\n## Notice\n### Dont't forget to declare your type params (it can be Pydantic model, array, str, int, Optional or Union, etc).\n### If not be declare it will be detect that your function using Any params.",
    'author': 'Mukhtar',
    'author_email': 'mukhtar.syariefudin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
