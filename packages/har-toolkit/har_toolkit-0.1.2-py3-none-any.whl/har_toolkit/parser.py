#!/usr/bin/env python3
# parser.py - A HAR (HTTP Archive) parser
# Copyright (C) 2022  Mason Weaver <mason@swingproxy.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
from base64 import b64decode
from urllib.parse import urlparse


class HarParsingError(BaseException):
    pass


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


class Creator(VersionHarType):
    pass


class Browser(VersionHarType):
    pass


class Page(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.startedDateTime = data["startedDateTime"]
        self.id = data["id"]
        self.title = data["title"]
        self.pageTimings = PageTimings(data["pageTimings"]) if data["pageTimings"] != {} else None

    def __str__(self):
        return f"""Page\n\t{self.startedDateTime=}\n\t{self.id=}\n\t{self.title=}\n\t{self.pageTimings=}\n\t{self.comment=}"""


class PageTimings(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.onContentLoad = data.get("onContentLoad", -1)
        self.onLoad = data.get("onLoad", -1)


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


class CacheState(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.expires = data.get("expires")
        self.lastAccess = data["lastAccess"]
        self.eTag = data["eTag"]
        self.hitCount = data["hitCount"]


class Cache(HarType):

    def __init__(self, data):
        super().__init__(data)
        data_keys = data.keys()
        self.beforeRequest = CacheState(data["beforeRequest"]) if "beforeRequest" in data_keys else None
        self.afterRequest = CacheState(data["afterRequest"]) if "afterRequest" in data_keys else None


class Entry(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.pageref = data.get("pageref")
        self.startedDateTime = data["startedDateTime"]
        self.time = data["time"]
        self.request = Request(data["request"])
        self.response = Response(data["response"])
        self.cache = Cache(data["cache"]) if data["cache"] != {} else None
        self.timings = Timings(data["timings"]) if data["timings"] != {} else None
        self.serverIPAddress = data.get("serverIPAddress")
        self.connection = data.get("connection")


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


class Header(SimpleHarType):
    pass


class queryString(SimpleHarType):
    pass


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
        else:
            # Nothing to decode
            pass
        return self


class PostData(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.mimeType = data["mimeType"]
        self.params = []
        if "params" in data.keys():
            for param in data["params"]:
                Params(param)
        self.text = data["text"] if "text" in data.keys() else None


class Params(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.name = data["name"]
        self.value = data.get("value")
        self.fileName = data.get("fileName")
        self.contentType = data.get("contentType")


class HarReader:

    def __init__(self, filename):

        self.version = None
        self.creator = None
        self.browser = None
        self.pages = []
        self.entries = []
        self.comment = None

        with open(filename, 'rb') as har_file:
            _data = json.load(har_file)

        try:
            self._parse(_data["log"])
        except Exception:
            raise HarParsingError

    def _parse(self, data):
        self.version = data["version"]
        self.creator = Creator(data["creator"])
        self.browser = Browser(data["browser"]) if "browser" in data.keys() else None
        if "pages" in data.keys():
            for page in data["pages"]:
                self.pages.append(Page(page))
        for entry in data["entries"]:
            self.entries.append(Entry(entry))

    def __str__(self):
        return f"Version\n\t{self.version}\n{self.creator}\n{self.browser}\nPages\n\t{len(self.pages)} pages\nEntries\n\t{len(self.entries)} entries\nComment\n\t{self.comment}"

    def extract_images(self):
        """Looks through the entries and returns an array of image data.

        The image data is a dictionary with two entries:
            'filename' - The name of the file from the request url
            'data' - The Content object of the Response for an image request
        """

        media = []
        for entry in self.entries:
            if (entry.response.content.mimeType is not None) and ("image/" in entry.response.content.mimeType) and (entry.response.content.text is not None):
                content = entry.response.content.decode()
                media.append({
                    "filename": urlparse(entry.request.url).path.split("/")[-1],
                    "data": content
                })

        return media
