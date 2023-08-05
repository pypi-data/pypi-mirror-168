"""
Views
=====

Implemented view is a basic view which inherits from
``django.views.generic.TemplateView`` to add some additional attribute and extend the
template context.

If needed you can define another class based view to use with loader argument
``view_class``.
"""
from django.views.generic import TemplateView


class StaticPageView(TemplateView):
    """
    Simple template view with some additional arguments related to staticpages.

    Attributes:
        page_options (dict): Resolved current page options. Will be passed to context
            in ``page_options`` variable. Default to empty dictionnary.
        staticpages (list): Resolved page items registry (including current page
            itself). Will be passed to context in ``staticpages`` variable. Default to
            empty list.
        give_staticpages (boolean): Determine if registry must be passed to template
            context or not. If not, ``staticpages`` variable won't be available from
            context. Default is true, this variable is always filled.
    """
    page_options = {}
    staticpages = []
    give_staticpages = True

    def get_context_data(self, **kwargs):
        """
        Extend template context with current page options in ``page_options`` variable
        and possible static page list in ``staticpages`` variable depending value of
        attribute ``give_staticpages``.
        """
        context = super(StaticPageView, self).get_context_data(**kwargs)

        context.update({
            "page_options": self.page_options,
        })

        if self.give_staticpages and self.staticpages:
            context.update({
                "staticpages": self.staticpages,
            })
        return context
