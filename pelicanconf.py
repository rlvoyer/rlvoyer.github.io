#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

HOME = os.environ["HOME"]
AUTHOR = u'Robert Voyer'
SITENAME = '[ robert voyer ]'
SITEURL = ''
SITESUBTITLE = ''
MENUITEMS = (("blog", "archives.html"),)

PATH = 'content'

STATIC_PATHS = ['images']

PAGE_PATHS = ['pages']

TIMEZONE = 'America/Vancouver'

DEFAULT_LANG = u'en'
DEFAULT_DATE_FORMAT = '%B %d, %Y'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Categories
DISPLAY_CATEGORIES_ON_MENU = True

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'theme'

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
    }
}

PLUGIN_PATHS = ['{}/Code/pelican-plugins'.format(HOME)]

PLUGINS = ['render_math']

DESCRIPTION = 'A view on a data science and software engineering from a ' \
              'Seattle technologist'
