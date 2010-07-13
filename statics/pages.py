""" Pages script."""

from statics.element import items_to_elements
from statics.element import ContentItemElement
from statics.item import ContentItem

__all__ = ["pages", "Page"]


class Page(ContentItemElement):

    def __init__(self, item, site, template, children=None):
        super(Page, self).__init__(item, children=children)
        self.site = site
        self.template = template

    @property
    def title(self):
        return self.metadata.get("title")

    def get_context(self):
        return {"page": self, "site": self.site}

    def render(self):
        context = self.get_context()
        return self.template.render(context)


def pages(site, config, item):
    template = site.templates.get_template(config["template"])
    def make_page(item):
        if isinstance(item, ContentItem):
            return Page(item, site, template)
        return item
    return items_to_elements(make_page, item)
