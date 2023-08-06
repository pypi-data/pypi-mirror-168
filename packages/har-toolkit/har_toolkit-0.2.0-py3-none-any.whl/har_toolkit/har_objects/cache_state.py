#!/usr/bin/env python3
from .bases import HarType


class CacheState(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.expires = data.get("expires")
        self.lastAccess = data["lastAccess"]
        self.eTag = data["eTag"]
        self.hitCount = data["hitCount"]
