#!/usr/bin/env python3
from .bases import HarType
from .cookie import Cookie
from .header import Header
from .content import Content


class Response(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.status = data["status"]
        self.statusText = data["statusText"]
        self.httpVersion = data["httpVersion"]
        self.cookies = []
        for cookie in data["cookies"]:
            self.cookies.append(Cookie(cookie))
        self.headers = []
        for header in data["headers"]:
            self.headers.append(Header(header))
        self.content = Content(data["content"]) if data["content"] != {} else None
        self.redirectURL = data["redirectURL"]
        self.headersSize = data.get("headersSize", -1)
        self.bodySize = data["bodySize"]
