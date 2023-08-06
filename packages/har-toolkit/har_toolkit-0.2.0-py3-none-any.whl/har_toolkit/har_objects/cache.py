#!/usr/bin/env python3
from .cache_state import CacheState
from .bases import HarType


class Cache(HarType):

    def __init__(self, data):
        super().__init__(data)
        data_keys = data.keys()
        self.beforeRequest = CacheState(data["beforeRequest"]) if "beforeRequest" in data_keys else None
        self.afterRequest = CacheState(data["afterRequest"]) if "afterRequest" in data_keys else None
