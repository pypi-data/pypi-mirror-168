"""
Sub URL configuration to test mounting created urls from registries
"""

from staticpages.loader import StaticpagesLoader


staticpages_loader = StaticpagesLoader(template_basepath="sub")


# Add pages urls using the same template
urlpatterns = staticpages_loader.build_urls([
    "index",
    {
        "template_path": "index.html",
        "name": "plif",
    },
])
