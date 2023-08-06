
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


class HTTPError(Exception):
    def __init__(self, status_code, message):
        """Raise HTTP Errors.

        Args:
            status_code (int): Status Code
            message (str): Message to show
        """
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

import enum

import yarl
try:
    import orjson as json  # SPEED
except ImportError:
    import json


class Status(enum.Enum):
    OK = "OK"
    ERR = "ERR"

class decoder:
    def __init__(self, **kwargs):
        pass
    def decode(self, json_string:str):
        return json.loads(json_string)

class Result:
    """
    A result class that contains data that API returns
    """
    def __init__(self, data: list, status_code: int):
        data: dict = data[0]
        self.time = data.get("time")
        self.status_code = status_code
        if data.get("status", None) is not None:
            self.status = Status(data["status"])
        else:
            raise HTTPError(
                status_code,
                "Server Errors Out"
                f"\nStatus Code: {status_code}"
                f"\nError message: {data.get('information', data.get('detail', data))}"
                f"\nDetailed Message: {data.get('description',None)}"
            )
        self.result = data.get("result", None)

    def __repr__(self) -> str:
        return f"<surreal.client.Result status={self.status} status_code={self.status_code}>"

    def __str__(self) -> str:
        return self.__repr__()


class Base:
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        db: str,
        namespace: str,
        block: bool = True,
    ) -> None:
        """Initialize the client.

        Args:
            host (str): A full host URI (https://example.com:69420)
            username (str): The username to use for authentication
            password (str): The password to use for authentication
            db (str): The database to use
            namespace (str): The namespace to use
            block (bool, optional): Blocking or Asynchronous. Defaults to True. Usually ignore this since it's for class to subclass it.
        """
        self.username = username
        self.password = password
        self.block = block
        self.session = Requests(
            block=block,
            headers={
                "DB": db,
                "NS": namespace,
                "Content-Type": "application/json",
            },
            auth=aiohttp.BasicAuth(username,password) if not block else HTTPBasicAuth(username, password)
        )
        self.host = yarl.URL(host)
    
    def __repl__(self):
        return f"<{'AsyncSurrealDB' if not self.block else 'SurrealDB'} host={self.host} username={self.username} session={self.session}"
    
    def __str__(self):
        return self.__repl__()

class AsyncSurrealDB(Base):
    """
    Asynchronously connect/fetch and execute from SurrealDB with the HTTP API.
    """
    def __init__(
        self, host: str, username: str, password: str, db: str, namespace: str
    ):
        super().__init__(host, username, password, db, namespace, block=False)

    async def execute(self, sql: str) -> Result:
        """Execute a SurrealQL statement.

        Args:
            sql (str): The SurrealQL statement to execute
        """
        res: aiohttp.ClientResponse = await self.session.post(
            self.host / "sql", sql
        )
        return Result(await res.json(loads=decoder), res.status)

    async def fetch(self, sql: str) -> Result:
        res: aiohttp.ClientResponse = await self.session.post(
            self.host / "sql", sql
        )
        return Result(await res.json(loads=decoder), res.status)


class SurrealDB(Base):
    """
    Synchronously connect/fetch and execute from SurrealDB with the HTTP API.
    """
    def __init__(
        self, host: str, username: str, password: str, db: str, namespace: str
    ):
        super().__init__(host, username, password, db, namespace, block=True)

    def execute(self, sql: str) -> Result:
        """Execute a SurrealQL statement.

        Args:
            sql (str): The SurrealQL statement to execute
        """
        res: requests.Response = self.session.post(self.host / "sql", sql)
        return Result(res.json(cls=decoder), res.status_code)

    def fetch(self, sql: str) -> Result:
        """Fetch data

        Args:
            sql (str): The SurrealQL statement to execute

        Returns:
            typing.List[typing.Dict[str, typing.Any]]: A
        """
        res: requests.Response = self.session.post(self.host / "sql", sql)
        return Result(res.json(cls=decoder), res.status)
