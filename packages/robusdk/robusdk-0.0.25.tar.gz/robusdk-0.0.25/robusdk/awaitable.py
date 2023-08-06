#!/usr/bin/env python3
# -*- coding: utf-8 -*-

async def Awaitable(task, callback=lambda *args: None):
    async for result in task():
       callback(result)
