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
class Menu:
    """Menu Data Class to hold Header and footer menus"""

    header: dict
    footer: dict


@dataclass
class Folders:
    """Folder data class for differnt types of folder used in Processing"""

    output: str
    content: str
    meetups: str
    pages: str


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

    @classmethod
    def from_json(cls, json_file_: Path):
        """Generate Config data class from json file

        Args:
            json_file (Path): Json file containing Project Configurations

        Returns:
            Configs: Return Configs Data object
        """
        assert isinstance(json_file_, Path)
        assert json_file_.exists()

        with codecs.open(json_file_, "r", encoding="utf-8") as f:
            cfgs = json.load(f)
            return cls(
                name=cfgs["name"],
                URL=cfgs["URL"],
                language=cfgs["language"],
                theme=cfgs["theme"],
                title=cfgs["title"],
                author=cfgs["author"],
                email=cfgs["email"],
                description=cfgs["description"],
                sitemap=cfgs["sitemap"],
                feeds=cfgs["feeds"],
                robots=cfgs["robots"],
                logo=cfgs["logo"],
                favicon=cfgs["favicon"],
                copyright=cfgs["copyright"],
                home=cfgs["home"],
                folders=Folders(**cfgs["folders"]),
                menu=Menu(**cfgs["menu"]),
            )
