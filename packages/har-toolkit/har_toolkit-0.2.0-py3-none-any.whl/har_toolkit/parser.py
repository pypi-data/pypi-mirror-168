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


from .har_objects import (
    Browser,
    Creator,
    Entry,
    Page,
    HarParsingError
)


class Har:

    def __init__(self, data):

        self.version = None
        self.creator = None
        self.browser = None
        self.pages = []
        self.entries = []
        self.comment = None

        try:
            self._parse(data["log"])
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

    def extract_image_entries(self):
        """Looks through the entries and returns an array of image data.

        The image data is a dictionary with two entries:
            'filename' - The name of the file from the request url
            'data' - The Content object of the Response for an image request
        """

        media = []
        for entry in self.entries:
            if (entry.response.content is not None) and \
               (entry.response.content.mimeType is not None) and \
               ("image/" in entry.response.content.mimeType) and \
               (entry.response.content.text is not None):

                content = entry.response.content.decode()
                media.append({
                    "filename": entry.request.parse_url().path.split("/")[-1],
                    "data": content
                })

        return media
