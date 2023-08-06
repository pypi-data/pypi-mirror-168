#!/usr/bin/env python3
from .bases import HarType


class PageTimings(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.onContentLoad = data.get("onContentLoad", -1)
        self.onLoad = data.get("onLoad", -1)
