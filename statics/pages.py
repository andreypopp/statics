""" Pages script."""

from statics import element
from statics.item import ContentItem

__all__ = ["pages", "Page"]


class Page(element.TemplatedElementMixin, element.ContentItemElement):

    def __init__(self, item, site, template, children=None):
        element.ContentItemElement.__init__(self, item, children=children)
        self.site = site
        self.template = template
        self.title = self.metadata.get("title")

    def get_context(self):
        return {"page": self, "site": self.site}


def pages(site, config, item):
    template = site.templates.get_template(config["template"])
    def make_page(item):
        if isinstance(item, ContentItem):
            return Page(item, site, template)
        return item
    return element.items_to_elements(make_page, item)
