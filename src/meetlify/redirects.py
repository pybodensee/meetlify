# -*- coding: utf-8 -*-

"""
Meetlify: Static Site Generator for Meetup Websites
A Python Package for Generating Static Website for Meetups.
https://github.com/pybodensee/meetlify

    src\meetlify\\redirects.py

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
class Redirect:
    from_: str
    to: str
    force: bool
    status_code: int

    def __str__(self) -> str:
        return f"{self.from_}\t{self.to}\t{self.status_code}"

    @classmethod
    def from_dict(cls, object_: dict):
        return cls(
            from_=object_.get("from_"),
            to=object_.get("to"),
            force=object_.get("force"),
            status_code=object_.get("status_code"),
        )


class Redirects:
    def __init__(self, *, redirect_items_: list[dict]) -> None:
        self.all_redirects = [
            Redirect.from_dict(
                {
                    "from_": redirect_item.get("from"),
                    "to": redirect_item.get("to"),
                    "force": redirect_item.get("force"),
                    "status_code": redirect_item.get("status_code"),
                }
            )
            for redirect_item in redirect_items_
        ]

    def __getitem__(self, status_code_: list[int] | int) -> list[Redirect]:
        if not isinstance(status_code_, list):
            status_code_ = [status_code_]

        return [
            redirect
            for redirect in self.all_redirects
            if redirect.status_code in status_code_
        ]

    def __str__(self) -> str:
        return "\n".join([str(redirect) for redirect in self.all_redirects])

    @classmethod
    def from_json(cls, json_file_: Path):
        assert isinstance(json_file_, Path)
        assert json_file_.exists()
        with codecs.open(json_file_, "r", encoding="utf-8") as f:
            return cls(redirect_items_=json.load(f))
