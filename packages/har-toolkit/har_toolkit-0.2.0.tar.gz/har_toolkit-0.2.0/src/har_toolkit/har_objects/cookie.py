#!/usr/bin/env python3
from .bases import HarType


class Cookie(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.name = data["name"]
        self.value = data["value"]
        self.path = data.get("path")
        self.domain = data.get("domain")
        self.expires = data.get("expires")
        self.httpOnly = data.get("httpOnly")
        self.secure = data.get("secure")
