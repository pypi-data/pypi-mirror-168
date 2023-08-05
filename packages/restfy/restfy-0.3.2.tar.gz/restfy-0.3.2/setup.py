# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['restfy', 'restfy.http']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'restfy',
    'version': '0.3.2',
    'description': 'A small rest framework',
    'long_description': "# restfy\nA small rest framework.\n\n[![Stable Version](https://img.shields.io/pypi/v/restfy?label=pypi)](https://pypi.org/project/restfy/)\n\n\n## Instalation\n\n```shell\npip install restfy\n```\n\n## Usage\n\n### Minimal usage\n\n```python\nfrom restfy import Application, Server\nfrom restfy.http import Response, Request\n\n\nasync def handler(request: Request) -> Response:\n    data = 'restfy'\n    return Response(data)\n\n\napp = Application()\napp.add_route('/', handler, method='GET')\n\nserver = Server(app)\nserver.run()\n\n```\n\n### Adding route by router decorator\nA route can be added by decorating handler function with .get, .post, .put, .delete or .path methods.\n```python\nfrom restfy import Application, Router, Request, Response\n\n# By using router object\nrouter = Router()\n\n@router.get('')\nasync def handler(request: Request) -> Response:\n    ret = {}\n    return Response(ret)\n\n\napp = Application()\napp.register_router('', router=router)\n\n# Or by app router decorator\n@app.post('')\nasync def other_handler(request: Request) -> Response:\n    ret = request.data\n    return Response(ret)\n\n...\n\n\n```\n\n### Receiving JSON data and args from request object\nBy default, Restfy will try to deserialize body data into request object data property by content type header information.\nYou can prefer deserialize body value manually or using dict request method. \nFor this case, it's recommended to disable the process of deserialize by parsing False to prepare_request_data in Application.\n\nThe querystring values are deserialized using args() request method. The raw querystring is on query request attribute.\n\n```python\n...\n\nfrom restfy.http import Response, Request\n\n...\n\nasync def handler(request: Request) -> Response:\n    data = request.data  # pre-deserialized body data before execute handler.\n    args = request.args()  # A dict with querystring values.\n    data = request.dict()  # Try deserialize body data in a dictionary. Recommended to use request.data instead.\n    query = request.query\n    ...\n\n```\n\n### Parsing value in url path.\n\nIf a path item is inside {}, its a variable. The handler function should have a parameter with the same name.\n\n```python\nfrom restfy import Application, Server\nfrom restfy.http import Response, Request\n\n\nasync def handler(request: Request, pk: int) -> Response:\n    data = f'restfy: pk {pk}'\n    return Response(data)\n\n\napp = Application()\napp.add_route('/{pk}', handler, method='GET')\n\n...\n```\n\n### Returning a response with custom \nBy default, the Response class set 200 as status code. \nThe content type is identified dynamically by data type. \nThese parameters may be changed instancing the response passing status, headers and content_type parameters.\n\n```python\nfrom restfy.http import Response, Request\n\n...\n\nasync def handler(request: Request, pk: int) -> Response:\n    data = f'<b>restfy: pk {pk}</b>'\n    headers = {\n        'Content-Type': 'text/html'\n    }\n    return Response(data, status=400, headers=headers)\n\n...\n\nasync def handler_other(request: Request, pk: int) -> Response:\n    data = f'<b>restfy: pk {pk}</b>'\n    return Response(data, status=400, content_type='text/html')\n\n...\n```\n\n\n\n### Middlewares\nRestfy uses middleware creating a class with .exec() method. \nThe parameter request must be passed into exec method.\n\nThe Application has the method .register_middleware() to register middlewares. \nThe register order is the same order of execution.\n\n```python\nfrom restfy import Application, Middleware\n\n\nclass DefaultMiddleware(Middleware):\n    async def exec(self, request):\n        # Do something with request object\n        ...\n        response = await self.forward(request)\n        ...\n        # Do something with response object\n        return response\n\n\napp = Application()\napp.register_middleware(DefaultMiddleware)\n\n```\n\n\n",
    'author': 'Manasses Lima',
    'author_email': 'manasseslima@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/manasseslima/restfy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
