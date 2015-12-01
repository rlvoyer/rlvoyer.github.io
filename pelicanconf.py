#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Robert Voyer'
SITENAME = u'[ ) Between Two Ranges ( ]'
SITEURL = ''
SITESUBTITLE = ''
MENUITEMS = (("about", "about.html"), ("archives", "archives.html"))

PATH = 'content'

STATIC_PATHS = ['images']

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

# Comments
DISQUS_SITENAME = "betweentworanges"

# Blogroll
LINKS = (('Socrata', 'http://www.socrata.com/'),
         ('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'))

# Social widget
SOCIAL = (('Find me on Github', 'http://www.github.com/rlvoyer'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Theme
THEME = '/Users/robertvoyer/Code/pelican-themes/aboutwilson'

MD_EXTENSIONS = ['codehilite(css_class=highlight code)', 'extra']

PLUGIN_PATHS = ['/Users/robertvoyer/Code/pelican-plugins']

PLUGINS = ['render_math']

DESCRIPTION = 'A blog about things'
