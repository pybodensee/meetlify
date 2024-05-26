# -*- coding: utf-8 -*-

"""
Meetlify: Static Site Generator for Meetup Websites
A Python Package for Generating Static Website for Meetups.
https://github.com/pybodensee/meetlify

    src\meetlify\page.py

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

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# 3rd PARTY LIBRARY IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from slugify import slugify

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# INTERNAL IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from .utils import markdown_convertor
from .constants import STATUS

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPLEMENATIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


@dataclass
class Page:
    title: str
    author: str
    description: str
    slug: str
    create_date: datetime
    last_modified: datetime
    toc: str
    content: str
    add_to_sitemap: bool
    status: str

    def __lt__(self, other_):
        return self.create_date < other_.create_date

    @classmethod
    def from_markdown(cls, page_md_: Path):
        meta, toc, content = markdown_convertor(page_md_)
        return cls(
            title=meta.get("title"),
            author=meta.get("author"),
            description=meta.get("description"),
            slug=meta.get("slug") or slugify(meta.get("title")),
            create_date=datetime.strptime(meta.get("create_date"), "%Y-%m-%d::%H:%M"),
            last_modified=datetime.fromtimestamp(
                page_md_.stat().st_mtime, tz=timezone.utc
            ),
            toc=toc,
            content=content,
            add_to_sitemap=bool(meta.get("add_to_sitemap")),
            status=meta.get("status"),
        )


class Pages:
    def __init__(self, *, path_: Path, reverse_: bool = True) -> None:
        self.content = sorted(
            [
                Page.from_markdown(page_md)
                for page_md in path_.iterdir()
                if page_md.is_file() and page_md.suffix == ".md"
            ],
            reverse=reverse_,
        )

    def __getitem__(self, status_: list[STATUS] | STATUS) -> list[Page]:
        if isinstance(status_, STATUS):
            status_ = [status_]
        return [
            content
            for content in self.content
            if content.status in [stat.value for stat in status_]
        ]
