#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import stdout
from logging import StreamHandler, getLogger, DEBUG, Formatter, BASIC_FORMAT

class Handler(StreamHandler):
    def __init__(self, log_level=DEBUG):
        StreamHandler.__init__(self)
        self.setFormatter(Formatter(fmt='[%(asctime)s] %(levelname)s: %(message)s'))

def Logger():
    logger = getLogger(__package__)
    logger.setLevel(DEBUG)
    logger.addHandler(Handler(stdout))
    return logger

Logger = Logger()
