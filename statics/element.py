""" Element."""

from ordereddict import OrderedDict

from statics.tree import externalmap
from statics.tree import TreeMixin
from statics.item import Item
from statics.item import ContentItem
from statics.item import BinaryItem
from statics.util import cached_property

__all__ = ["Element", "ContentElement", "BinaryElement", "ContentItemElement",
           "TemplatedElementMixin", "items_to_elements"]


class Element(TreeMixin):
    """ Element."""

    def __init__(self, name, extension=None, children=None):
        self.name = name
        self.extension = extension
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


class ContentItemElement(ContentElement):
    """ Content element, that wraps ContentItem object."""

    def __init__(self, item, extension=None, children=None):
        super(ContentItemElement, self).__init__(item.name,
                                                 extension=extension,
                                                 children=children)
        self.item = item

    @cached_property
    def metadata(self):
        return self.item.metadata()

    @cached_property
    def content(self):
        return self.item.content()

    def render(self):
        return self.content


class TemplatedElementMixin(object):
    """ ContentElement mixin that is provide content by rendering template.

    This mixin assumes element store template object in ``template`` attribute.
    """

    def get_context(self):
        raise NotImplementedError()

    def render(self):
        return self.template.render(self.get_context())


class BinaryElement(Element):
    """ Element, that wraps binary content."""

    def __init__(self, filename, name, extension=None, children=None):
        super(BinaryElement, self).__init__(name, extension=extension,
                                            children=children)
        self.filename = filename


def items_to_elements(fun, item):
    """ Map items to elements.

    Like :function:`statics.tree.externalmap` but implicitely converts all
    items to elements.
    """
    def fun_(item):
        maybe_element = fun(item)
        if isinstance(maybe_element, BinaryItem):
            return BinaryElement(item.filename, item.name)
        elif isinstance(maybe_element, ContentItem):
            return ContentItemElement(item)
        elif isinstance(maybe_element, Item):
            return Element(maybe_element.name)
        return maybe_element
    return externalmap(fun_, item)
