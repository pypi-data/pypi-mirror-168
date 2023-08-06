#!/usr/bin/env python3
from .bases import HarType


class Timings(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.blocked = data.get("blocked", -1)
        self.dns = data.get("dns", -1)
        self.connect = data.get("connect", -1)
        self.send = data["send"]
        self.wait = data["wait"]
        self.receive = data["receive"]
        self.ssl = data.get("ssl", -1)
