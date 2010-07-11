""" Pages script."""

# TODO: This is subject to refactoring.

from os.path import dirname
from os.path import basename

from jinja2 import Environment
from jinja2 import FileSystemLoader

from statics.element import externalmapitem
from statics.element import ContentElement
from statics.element import BinaryElement
from statics.element import Element
from statics.item import BinaryItem
from statics.item import ContentItem
from statics.util import cached_property

__all__ = ["pages", "Page"]


def get_template(config):
    template_dir = dirname(config["template"])
    template_name = basename(config["template"])
    environment = Environment(loader=FileSystemLoader(template_dir))
    return environment.get_template(template_name)


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

    def render(self):
        return self.template.render({"page": self})


def pages(site, config, item):
    template = get_template(config)
    def make_page(item):
        if isinstance(item, ContentItem):
            return Page(item, template)
        return item
    return externalmapitem(make_page, item)
