#!/usr/bin/env python3
from .bases import HarType
from .cookie import Cookie
from .header import Header
from .post_data import PostData
from urllib.parse import urlparse


class Request(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.method = data["method"]
        self.url = data["url"]
        self.httpVersion = data["httpVersion"]
        self.cookies = []
        if "cookies" in data.keys():
            for cookie in data["cookies"]:
                self.cookies.append(Cookie(cookie))
        self.headers = []
        if "headers" in data.keys():
            for header in data["headers"]:
                self.headers.append(Header(header))
        self.queryString = []
        if "queryString" in data.keys():
            for query in data["queryString"]:
                self.queryString.append(query)
        self.postData = PostData(data["postData"]) if "postData" in data.keys() else None
        self.headersSize = data["headersSize"]
        self.bodySize = data["bodySize"]

    def parse_url(self):
        """Helper method to call urllib3.parse.urlparse on the request URL."""
        return urlparse(self.url)
