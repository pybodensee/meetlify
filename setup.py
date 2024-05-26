# -*- coding: utf-8 -*-

"""
Meetlify: Static Site Generator for Meetup Websites
A Python Package for Generating Static Website for Meetups.
https://github.com/pybodensee/meetlify

    setup.py
    
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
from setuptools import (
    find_packages,
    setup,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# INTERNAL IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from src.meetlify import __version__

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# DATABASE/CONSTANTS LIST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

python_minor_min = 11
python_minor_max = 12
confirmed_python_versions = [
    "Programming Language :: Python :: 3.{MINOR:d}".format(MINOR=minor)
    for minor in range(python_minor_min, python_minor_max + 1)
]

# Fetch readme file
with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

# Define source directory (path)
SRC_DIR = "src"

# Requirements for dev and gui
extras_require = {
    "dev": [
        "black",
        "python-language-server[all]",
        "setuptools",
        "twine",
        "wheel",
        "setuptools",
        "pytest",
        "pytest-cov",
        "twine",
        "wheel",
        "mkdocs",
        "mkdocs-gen-files",
        "mkdocstrings[python]",
        "pymdown-extensions",
    ],
}
extras_require["all"] = list(
    {rq for target in extras_require.keys() for rq in extras_require[target]}
)

# Install package
setup(
    name="meetlify",
    packages=find_packages(SRC_DIR),
    package_dir={"": SRC_DIR},
    version=__version__,
    description="Python Package to Generate Meetup Websites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Faisal Shahzad",
    author_email="pybodensee@gmail.com",
    url="https://github.com/pybodensee/meetlify",
    download_url="https://github.com/pybodensee/meetlify/releases/v%s.tar.gz"
    % __version__,
    license="MIT",
    keywords=["meetups", "static-site-generators", "seo", "python"],
    scripts=[],
    include_package_data=True,
    python_requires=">=3.{MINOR:d}".format(MINOR=python_minor_min),
    setup_requires=[],
    install_requires=["click", "markdown", "Jinja2", "python-slugify"],
    extras_require=extras_require,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "meetlify = meetlify.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ]
    + confirmed_python_versions
    + [
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: System",
        "Topic :: System :: Archiving",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Archiving :: Mirroring",
        "Topic :: System :: Filesystems",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
)
