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
import logging

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

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.getLogger("meetlify").propagate = True


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
@click.option("--posts/--no-posts", default=False)
@click.option("--assets/--no-assets", default=False)
@click.option("--sitemap/--no-sitemap", default=False)
def make(meetups, home, pages, posts, assets, sitemap):
    click.echo("Make Current Project")
    mtlfy = Meetlify(dest_=Path(os.getcwd()))

    if home:
        mtlfy.render_home()
        mtlfy.render_404_page()

    if meetups:
        mtlfy.render_meetups()

    if pages:
        mtlfy.render_pages()

    if posts:
        mtlfy.render_posts()

    if sitemap:
        mtlfy.render_redirects()
        mtlfy.render_robots_txt()
        mtlfy.render_sitemaps()

    if assets:
        mtlfy.copy_assests()

    if not any([meetups, home, pages, posts, assets, sitemap]):
        mtlfy.render_home()
        mtlfy.render_404_page()
        mtlfy.render_meetups()
        mtlfy.render_posts()
        mtlfy.render_categories()
        mtlfy.render_pages()
        mtlfy.render_redirects()
        mtlfy.render_sitemaps()
        mtlfy.render_robots_txt()
        mtlfy.copy_assests()
