#!/usr/bin/env python3


class HarType:

    def __init__(self, data):
        self.comment = data.get("comment", "")

    def append_comment(self, msg):
        if self.comment:  # Empty string
            self.comment = msg
        else:
            self.comment += f"; {msg}"
        return


class VersionHarType(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.name = data["name"]
        self.version = data["version"]

    def __str__(self):
        return f"{type(self).__name__}\n\t{self.name=}\n\t{self.version=}\n\t{self.comment=}"


class SimpleHarType(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.name = data["name"]
        self.value = data["value"]

    def __str__(self):
        return f"{type(self).__name__}\n\t{self.name=}\n\t{self.value=}\n\t{self.comment=}"
