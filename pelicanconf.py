#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'University of California, Berkeley'
SITENAME = u'pywren'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'US/Pacific'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
PLUGIN_PATHS = ['/Users/jonas/projects/pywren/pelican-plugins']

PLUGINS = ['i18n_subsites', 'jinja2content']


THEME = "pelican-bootstrap3"
BOOTSTRAP_THEME = 'spacelab' 

HIDE_SIDEBAR=True
DISPLAY_CATEGORIES_ON_MENU=False
MENUITEMS=[('blog', "/blog.html"),
           ('getting started', "/pages/gettingstarted.html"),
           ('documentation', "http://pywren.io/docs"),
           ("examples", "https://github.com/pywren/examples/"), 
           ("code", "http://github.com/pywren/pywren"), 
           ("bugs", "https://github.com/pywren/pywren/issues"), 
]
GITHUB_URL="http://github.com/pywren/pywren"

# PLUGINS = ['summary', 'i18n_subsites', 'liquid_tags.img', 'liquid_tags.video',
#                           'liquid_tags.youtube', 'render_math',
#              'liquid_tags.include_code', 
#              'liquid_tags.literal', 'tipue_search']
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}


# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False
EXTRA_TEMPLATES_PATHS=['./']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
#DIRECT_TEMPLATES=['index', 'categories', 'authors', 'archives', 'test']
#TEMPLATE_PAGES = {'test.html': 'pages/test.html', }

BANNER=True
BANNER_ALL_PAGES=False


# from http://stackoverflow.com/a/30030492

STATIC_PATHS = ['extras', 'images']

EXTRA_PATH_METADATA = {
    'extras/custom.css': {'path': 'static/custom.css'}
}

CUSTOM_CSS = 'static/custom.css'

INDEX_SAVE_AS = 'blog.html'

PYGMENTS_STYLE='friendly'

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'fooo', 'lalala' : "whatever"},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}
