# -*- coding: utf-8 -*-

"""
Meetlify: Static Site Generator for Meetup Websites
A Python Package for Generating Static Website for Meetups.
https://github.com/pybodensee/meetlify

    src\meetlify\constants.py
    
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

from enum import Enum

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# DATABASE/CONSTANTS LIST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_REVISION = 12

FULL_VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_REVISION}"


class ExtendedEnum(Enum):
    """An extended enum class to convert list of items in an enumration."""

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class STATUS(ExtendedEnum):
    """An enum for the different Hostings."""

    DRAFT = "draft"
    PLANNING = "planning"
    PUBLISHED = "published"
    DONE = "done"


class BANNER(ExtendedEnum):
    """An enum for the different Banners."""

    DRAFT = "draft"
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
