# meetlify

Python based Static Site Genrators for Meetups/Meetup Webites.

[![license](https://img.shields.io/pypi/l/meetlify.svg?style=flat-square "Project License: MIT")](https://github.com/pybodensee/meetlify/blob/master/LICENSE)
[![status](https://img.shields.io/pypi/status/meetlify.svg?style=flat-square "Project Development Status")](https://github.com/pybodensee/meetlify/milestone/1)
[![pypi_version](https://img.shields.io/pypi/v/meetlify.svg?style=flat-square "Available on PyPi - the Python Package Index")](https://pypi.python.org/pypi/meetlify)
[![supported_python_versions](https://img.shields.io/pypi/pyversions/meetlify.svg?style=flat-square "Supported Python Version")](https://pypi.python.org/pypi/meetlify)


## How to Use?
This package is available at ``pypi`` and you can install it with ``pip install meetlify`` command. It will also install required additional libraries/Python Packages automatically.

### Using GitHub Template

We have prepard [meetlify-template](https://github.com/pybodensee/meetlify-template) which is a sample template repository. Just use this template to create your own repository. 

This approach is for buy and non techies who just want to host a simple meetup website. Make sure that GitHub actions are allowed to execute on your account. After successful clone, the website will automatically create/update gh_pages branch which you can link with any static hosting provider e.g. GitHub Page, Netlify, Cloudflare Pages, Vercel and others. However, this repo is optimized for hosting on Netlify.

### Using Command Line Interface (CLI)

Create an empty folder on your computer or move to a desired location where you want to create the Meetup Website. 

1. Now execute ``meetlify init`` which will crate an empty configuration file (JSON) in the folder. Feel free to edit it as per your need. Content of the configuration file are self explanatory.  

2. Now execute ``meetlify setup`` which will setup the all folders as per your configurations. 

3. Now execute ``meetlify make`` which will generate full website in output folder.


### Using Application Programming Interface (API)

You can embed ``meetilify`` into your existing workflow easily. Here is a sample snippet.

```python
from pathlib import Path
from meetlify.api import Meetlify
from meetlify.utils import initialize

destination_path = Path("/home/user/Desktop/sample_webiste/")

# Now initialize configurationn file
initialize(dest_=destination_path)

# Modify newly created config.json file as per your need.
mtlfy = Meetlify(dest_=destination_path)
mtlfy.render_home()
mtlfy.render_404_page()
mtlfy.render_meetups()
mtlfy.render_posts()
mtlfy.render_pages()
mtlfy.render_categories()
mtlfy.render_redirects()
mtlfy.render_sitemaps()
mtlfy.render_robots_txt()
mtlfy.copy_assests()

```

## How to Extend ?
- Clone or download this repository to your computer.
- Create a virtual environment using ``python -m .venv venv``
- Navigate to the downloaded directory and then install all required dependencies using ``pip install -e .``
- Now you can open ``api.py`` file and start editing it. Feel free to extend it or even submit a pull request if you have a useful feature. 

## Contribute

Pull Requests, Feature Suggestions, and collaborations are welcome.

## About Us

This work is a collaborative effort of [PyBodensee](https://pybodensee.com/), and [SerpWings](https://serpwings.com/).