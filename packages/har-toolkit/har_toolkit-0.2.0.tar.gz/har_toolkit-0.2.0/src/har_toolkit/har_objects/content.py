#!/usr/bin/env python3
from .bases import HarType
from base64 import b64decode


class Content(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.size = data.get("size")
        self.compression = data.get("compression")
        self.mimeType = data.get("mimeType")
        self.text = data.get("text")
        self.encoding = data.get("encoding")
        self.charset = self._extract_charset()

    def _extract_charset(self):
        if "; charset=" in self.mimeType:
            return self.mimeType.split("=")[-1]
        else:
            return None

    def decode(self):
        if self.encoding == "base64":
            self.text = b64decode(self.text)

        # Convert the text to utf8 bytes
        if isinstance(self.text, str):
            self.text = self.text.encode('utf8')

        return self
