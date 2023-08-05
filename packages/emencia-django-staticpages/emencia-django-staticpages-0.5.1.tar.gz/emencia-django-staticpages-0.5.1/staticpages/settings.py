"""
Default application settings
----------------------------

These are the default settings you can override in your own project settings.

"""

STATICPAGES = []
"""
List of page definition to mount as urls.

It should be something like this: ::

    STATICPAGES = [
        "index",
        {
            "template_path": "bar/foo.html",
            "name": "foo",
            "extra": "free for use",
        },
    ]

Where each item is a static page item to mount as an url. A static page item can be
either a simple string which is the page template name or it can be a dictionnary to
define one or more page options.
"""

STATICPAGES_DEFAULT_TEMPLATEPATH = "staticpages"
"""
Template directory path to use as default prefix for every page template path. It is a
relative path to your 'templates' directory without ending slash.

If not empty, the staticpage loader will prefix every template path with this value,
except if ``template_basepath`` is given to the loader.
"""

STATICPAGES_DEFAULT_NAME_BASE = ""
"""
Default base name that will be prefixed to the page url name.

If not empty, the staticpage loader will prefix every page urlname with this value,
except if ``name_base`` is given to the loader.
"""

STATICPAGES_DEFAULT_URLPATH = None
"""
Default base path that will be prefixed to the page url path. It is a relative url path
so no leading or ending slash (it will be joined automatically with a slash to page
path).

If not empty, the staticpage loader will prefix every page url with this value,
except if ``url_basepath`` is given to the loader.
"""

STATICPAGES_INDEX_NAME = "index"
"""
URL name which qualify a staticpage as an index page.

We check it against the page urlname (without possible urlname prefix) to mark page as
an index and also to change the url path to ``/``.
"""
