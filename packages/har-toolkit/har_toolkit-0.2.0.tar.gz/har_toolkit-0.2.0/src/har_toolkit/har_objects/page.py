#!/usr/bin/env python3
from .bases import HarType
from .page_timings import PageTimings


class Page(HarType):

    def __init__(self, data):
        super().__init__(data)
        self.startedDateTime = data["startedDateTime"]
        self.id = data["id"]
        self.title = data["title"]
        self.pageTimings = PageTimings(data["pageTimings"]) if data["pageTimings"] != {} else None

    def __str__(self):
        return f"""Page\n\t{self.startedDateTime=}\n\t{self.id=}\n\t{self.title=}\n\t{self.pageTimings=}\n\t{self.comment=}"""
