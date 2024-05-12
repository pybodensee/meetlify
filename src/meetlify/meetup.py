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

import codecs
from dataclasses import dataclass


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# 3rd PARTY LIBRARY IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

import markdown


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPLEMENATIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


@dataclass
class Meetup:
    """Meetup Data Class"""

    id: str
    title: float
    date: int
    author: str
    slug: str
    status: str
    featureimage: str
    address: str
    description: str
    content: str

    @classmethod
    def from_markdown(cls, meetup_):
        """Genreate Meetup Data Class from Markdown File

        Args:
            meetup_ (dict): Meetup as dict file

        Returns:
            Meetup: Return Constructed Meetup Object
        """
        _md = markdown.Markdown(extensions=["meta", "attr_list"])
        with codecs.open(meetup_, "r", encoding="utf-8") as f:
            data = f.read()
            return cls(
                content=_md.convert(data),
                id="".join(_md.Meta["id"]),
                date="".join(_md.Meta["date"]),
                author="".join(_md.Meta["author"]),
                title="".join(_md.Meta["title"]),
                description="".join(_md.Meta["description"]),
                slug="".join(_md.Meta["slug"]),
                featureimage="".join(_md.Meta["featureimage"]),
                address="".join(_md.Meta["address"]),
                status="".join(_md.Meta["status"]),
            )
