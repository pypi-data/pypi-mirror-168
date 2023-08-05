"""
Django settings for tests
"""

from sandbox.settings.base import *

TESTS_PATH = join(BASE_DIR, "tests")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {
            "NAME": join(VAR_PATH, "db", "tests.sqlite3"),  # noqa
        }
    }
}


TEMPLATES[0]["DIRS"].extend([
    join(TESTS_PATH, "data_fixtures", "templates", "staticpages_tests"),
])


# Media directory dedicated to tests to avoid polluting other environment
# media directory
MEDIA_ROOT = join(VAR_PATH, "media-tests")


# Neutralize default settings
STATICPAGES = []
STATICPAGES_DEFAULT_TEMPLATEPATH = None
STATICPAGES_DEFAULT_NAME_BASE = None
STATICPAGES_DEFAULT_URLPATH = None
