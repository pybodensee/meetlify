# -*- coding: utf-8 -*-

"""
Meetlify: Static Site Generator for Meetup Websites
A Python Package for Generating Static Website for Meetups.
https://github.com/pybodensee/meetlify

    src\meetlify\meetup.py

    Copyright (C) 2024-2024 Faisal Shahzad <info@serpwings.com>

<LICENSE_BLOCK>
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</LICENSE_BLOCK>
"""


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# STANDARD LIBARY IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Self


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# 3rd PARTY LIBRARY IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from slugify import slugify

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# INTERNAL IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from .constants import STATUS
from .utils import markdown_convertor

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPLEMENATIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


@dataclass
class Meetup:
    title: str
    description: str
    organizer: list[str]
    slug: str
    categories: str
    event_datetime: datetime
    last_modified: datetime
    feature_image: str
    address: str
    toc: str
    content: str
    add_to_sitemap: bool
    status: str  # TODO: replace with STATUS ENUM

    def __lt__(self, other_: Self) -> bool:
        return self.event_datetime < other_.event_datetime

    @classmethod
    def from_markdown(cls, meetup_md_: Path) -> Self:
        meta, toc, content = markdown_convertor(meetup_md_)
        return cls(
            title=meta.get("title"),
            description=meta.get("description"),
            organizer=meta.get("organizer"),
            slug=meta.get("slug") or slugify(meta.get("title")),
            event_datetime=datetime.strptime(
                meta.get("event_datetime"), "%Y-%m-%d::%H:%M"
            ),
            last_modified=datetime.fromtimestamp(
                meetup_md_.stat().st_mtime, tz=timezone.utc
            ),
            categories=[
                category.strip() for category in meta.get("categories").split(",")
            ],
            feature_image=meta.get("feature_image"),
            address=meta.get("address"),
            toc=toc,
            content=content,
            add_to_sitemap=bool(meta.get("add_to_sitemap")),
            status=meta.get("status"),
        )


class Meetups:
    def __init__(self, *, path_: Path, reverse_: bool = True) -> None:
        self.events = sorted(
            [
                Meetup.from_markdown(meetup_md)
                for meetup_md in path_.iterdir()
                if meetup_md.is_file() and meetup_md.suffix == ".md"
            ],
            reverse=reverse_,
        )

    def __getitem__(self, status_: list[STATUS] | STATUS) -> list[Meetup]:
        if isinstance(status_, STATUS):
            status_ = [status_]

        return [
            event
            for event in self.events
            if event.status in [stat.value for stat in status_]
        ]
