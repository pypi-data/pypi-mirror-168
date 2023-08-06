from typing import Callable, Dict

import aiohttp


class Callback_Event_Listener:
    def __init__(self, callbacks: Dict[str, Callable]):
        self.callbacks = callbacks

    def get(self, key: str):
        if not key in self.callbacks.keys():
            raise KeyError(f"Key {key} not found in callbacks")
        return self.callbacks[key]

    def add(self, key: str, callback: Callable):
        if key in self.callbacks.keys():
            raise KeyError(f"Key {key} already exists in callbacks")
        self.callbacks[key] = callback


class Listener:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        host: str,
        port: int,
        callbacks: Dict[str, Callable],
        ssl: bool = False,
    ):
        raise NotImplementedError(
            "This class is not implemented yet due to SurrealDB didn't documented websocket API"
        )
        self.session = session
        self.callbacks = Callback_Event_Listener(callbacks)
        self.ws: aiohttp.ClientWebSocketResponse = None
        self.host = host
        self.port = port
        self.ssl = ssl

    async def connect(self):
        self.ws = await self.session.ws_connect(
            f"ws{'s' if self.ssl else ''}://{self.host}:{self.port}/"
        )

    async def listen(self):
        pass

    async def stop(self):
        await self.ws.close()

    async def start(self):
        await self.connect()
        await self.listen()
