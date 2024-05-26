# -*- coding: utf-8 -*-

"""
Meetlify: Static Site Generator for Meetup Websites
A Python Package for Generating Static Website for Meetups.
https://github.com/pybodensee/meetlify

    src\meetlify\configs.py

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


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPLEMENATIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


@dataclass
class Banner:
    """Banner Data Class to hold Banners on Posts"""

    name: str
    type_: str
    message: str


@dataclass
class Menu:
    """Menu Data Class to hold Header and footer menus"""

    header: dict
    footer: dict


@dataclass
class Folders:
    """Folder data class for differnt types of folder used in Processing"""

    output: str
    themes: str
    images: str
    content: str
    meetups: str
    pages: str
    posts: str
    categories: str


@dataclass
class Configs:
    """Config Data Class to hold Project Configurations"""

    name: str
    URL: str
    language: str
    theme: str
    title: str
    author: str
    email: str
    description: str
    sitemap: bool
    feeds: bool
    robots: bool
    logo: str
    favicon: str
    copyright: str
    home: str
    folders: dict
    menu: Menu
    about_us: list[str]
    banners: list[Banner]

    @classmethod
    def from_json(cls, json_file_: Path):
        assert isinstance(json_file_, Path)
        assert json_file_.exists()

        with codecs.open(json_file_, "r", encoding="utf-8") as f:
            cfgs = json.load(f)
            return cls(
                name=cfgs.get("name"),
                URL=cfgs.get("URL"),
                language=cfgs.get("language"),
                theme=cfgs.get("theme"),
                title=cfgs.get("title"),
                author=cfgs.get("author"),
                email=cfgs.get("email"),
                description=cfgs.get("description"),
                sitemap=cfgs.get("sitemap"),
                feeds=cfgs.get("feeds"),
                robots=cfgs.get("robots"),
                logo=cfgs.get("logo"),
                favicon=cfgs.get("favicon"),
                copyright=cfgs.get("copyright"),
                home=cfgs.get("home"),
                folders=Folders(**cfgs.get("folders")),
                menu=Menu(**cfgs.get("menu")),
                about_us=cfgs.get("about_us"),
                banners=[Banner(**banner) for banner in cfgs.get("banners")],
            )

    def get_banner(self, banner_name: str) -> Banner:

        return next(
            (banner for banner in self.banners if banner.name == banner_name),
            Banner(name=None, type_="", message=""),
        )
