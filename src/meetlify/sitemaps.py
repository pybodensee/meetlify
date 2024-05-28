# -*- coding: utf-8 -*-

"""
Meetlify: Static Site Generator for Meetup Websites
A Python Package for Generating Static Website for Meetups.
https://github.com/pybodensee/meetlify

    src\meetlify\sitemap.py

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

from dataclasses import dataclass
from datetime import datetime
from typing import Self

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# INTERNAL IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from .constants import STATUS

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPLEMENATIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


@dataclass
class Sitemap:
    name: str
    slug: str
    last_modified: datetime
    urls: list
    images: list
    news: list
    videos: list
    status: STATUS
    robots_txt: bool # Add to robots.txt

    @classmethod
    def from_dict(cls, object_: dict) -> Self:
        return cls(
            name=object_.get("name"),
            slug=object_.get("slug"),
            last_modified=object_.get("last_modified"),
            urls=object_.get("urls"),
            images=object_.get("images"),
            news=object_.get("news"),
            videos=object_.get("videos"),
            status=object_.get("status"),
            robots_txt=object_.get("robots_txt"),
        )


class Sitemaps:
    def __init__(self, *, sitemap_items_: list[dict]) -> None:
        self.all_sitemaps = [
            Sitemap.from_dict(
                {
                    "name": sitemap_item.get("name"),
                    "slug": f"/{sitemap_item.get('name')}/",
                    "last_modified": (
                        sitemap_item.get("items")[0].last_modified
                        if len(sitemap_item.get("items")) > 0
                        else datetime.now()
                    ),
                    "urls": sitemap_item.get("items"),
                    "images": [],
                    "news": [],
                    "videos": [],
                    "status": STATUS.PUBLISHED.value,
                    "robots_txt": sitemap_item.get("robots_txt")
                }
            )
            for sitemap_item in sitemap_items_
        ]

    def __getitem__(self, status_: list[STATUS] | STATUS) -> list[Sitemap]:
        if isinstance(status_, STATUS):
            status_ = [status_]

        return [
            sitemap
            for sitemap in self.all_sitemaps
            if sitemap.status in [stat.value for stat in status_]
        ]
