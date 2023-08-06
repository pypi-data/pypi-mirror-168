#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from asyncio import sleep, ensure_future

class Sequence:
    def __init__(self, task, onSuccess=lambda *args: None, onError=lambda *args: None, options={}):
        self.task = task
        self.onSuccess = onSuccess
        self.onError = onError
        self.repeat = options.get('repeat', 1)
        self.delay = options.get('delay', 0)
        self.results = []
        self.errors = []
    def __await__(self):
        async def __await__():
            async def futures():
                for _ in range(self.repeat):
                    try:
                        async for result in self.task():
                            self.results.append(result)
                            self.onSuccess(result)
                    except Exception as error:
                        self.errors.append(error)
                        self.onError(error)
                    await sleep(self.delay)

                if len(self.errors) > 0:
                    raise Exception(self.errors)
                else:
                    return self.results
            return await ensure_future(futures())
        return __await__().__await__()
