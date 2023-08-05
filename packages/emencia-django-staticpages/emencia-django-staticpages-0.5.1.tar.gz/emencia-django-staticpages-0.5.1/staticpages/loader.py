"""
.. _loader_docstring_args:

Loader
======

Loader is in charge to resolve page item options and to create UrlPattern objects from
a given page registry.

Basically you could use it like this: ::

    staticpages_loader = StaticpagesLoader()
    staticpages_loader.build_urls()

This will return you a list of UrlPattern objects, note than without any argument
the loader will use the settings for default values from settings and especially
the setting ``STATICPAGES``.

In the following sample, you can see a more concrete way that will build
UrlPattern objects directly mounted as urls, something you can use in a Django
``urls.py``: ::

    staticpages_loader = StaticpagesLoader()

    urlpatterns = [
        ...
        # Add pages urls using the same template
        *staticpages_loader.build_urls([
            "index",
            "foo",
            "bar",
        ])
    ]

That will respectively configure pages on urls ``/``, ``/foo/`` and ``/bar/``.

"""
import os

from django.conf import settings
from django.urls import path, re_path

from .exceptions import StaticpagesResolverError
from .views import StaticPageView


class StaticpagesLoader:
    """
    A ``TemplateView`` inheriter with some more attributes to implement staticpages
    features.

    Keyword Arguments:
        template_basepath (string): Path to prefix a page template path.
            If empty, default value comes from ``STATICPAGES_DEFAULT_TEMPLATEPATH``
            setting.
        name_base (string): Name to prefix a page url name. If empty, default
            value comes from ``STATICPAGES_DEFAULT_NAME_BASE`` setting.
        url_basepath (string): Base url path to prefix a page url path. If empty,
            default value comes from ``STATICPAGES_DEFAULT_URLPATH`` setting.
        view_class (object): A Class based view to use instead of the default
            ``staticpages.views.StaticPageView`` that is an extend of Django class
            base view ``TemplateView``. Given class must respect expected
            attributes ``template_name``, ``page_options`` and ``staticpages``.
    """
    def __init__(self, template_basepath=None, name_base=None, url_basepath=None,
                 view_class=None):
        self.template_basepath = (
            template_basepath or settings.STATICPAGES_DEFAULT_TEMPLATEPATH
        )
        self.name_base = name_base or settings.STATICPAGES_DEFAULT_NAME_BASE
        self.url_basepath = url_basepath or settings.STATICPAGES_DEFAULT_URLPATH
        self.view_class = view_class or StaticPageView

    def validate_item(self, data):
        """
        Validate item data is correct.

        Arguments:
            data (dict): Item options to validate. See ``resolve_item`` for expected
                data.
        """
        if "template" not in data and "template_path" not in data:
            raise StaticpagesResolverError((
                "Either 'template' or 'template_path' must be defined in a staticpage "
                "registry item."
            ))

        if data.get("template_path") and "name" not in data:
            raise StaticpagesResolverError((
                "When a staticpage registry item defines 'template_path' the 'name' "
                "option must be defined too."
            ))

    def _is_index(self, data, payload):
        """
        Resolve if item is an index or not.

        Arguments:
            data (dict): Given item options to perform resolving. See ``resolve_item``
                for expected data.
            payload (dict): Resolved item options.

        Returns:
            bool: True if an index, else False.
        """
        return payload["name"] == settings.STATICPAGES_INDEX_NAME

    def _is_regex(self, data, payload):
        """
        Resolve if item path is a regex.

        Arguments:
            data (dict): Given item options to perform resolving. See ``resolve_item``
                for expected data.
            payload (dict): Resolved item options.

        Returns:
            bool: True if a regex, else False.
        """
        return data.get("re_path") not in ("", None)

    def _resolve_template(self, data, payload):
        """
        Resolve template path from options.

        Arguments:
            data (dict): Given item options to perform resolving. See ``resolve_item``
                for expected data.
            payload (dict): Resolved item options.

        Returns:
            string: Resolved template path.
        """
        # 'template_path' option have highest priority.
        if "template_path" in data:
            resolved_template = data["template_path"]
        # Else we use 'template' option with HTML extension suffix
        else:
            resolved_template = "{}.html".format(data["template"])

        # Finally prefix with template basepath if not empty
        if self.template_basepath:
            resolved_template = os.path.join(
                self.template_basepath,
                resolved_template
            )

        return resolved_template

    def _resolve_name(self, data, payload):
        """
        Resolve name from options.

        Arguments:
            data (dict): Given item options to perform resolving. See ``resolve_item``
                for expected data.
            payload (dict): Resolved item options.

        Returns:
            string: Resolved name.
        """
        return data.get("name") or data["template"]

    def _resolve_urlname(self, data, payload):
        """
        Resolve url name from options.

        Arguments:
            data (dict): Given item options to perform resolving. See ``resolve_item``
                for expected data.
            payload (dict): Resolved item options.

        Returns:
            string: Resolved url name.
        """
        urlname = payload["name"]

        if self.name_base:
            urlname = "{}{}".format(self.name_base, urlname)

        return urlname

    def _resolve_path(self, data, payload):
        """
        Resolve url path from options.

        Arguments:
            data (dict): Given item options to perform resolving. See ``resolve_item``
                for expected data.
            payload (dict): Resolved item options.

        Returns:
            string: Resolved url path.
        """
        if payload["is_index"]:
            path = ""
        else:
            path = (
                data.get("re_path") or
                data.get("path", "{}/".format(payload["name"]))
            )

        if self.url_basepath:
            path = os.path.join(self.url_basepath, path)

        return path

    def resolve_item(self, data):
        """
        Resolve a registry item.

        Expected data may be something like: ::

            {
                "path": "foo/",
                "re_path": r"foo/$",
                "template": "foo",
                "template_path": "foo.html",
                "name": "foo",
                "extra": "anything anykind",
            }

        See :ref:`Option specifications <usage_options_specs>` for more details.

        Arguments:
            data (dict): Item options.
            Returns:
                dict: A dictionnary of resolved options. See
                :ref:`usage_template_context` for more details.
        """
        self.validate_item(data)

        payload = {}

        payload["template"] = self._resolve_template(data, payload)
        payload["name"] = self._resolve_name(data, payload)
        payload["is_index"] = self._is_index(data, payload)
        payload["urlname"] = self._resolve_urlname(data, payload)
        payload["is_regex"] = self._is_regex(data, payload)
        payload["path"] = self._resolve_path(data, payload)

        # Optional extra context to pass to view
        payload["extra"] = data.get("extra", None)

        return payload

    def resolve_registry(self, registry=None):
        """
        From given registry, resolve each registry item to a tuple suitable to build
        urls.

        Keyword Arguments:
            registry (list): List of either string or dict. Dictionnary is the verbose
                way to define options opposed to a String which is expected to be a
                template name (without leading path and ending HTML suffix) that will
                be used to resolve options. If this argument is empty, default value
                will comes from ``STATICPAGES`` setting.

        Returns:
            list: A list of item options as dictionnary.
        """
        resolved = []

        registry = registry or settings.STATICPAGES

        # TODO: An error may be raised if there is duplicate path or url name ?

        for item in registry:
            # If a simple string, resolve every options
            if isinstance(item, str):
                resolved.append(
                    self.resolve_item({"template": item})
                )
            # Assume it's a dict with one or more options
            else:
                resolved.append(
                    self.resolve_item(item)
                )

        return resolved

    def build_url(self, page, pages):
        """
        Build an url object for given page item.

        Arguments:
            page (dict): Page options.
            pages (list): List of all pages options.

        Returns:
            django.urls.resolvers.URLPattern: URLPattern object to mount in urls.
        """
        # Use the right object to define url depending it's a regex path or not
        path_object = path
        if page["is_regex"]:
            path_object = re_path

        view = self.view_class.as_view(
            template_name=page["template"],
            page_options=page,
            staticpages=pages,
        )

        url_object = path_object(page["path"], view, name=page["urlname"])

        return url_object

    def build_urls(self, registry=None):
        """
        Build view url objects for page registry.

        Keyword Arguments:
            registry (list): List of page items.

        Returns:
            list: List of URLPattern objects.
        """
        resolved = self.resolve_registry(registry=registry)

        urls = []

        for item in resolved:
            urls.append(
                self.build_url(item, resolved)
            )

        return urls
