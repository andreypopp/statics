""" Element."""

from ordereddict import OrderedDict

from statics.tree import TreeMixin
from statics.item import Item
from statics.item import ContentItem
from statics.item import BinaryItem

__all__ = ["Element", "ContentElement", "BinaryElement"]


class Element(TreeMixin):
    """ Element."""

    def __init__(self, name, children=None):
        self.name = name
        self.parent = None
        self.children = OrderedDict()

        if children is None:
            children = []
        for child in children:
            self[child.name] = child


class ContentElement(Element):
    """ Element, that wraps textual content."""

    def render(self):
        """ Render content into HTML."""
        raise NotImplementedError()


class BinaryElement(Element):
    """ Element, that wraps binary content."""

    def __init__(self, filename, name, children=None):
        super(BinaryElement, self).__init__(name, children=children)
        self.filename = filename
