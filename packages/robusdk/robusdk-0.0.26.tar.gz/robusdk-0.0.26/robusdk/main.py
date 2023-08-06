#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiohttp import ClientSession
from websockets import connect
from websockets.exceptions import ConnectionClosed
from urllib.parse import urlparse, urlunparse, urlencode
from json import loads
from .lib.digest import DigestAuth

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

def robusdk(url, username, password):
    def __init__(application, ws=False):
        if ws:
            class Client:
                async def service(self, prop):
                    try:
                        url_parts = list(urlparse(url))
                        url_parts[0] = 'ws'
                        if type(prop).__name__ == 'list':
                            url_parts[2] = f'/websocket/{application}/'
                            url_parts[4] = urlencode({'q[]': prop}, True)
                        if type(prop).__name__ == 'str':
                            url_parts[2] = f'/websocket/{application}/{prop}/'
                            url_parts[4] = urlencode({}, True)
                        async with connect(urlunparse(url_parts)) as websocket:
                            async for message in websocket:
                                yield loads(message)
                            await websocket.wait_closed()
                    except ConnectionClosed as error:
                        raise error
                    except Exception as error:
                        raise error
                async def __call__(self, prop):
                    async for message in self.service(prop):
                        yield message
                def __enter__(self):
                    return self
                def __exit__(self, *args):
                    pass
                def __getattr__(self, prop):
                    async def callable(**args):
                        async for message in self.service(prop):
                            yield message
                    return callable
            return Client()
        else:
            for case in switch(application):
                if case('rpc') or case('pipeline'):
                    class Client:
                        def __enter__(self):
                            return self
                        def __exit__(self, *args):
                            pass
                        def __getattr__(self, prop):
                            class Callable:
                                def __init__(self, *args, **kwargs):
                                    self.current = True
                                    self.args = args
                                    self.kwargs = kwargs

                                def __aiter__(self):
                                    return self

                                async def __anext__(self):
                                    while self.current:
                                        self.current = False
                                        async with ClientSession() as session:
                                            method = {
                                                'rpc': 'post',
                                                'pipeline': 'get',
                                            }[application]
                                            response = await DigestAuth(username, password, session).request(method, f'''{url}api/{application}/{prop}''', json=[*self.args, self.kwargs])
                                            if response.status == 200:
                                                return await response.json()
                                            elif response.status == 500:
                                                result = await response.json()
                                                response.reason = result.get('message')
                                                raise response.raise_for_status()
                                            else:
                                                raise response.raise_for_status()
                                    raise StopAsyncIteration
                            return Callable
                    return Client()

    return __init__
