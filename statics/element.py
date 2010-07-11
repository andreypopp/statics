""" Element."""

from ordereddict import OrderedDict

from statics.tree import externalmap
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


class DummyContentElement(ContentElement):

    def __init__(self, content, name, children=None):
        super(DummyContentElement, self).__init__(name, children=children)
        self.content = content

    def render(self):
        return self.content


class BinaryElement(Element):
    """ Element, that wraps binary content."""

    def __init__(self, filename, name, children=None):
        super(BinaryElement, self).__init__(name, children=children)
        self.filename = filename


def externalmapitem(fun, item):
    """ Map items to elements.

    Like :function:`statics.tree.externalmap` but implicitely converts all
    items to elements.
    """
    def fun_(item):
        maybe_element = fun(item)
        if isinstance(maybe_element, BinaryItem):
            return BinaryElement(item.filename, item.name)
        elif isinstance(maybe_element, ContentItem):
            return DummyContentElement(
                maybe_element.content, maybe_element.name)
        elif isinstance(maybe_element, Item):
            return Element(maybe_element.name)
        return maybe_element
    return externalmap(fun_, item)
