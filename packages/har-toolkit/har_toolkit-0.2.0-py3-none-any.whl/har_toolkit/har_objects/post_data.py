#!/usr/bin/env python3
from .bases import HarType
from .params import Params


class PostData(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.mimeType = data["mimeType"]
        self.params = []
        if "params" in data.keys():
            for param in data["params"]:
                Params(param)
        self.text = data["text"] if "text" in data.keys() else None
