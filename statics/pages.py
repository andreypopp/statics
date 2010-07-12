""" Pages script."""

# TODO: This is subject to refactoring.

from statics.element import externalmapitem
from statics.element import ContentElement
from statics.item import ContentItem
from statics.util import cached_property

__all__ = ["pages", "Page"]


class Page(ContentElement):

    def __init__(self, item, template):
        super(Page, self).__init__(item.name)
        self.item = item
        self.template = template

    @cached_property
    def content(self):
        return self.item.content()

    @cached_property
    def metadata(self):
        return self.item.metadata()

    @property
    def title(self):
        return self.metadata.get("title")

    def render(self):
        return self.template.render({"page": self})


def pages(site, config, item):
    template = site.templates.get_template(config["template"])
    def make_page(item):
        if isinstance(item, ContentItem):
            return Page(item, template)
        return item
    return externalmapitem(make_page, item)
