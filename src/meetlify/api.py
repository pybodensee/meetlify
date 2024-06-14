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

import shutil
import logging
from pathlib import Path


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# 3rd PARTY LIBRARY IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from jinja2 import Environment, FileSystemLoader


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# INTERNAL IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from .configs import Configs
from .posts import Posts
from .categories import Categories
from .pages import Pages
from .meetups import Meetups
from .sitemaps import Sitemaps
from .redirects import Redirects
from .robots import Robots
from .constants import STATUS

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPLEMENATIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

logging.getLogger("meetlify").addHandler(logging.NullHandler())


class Meetlify:
    """Meetlify Static Site Generator for Meetups"""

    def __init__(self, dest_: Path) -> None:
        assert isinstance(dest_, Path)

        self.dest = dest_
        self.src = Path(__file__).resolve().parent
        self.configs = Configs.from_json(Path(self.dest, "configs.json"))

        self.renderer = Environment(
            loader=FileSystemLoader(
                Path(
                    self.dest,
                    self.configs.folders.themes,
                    self.configs.theme,
                    "templates",
                )
            )
        )

        self.meetups = Meetups(
            path_=Path(
                self.dest,
                self.configs.folders.content,
                self.configs.folders.meetups,
            ),
            reverse_=True,
        )

        self.posts = Posts(
            path_=Path(
                self.dest, self.configs.folders.content, self.configs.folders.posts
            ),
            reverse_=True,
        )

        self.categories = Categories(
            path_=Path(
                self.dest, self.configs.folders.content, self.configs.folders.categories
            ),
            reverse_=True,
        )

        self.pages = Pages(
            path_=Path(
                self.dest, self.configs.folders.content, self.configs.folders.pages
            ),
            reverse_=True,
        )

        self.sitemaps = Sitemaps(
            sitemap_items_=[
                {
                    "name": self.configs.folders.pages,
                    "items": self.pages[STATUS.PUBLISHED, STATUS.DONE],
                    "robots_txt": True,
                },
                {
                    "name": self.configs.folders.posts,
                    "items": self.posts[STATUS.PUBLISHED, STATUS.DONE],
                    "robots_txt": True,
                },
                {
                    "name": self.configs.folders.meetups,
                    "items": self.meetups[STATUS.PUBLISHED, STATUS.DONE],
                    "robots_txt": True,
                },
                {
                    "name": self.configs.folders.categories,
                    "items": self.categories[STATUS.PUBLISHED, STATUS.DONE],
                    "robots_txt": True,
                },
            ]
        )

        self.redirects = Redirects.from_json(Path(self.dest, "redirects.json"))
        self.robots = Robots.from_json(Path(self.dest, "robots.json"))

    def setup(self) -> None:
        """Setup Current Folder for Meetlify Website."""
        Path(self.dest, self.configs.folders.output).mkdir(parents=True, exist_ok=True)
        # TODO: Support to update themes folder - switch between multiple folders
        shutil.copytree(
            Path(self.src, self.configs.folders.themes, self.configs.theme),
            Path(self.dest, self.configs.folders.themes, self.configs.theme),
            dirs_exist_ok=True,
        )

        shutil.copytree(
            Path(self.src, "share", "content"),
            Path(self.dest, self.configs.folders.content),
            dirs_exist_ok=True,
        )

    def clean(self):
        """Cleanup output folder"""

        output_folder = Path(self.dest, self.configs.folders.output)

        if not output_folder.exists():
            output_folder.mkdir()
        else:
            for path in output_folder.iterdir():
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)

    def render_home(self):
        with open(
            Path(self.dest, self.configs.folders.output, "index.html"),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self.renderer.get_template("index.html").render(
                    meta=self.configs,
                    about_us_paragraphs=self.configs.about_us,
                    meetups=self.meetups[STATUS.PUBLISHED, STATUS.DONE][0:3],
                    posts=self.posts[STATUS.PUBLISHED, STATUS.DONE][0:3],
                    categories=self.categories[STATUS.PUBLISHED, STATUS.DONE][0:8],
                )
            )
            logging.info("... wrote output/home")

    def render_404_page(self):
        with open(
            Path(self.dest, self.configs.folders.output, "404.html"),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self.renderer.get_template("404.html").render(
                    meta=self.configs,
                    meetups=self.meetups[STATUS.PUBLISHED, STATUS.DONE][0:3],
                    posts=self.posts[STATUS.PUBLISHED, STATUS.DONE][0:3],
                    categories=self.categories[STATUS.PUBLISHED, STATUS.DONE][0:3],
                )
            )
            logging.info("... wrote output/404")

    def render_meetups(self):
        """Render meetup pages and Meetup index page"""

        # TODO: Check if there are less than 3 meetups and runs without error? make 3 config variable
        for meetup in self.meetups[STATUS.PUBLISHED, STATUS.DONE]:
            Path(
                self.dest,
                self.configs.folders.output,
                self.configs.folders.meetups,
                meetup.slug,
            ).mkdir(parents=True, exist_ok=True)

            with open(
                Path(
                    self.dest,
                    self.configs.folders.output,
                    self.configs.folders.meetups,
                    meetup.slug,
                    "index.html",
                ),
                mode="w",
                encoding="utf-8",
            ) as file:
                file.write(
                    self.renderer.get_template("meetup.html").render(
                        meta=self.configs,
                        meetup=meetup,
                        meetups=self.meetups[STATUS.PUBLISHED, STATUS.DONE][1:4],
                    )
                )
                logging.info(f"...... wrote output/meetups/{meetup.slug}")

        # save meetup index page
        with open(
            Path(
                self.dest,
                self.configs.folders.output,
                self.configs.folders.meetups,
                "index.html",
            ),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self.renderer.get_template("meetups.html").render(
                    meta=self.configs,
                    meetups=self.meetups[STATUS.PUBLISHED, STATUS.DONE],
                )
            )
            logging.info("... wrote output/meetups")

    def render_posts(self):
        """Render posts and Meetup index page"""

        # TODO: Check if there are less than 3 posts  and runs without error? make 3 config variable
        for post in self.posts[STATUS.PUBLISHED, STATUS.DONE]:
            Path(
                self.dest,
                self.configs.folders.output,
                self.configs.folders.posts,
                post.slug,
            ).mkdir(parents=True, exist_ok=True)

            with open(
                Path(
                    self.dest,
                    self.configs.folders.output,
                    self.configs.folders.posts,
                    post.slug,
                    "index.html",
                ),
                mode="w",
                encoding="utf-8",
            ) as file:
                file.write(
                    self.renderer.get_template("post.html").render(
                        meta=self.configs,
                        post=post,
                        posts=self.posts[STATUS.PUBLISHED, STATUS.DONE][1:4],
                        banner=self.configs.get_banner(banner_name=post.banner),
                    )
                )
                logging.info(f"...... wrote output/posts/{post.slug}")

        # save meetup index page
        with open(
            Path(
                self.dest,
                self.configs.folders.output,
                self.configs.folders.posts,
                "index.html",
            ),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self.renderer.get_template("posts.html").render(
                    meta=self.configs, posts=self.posts[STATUS.PUBLISHED, STATUS.DONE]
                )
            )
            logging.info("... wrote output/posts")

    def render_categories(self):
        """Render categoires and categoires index page"""

        # TODO: Check if there are less than 3 posts  and runs without error? make 3 config variable
        for category in self.categories[STATUS.PUBLISHED, STATUS.DONE]:
            Path(
                self.dest,
                self.configs.folders.output,
                self.configs.folders.categories,
                category.slug,
            ).mkdir(parents=True, exist_ok=True)

            with open(
                Path(
                    self.dest,
                    self.configs.folders.output,
                    self.configs.folders.categories,
                    category.slug,
                    "index.html",
                ),
                mode="w",
                encoding="utf-8",
            ) as file:
                file.write(
                    self.renderer.get_template("category.html").render(
                        meta=self.configs,
                        category=category,
                        posts=self.posts.by_categories()[category.slug][0:3],
                    )
                )
                logging.info(f"...... wrote output/categories/{category.slug}")

        # save meetup index page
        with open(
            Path(
                self.dest,
                self.configs.folders.output,
                self.configs.folders.categories,
                "index.html",
            ),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(
                self.renderer.get_template("categories.html").render(
                    meta=self.configs,
                    categories=self.categories[STATUS.PUBLISHED, STATUS.DONE],
                )
            )
            logging.info("... wrote output/categories")

    def render_pages(self):
        """Render permanent pages"""

        for page in self.pages[STATUS.PUBLISHED, STATUS.DONE]:
            Path(
                self.dest,
                self.configs.folders.output,
                self.configs.folders.pages,
                page.slug,
            ).mkdir(parents=True, exist_ok=True)

            with open(
                Path(
                    self.dest,
                    self.configs.folders.output,
                    self.configs.folders.pages,
                    page.slug,
                    "index.html",
                ),
                mode="w",
                encoding="utf-8",
            ) as file:
                file.write(
                    self.renderer.get_template("page.html").render(
                        meta=self.configs, page=page
                    )
                )
                logging.info(f"... wrote output/{page.slug}")

    def render_sitemaps(self):
        """Render Sitemaps"""

        for sitemap in self.sitemaps[STATUS.PUBLISHED]:
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
                        meta=self.configs, sitemap=sitemap
                    )
                )
                logging.info(f"... wrote output/{sitemap.name}/sitemap")

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
                    meta=self.configs, sitemaps=self.sitemaps[STATUS.PUBLISHED]
                )
            )
            logging.info("... wrote output/sitemap-index")

    def render_redirects(self):
        with open(
            Path(
                self.dest,
                self.configs.folders.output,
                "_redirects",
            ),
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(str(self.redirects))
            logging.info("... wrote output/redirects file")

    def render_robots_txt(self):
        # Add additional sitemaps to Robots.txt if not added in robots.json
        self.robots.add_sitemaps(
            additional_sitems=[
                f"{self.configs.URL}/sitemap-{sitemap.name}.xml"
                for sitemap in self.sitemaps[STATUS.PUBLISHED, STATUS.DONE]
                if sitemap.robots_txt
            ]
        )

        if self.configs.robots:
            with open(
                Path(
                    self.dest,
                    self.configs.folders.output,
                    "robots.txt",
                ),
                mode="w",
                encoding="utf-8",
            ) as file:
                file.write(str(self.robots))
                logging.info("... wrote output/robots.txt file")

    def copy_assests(self):
        # copy static folders
        shutil.copytree(
            Path(self.dest, self.configs.folders.themes, self.configs.theme, "static"),
            Path(
                self.dest,
                self.configs.folders.output,
                "static",
            ),
            dirs_exist_ok=True,
        )
        logging.info("... copied output/themes static folder")

        # copy images folder
        shutil.copytree(
            Path(self.dest, self.configs.folders.content, self.configs.folders.images),
            Path(
                self.dest,
                self.configs.folders.output,
                self.configs.folders.images,
            ),
            dirs_exist_ok=True,
        )
        logging.info("... copied output/images folder")

    def make(self):
        self.render_home()
        self.render_404_page()
        self.render_meetups()
        self.render_posts()
        self.render_categories()
        self.render_pages()
        self.render_redirects()
        self.render_sitemaps()
        self.render_robots_txt()
        self.copy_assests()
