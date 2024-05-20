# -*- coding: utf-8 -*-

"""
Meetlify: Static Site Generator for Meetup Websites
A Python Package for Generating Static Website for Meetups.
https://github.com/pybodensee/meetlify

    src\meetlify\\api.py

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
import shutil
from pathlib import Path
from datetime import datetime


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# 3rd PARTY LIBRARY IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

import markdown
from jinja2 import Environment, FileSystemLoader


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# INTERNAL IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from .configs import Configs
from .page import Page
from .meetup import Meetup
from .sitemap import Sitemap
from .constants import STATUS

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPLEMENATIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


class Meetlify:
    """Meetlify Static Site Generator for Meetups"""

    def __init__(self, dest_: Path) -> None:
        assert isinstance(dest_, Path)

        self.dest = dest_
        self.src = Path(__file__).resolve().parent
        self.configs = Configs.from_json(Path(self.dest, "configs.json"))

        self.renderer = Environment(
            loader=FileSystemLoader(
                Path(self.dest, "themes", self.configs.theme, "templates")
            )
        )
        self.meetups = []
        self.pages = []
        self.sitemaps = []

    def setup(self) -> None:
        """Setup Current Folder for Meetlify Website."""

        Path(self.dest, self.configs.folders.output).mkdir(parents=True, exist_ok=True)

        # TODO: Support to update themes folder - switch between multiple folders
        shutil.copytree(
            Path(self.src, "themes", self.configs.theme),
            Path(self.dest, "themes", self.configs.theme),
            dirs_exist_ok=True,
        )

        shutil.copytree(
            Path(self.src, "share", "content"),
            Path(self.dest, self.configs.folders.content),
            dirs_exist_ok=True,
        )

    def clean(self):
        """Cleanup output folder"""

        _output_folder = Path(self.dest, self.configs.folders.output)

        if not _output_folder.exists():
            _output_folder.mkdir()
        else:
            for path in _output_folder.iterdir():
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)

    def parse_meetups(self):
        """Parse all Meetup events available as Markdown"""

        self.meetups = [
            Meetup.from_markdown(mt)
            for mt in Path(self.dest, self.configs.folders.content, "meetups").iterdir()
            if mt.is_file() and mt.suffix == ".md"
        ]
        self.meetups = [
            mt
            for mt in self.meetups
            if mt.status in [STATUS.PROGRESS.value, STATUS.DONE.value]
        ]
        self.meetups = sorted(self.meetups, key=lambda x: x.id, reverse=True)

        self.sitemaps.append(
            Sitemap.from_dict(
                {
                    "name": "meetups",
                    "slug": "/meetups/",
                    "modifieddate": datetime.now(),
                    "items": self.meetups,
                }
            )
        )

    def parse_pages(self):
        """Parse Pages avaialable as Markdown"""

        self.pages = [
            Page.from_markdown(mt)
            for mt in Path(self.dest, self.configs.folders.content, "pages").iterdir()
            if mt.is_file() and mt.name in ["privacy.md", "terms.md", "contact.md"]
        ]

        self.sitemaps.append(
            Sitemap.from_dict(
                {
                    "name": "pages",
                    "slug": "/",
                    "modifieddate": datetime.now(),
                    "items": self.pages,
                }
            )
        )

    def render_home(self):
        """Render home page"""
        with codecs.open(
            Path(
                self.dest,
                self.configs.folders.content,
                self.configs.folders.pages,
                f"{self.configs.home}.md",
            ),
            "r",
            encoding="utf-8",
        ) as f:
            data = f.read()
            home_content = markdown.Markdown(extensions=["meta", "attr_list"]).convert(
                data
            )

        with open(
            Path(self.dest, self.configs.folders.output, "index.html"),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self.renderer.get_template("index.html").render(
                    meta=self.configs,
                    home_content="".join(home_content),
                    meetups=self.meetups[0:3],
                )
            )
            print("... wrote output/home")

        with open(
            Path(self.dest, self.configs.folders.output, "404.html"),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self.renderer.get_template("404.html").render(
                    meta=self.configs, meetups=self.meetups[0:3]
                )
            )
            print("... wrote output/404")

    def render_pages(self):
        """Render permanent pages"""

        for _page in self.pages:
            Path(self.dest, self.configs.folders.output, _page.slug).mkdir(
                parents=True, exist_ok=True
            )

            with open(
                Path(self.dest, self.configs.folders.output, _page.slug, "index.html"),
                mode="w",
                encoding="utf-8",
            ) as file:
                file.write(
                    self.renderer.get_template("page.html").render(
                        meta=self.configs, front=_page
                    )
                )
                print(f"... wrote output/{_page.slug}")

    def render_sitemaps(self):
        """Render Sitemaps"""

        for sitemap in self.sitemaps:
            with open(
                Path(
                    self.dest,
                    self.configs.folders.output,
                    f"sitemap-{sitemap.name}.xml",
                ),
                mode="w",
                encoding="utf-8",
            ) as file:
                file.write(
                    self.renderer.get_template("sitemap.xml").render(
                        meta=self.configs,
                        category=sitemap.slug,
                        items=sitemap.items,
                    )
                )
                print(f"... wrote output/{sitemap.name}/sitemap")

        with open(
            Path(
                self.dest,
                self.configs.folders.output,
                "sitemap-index.xml",
            ),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self.renderer.get_template("sitemap-index.xml").render(
                    meta=self.configs, sitemaps=self.sitemaps
                )
            )
            print("... wrote output/sitemap-index")

    def render_meetups(self):
        """Render meetup pages and Meetup index page"""

        # TODO: Check if there are less than 3 meetups and runs without error? make 3 config variable
        for _meetup in self.meetups:
            Path(self.dest, self.configs.folders.output, "meetups", _meetup.slug).mkdir(
                parents=True, exist_ok=True
            )

            with open(
                Path(
                    self.dest,
                    self.configs.folders.output,
                    "meetups",
                    _meetup.slug,
                    "index.html",
                ),
                mode="w",
                encoding="utf-8",
            ) as file:
                file.write(
                    self.renderer.get_template("meetup.html").render(
                        meta=self.configs,
                        content=_meetup.content,
                        front=_meetup,
                    )
                )
                print(f"... wrote output/meetups/{_meetup.slug}")

        # save meetup index page
        with open(
            Path(self.dest, self.configs.folders.output, "meetups", "index.html"),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self.renderer.get_template("meetups.html").render(
                    meta=self.configs, meetups=self.meetups
                )
            )
            print("... wrote output/meetups")

    def copy_assests(self):
        """Copy Assets e.g. Static Folders, Images, Feeds, and Sitemaps"""

        # copy static folders
        shutil.copytree(
            Path(self.dest, "themes", self.configs.theme, "static"),
            Path(
                self.dest,
                self.configs.folders.output,
                "static",
            ),
            dirs_exist_ok=True,
        )
        print("... copied output/themes static folder")

        # copy images folder
        shutil.copytree(
            Path(self.dest, self.configs.folders.content, "images"),
            Path(
                self.dest,
                self.configs.folders.output,
                "images",
            ),
            dirs_exist_ok=True,
        )
        print("... copied output/images folder")

        # copy robots.txt file
        if self.configs.robots:
            shutil.copyfile(
                Path(self.src, "share", "robots.txt"),
                Path(
                    self.dest,
                    self.configs.folders.output,
                    "robots.txt",
                ),
            )
            print("... copied output/robots.txt filed")

    def make(self):
        """Make Static Site and Save to Output folder"""

        self.parse_meetups()
        self.parse_pages()
        self.render_home()
        self.render_meetups()
        self.render_pages()
        self.render_sitemaps()
        self.copy_assests()
