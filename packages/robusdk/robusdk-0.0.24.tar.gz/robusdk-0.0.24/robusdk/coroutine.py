#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from asyncio import wait

class Coroutine:
    def __init__(self, sequences):
        self.sequences = sequences

    def __await__(self):
        async def __await__():
            finished, _ = await wait(self.sequences)
            return [i.result() for i in finished]
        return __await__().__await__()
