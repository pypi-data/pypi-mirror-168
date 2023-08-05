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


class SimpleHarType:

    def __init__(self, data):
        self.name = data["name"]
        self.version = data["version"]
        self.comment = data["comment"] if "comment" in data.keys() else None

    def __str__(self):
        return f"{type(self).__name__}\n\t{self.name=}\n\t{self.version=}\n\t{self.comment=}"


class Creator(SimpleHarType):
    pass


class Browser(SimpleHarType):
    pass


class Page:

    def __init__(self, data):
        self.startedDateTime = data["startedDateTime"]
        self.id = data["id"]
        self.title = data["title"]
        self.pageTimings = PageTimings(data["pageTimings"])
        self.comment = data["comment"] if "comment" in data.keys() else None

    def __str__(self):
        return f"""Page\n\t{self.startedDateTime=}\n\t{self.id=}\n\t{self.title=}\n\t{self.pageTimings=}\n\t{self.comment=}"""


class PageTimings:

    def __init__(self, data):
        self.onContentLoad = data["onContentLoad"] if "onContentLoad" in data.keys() else None
        self.onLoad = data["onLoad"] if "onLoad" in data.keys() else None
        self.comment = data["comment"] if "comment" in data.keys() else None


class Timings:

    def __init__(self, data):
        pass


class Cache:

    def __init__(self, data):
        pass


class Entry:

    def __init__(self, data):

        self.pageref = data["pageref"] if "pageref" in data.keys() else None
        self.startedDateTime = data["startedDateTime"]
        self.time = data["time"]
        self.request = Request(data["request"])
        self.response = Response(data["response"])
        self.timings = Timings(data["timings"])
        self.serverIPAddress = data["serverIPAddress"] if "serverIPAddress" in data.keys() else None
        self.connection = data["connection"] if "connection" in data.keys() else None
        self.comment = data["comment"] if "comment" in data.keys() else None


class Request:

    def __init__(self, data):
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
        self.comment = data["comment"] if "comment" in data.keys() else None


class Response:

    def __init__(self, data):
        self.status = data["status"]
        self.statusText = data["statusText"]
        self.httpVersion = data["httpVersion"]
        self.cookies = []
        for cookie in data["cookies"]:
            self.cookies.append(Cookie(cookie))
        self.headers = []
        for header in data["headers"]:
            self.headers.append(Header(header))
        self.content = Content(data["content"])
        self.redirectURL = data["redirectURL"]
        self.headersSize = data["headersSize"] if "headersSize" in data.keys() else None
        self.bodySize = data["bodySize"]
        self.comment = data["comment"] if "comment" in data.keys() else None


class Cookie:

    def __init__(self, data):
        self.name = data["name"]
        self.value = data["value"]
        self.path = data["path"] if "path" in data.keys() else None
        self.domain = data["domain"] if "domain" in data.keys() else None
        self.expires = data["expires"] if "expires" in data.keys() else None
        self.httpOnly = data["httpOnly"] if "httpOnly" in data.keys() else None
        self.secure = data["secure"] if "secure" in data.keys() else None
        self.comment = data["comment"] if "comment" in data.keys() else None


class Header:

    def __init__(self, data):
        self.name = data["name"]
        self.value = data["value"]
        self.comment = data["comment"] if "comment" in data.keys() else None


class queryString(SimpleHarType):
    pass


class Content:

    def __init__(self, data):
        self.size = data["size"] if "size" in data.keys() else None
        self.compression = data["compression"] if "compression" in data.keys() else None
        self.mimeType = data["mimeType"] if "mimeType" in data.keys() else None
        self.text = data["text"] if "text" in data.keys() else None
        self.encoding = data["encoding"] if "encoding" in data.keys() else None
        self.comment = data["comment"] if "comment" in data.keys() else None

    def decode(self):
        if self.encoding == "base64":
            self.text = b64decode(self.text)
        else:
            # Nothing to decode
            pass
        return self


class PostData:

    def __init__(self, data):
        self.mimeType = data["mimeType"]
        self.params = []
        if "params" in data.keys():
            for param in data["params"]:
                Params(param)
        self.text = data["text"] if "text" in data.keys() else None
        self.comment = data["comment"] if "comment" in data.keys() else None


class Params:

    def __init__(self, data):
        self.name = data["name"] if "name" in data.keys() else None
        self.value = data["value"] if "value" in data.keys() else None
        self.fileName = data["fileName"] if "fileName" in data.keys() else None
        self.contentType = data["contentType"] if "contentType" in data.keys() else None
        self.comment = data["comment"] if "comment" in data.keys() else None


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

