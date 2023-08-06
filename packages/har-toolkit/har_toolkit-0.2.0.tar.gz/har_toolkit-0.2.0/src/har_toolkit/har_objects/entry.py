#!/usr/bin/env python3
from .bases import HarType
from .request import Request
from .response import Response
from .cache import Cache
from .timings import Timings


class Entry(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.pageref = data.get("pageref")
        self.startedDateTime = data["startedDateTime"]
        self.time = data["time"]
        self.request = Request(data["request"])
        self.response = Response(data["response"])
        self.cache = Cache(data["cache"]) if data["cache"] != {} else None
        self.timings = Timings(data["timings"]) if data["timings"] != {} else None
        self.serverIPAddress = data.get("serverIPAddress")
        self.connection = data.get("connection")
