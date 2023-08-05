"""
URL Configuration to test mounting created urls from registries
"""
from django.contrib import admin
from django.urls import include, path

from staticpages.loader import StaticpagesLoader


staticpages_loader = StaticpagesLoader()


urlpatterns = [
    path("admin/", admin.site.urls),
    # Add base pages urls using the same template
    *staticpages_loader.build_urls([
        "index",
        {
            "template_path": "index.html",
            "name": "foo",
            "extra": "free for use",
        },
    ])
]

# Include another urls map on a sub path
urlpatterns.append(
    path("sub/", include("sandbox.staticpages_testapp.sub_urls")),
)
