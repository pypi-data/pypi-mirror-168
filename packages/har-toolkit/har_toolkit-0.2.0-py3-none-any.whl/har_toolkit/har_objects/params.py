#!/usr/bin/env python3
from .bases import HarType


class Params(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.name = data["name"]
        self.value = data.get("value")
        self.fileName = data.get("fileName")
        self.contentType = data.get("contentType")
