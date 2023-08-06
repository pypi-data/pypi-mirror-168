import typing

import aiohttp
import requests
from requests.auth import HTTPBasicAuth

class wrap_response:
    def __init__(self, response: aiohttp.ClientResponse):
        self.response = response
        
    async def json(self, loads: typing.Callable):
        return loads().decode(await self.response.content.read())
    @property
    def status(self):
        return self.response.status

class aiohttp2requests:
    def __init__(self, auth: typing.Union[tuple,aiohttp.BasicAuth]):
        self.auth = auth
    
    async def get(self, **kwargs):
        async with aiohttp.ClientSession(auth=self.auth) as session:
            async with session.get(**kwargs) as response:
                return wrap_response(response)

class Requests:
    def __init__(self, auth: typing.Union[tuple,HTTPBasicAuth,aiohttp.BasicAuth], block: bool = True,**kwargs: dict):
        if block:
            self.session = requests
            kwargs.update({"auth": auth})
        else:
            self.session = aiohttp2requests(auth)
        self.kwargs = kwargs

    def get(
        self, url: str, body: typing.Any
    ) -> typing.Union[requests.Response, aiohttp.ClientResponse]:
        return self.session.get(url, **self.kwargs, data=body)

    def post(
        self, url: str, body: typing.Any
    ) -> typing.Union[requests.Response, aiohttp.ClientResponse]:
        return self.session.post(url, **self.kwargs, data=body)

    def put(
        self, url: str, body: typing.Any
    ) -> typing.Union[requests.Response, aiohttp.ClientResponse]:
        return self.session.put(url, **self.kwargs, data=body)

    def patch(
        self, url: str, body: typing.Any
    ) -> typing.Union[requests.Response, aiohttp.ClientResponse]:
        return self.session.patch(url, **self.kwargs, data=body)

    def delete(
        self, url: str, body: typing.Any
    ) -> typing.Union[requests.Response, aiohttp.ClientResponse]:
        return self.session.delete(url, **self.kwargs, data=body)
    
    def destroy(self):
        if isinstance(self.session, aiohttp.ClientSession):
            return self.session.close()
