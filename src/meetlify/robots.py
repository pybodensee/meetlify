# -*- coding: utf-8 -*-

"""
Meetlify: Static Site Generator for Meetup Websites
A Python Package for Generating Static Website for Meetups.
https://github.com/pybodensee/meetlify

    src\meetlify\\robots.py

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

import json
import codecs
from pathlib import Path
from dataclasses import dataclass
from typing import Self

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPLEMENATIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


@dataclass
class RobotAgent:
    name: str
    allow: list[str]
    disallow: list[str]

    def __str__(self) -> str:
        allows = "\nAllow: " if self.allow else ""
        allows += "\nAllow: ".join(self.allow)

        disallows = "\nDisallow: " if self.disallow else ""
        disallows += "\nDisallow: ".join(self.disallow)

        return f"User-agent: {self.name}{allows}{disallows}\n\n"

    @classmethod
    def from_dict(cls, object_: dict) -> Self:
        return cls(**object_)


class Robots:
    def __init__(self, *, robots_items_: dict) -> None:
        self.all_robots = [
            RobotAgent.from_dict(
                {
                    "name": robot_name,
                    "allow": robot_values.get("allow"),
                    "disallow": robot_values.get("disallow"),
                }
            )
            for robot_name, robot_values in robots_items_.items()
            if robot_name != "sitemaps"
        ]

        self.sitemaps = robots_items_.get("sitemaps")

    def __str__(self) -> str:
        sitemap_as_str = "\nSitemap: " if self.sitemaps else ""
        sitemap_as_str += "\nSitemap: ".join(set(self.sitemaps)) # Get Uniqe Sitemaps

        return (
            "\n".join([str(robot_agent) for robot_agent in self.all_robots])
            + sitemap_as_str
        )

    @classmethod
    def from_json(cls, json_file_: Path) -> Self:
        assert isinstance(json_file_, Path)
        assert json_file_.exists()
        with codecs.open(str(json_file_), "r", encoding="utf-8") as f:
            return cls(robots_items_=json.load(f))

    def add_sitemaps(self, additional_sitems: list[str]) -> None:
        self.sitemaps += additional_sitems
