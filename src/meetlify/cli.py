# -*- coding: utf-8 -*-

"""
Meetlify: Static Site Generator for Meetup Websites
A Python Package for Generating Static Website for Meetups.
https://github.com/pybodensee/meetlify

    src\meetlify\cli.py

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

import os
from pathlib import Path


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# 3rd PARTY LIBRARY IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

import click


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# INTERNAL IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from .api import Meetlify
from .utils import initialize


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPLEMENATIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


@click.group()
def main():
    pass


@main.command("init", help="Initialize Meetlify Project")
def init():
    click.echo("Initialize Meetlify Project")
    initialize(dest_=Path(os.getcwd()))


@main.command("setup", help="Setup Project Structure")
def setup():
    click.echo("Setup Project Structure")
    Meetlify(dest_=Path(os.getcwd())).setup()


@main.command("clean", help="Clean Output Folder")
def clean():
    click.echo("Clean Output Folder")
    Meetlify(dest_=Path(os.getcwd())).clean()


@main.command("make", help="Make Current Project")
@click.option("--meetups/--no-meetups", default=False)
@click.option("--home/--no-home", default=False)
@click.option("--pages/--no-pages", default=False)
@click.option("--assets/--no-assets", default=False)
@click.option("--sitemap/--no-sitemap", default=False)
def make(meetups, home, pages, assets, sitemap):
    click.echo("Make Current Project")
    _mlfy = Meetlify(dest_=Path(os.getcwd()))

    if meetups:
        _mlfy.parse_meetups()
        _mlfy.render_meetups()

    if home:
        _mlfy.parse_meetups()
        _mlfy.render_home()

    if pages:
        _mlfy.parse_pages()
        _mlfy.render_pages()

    if assets:
        _mlfy.copy_assests()

    if sitemap:
        _mlfy.parse_meetups()
        _mlfy.parse_pages()
        _mlfy.render_sitemaps()

    if not any([meetups, home, pages, assets, sitemap]):
        _mlfy.make()
