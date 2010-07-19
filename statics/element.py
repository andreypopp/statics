""" Element."""

from ordereddict import OrderedDict

from statics.tree import TreeMixin
from statics.item import Item
from statics.item import ContentItem
from statics.item import BinaryItem
from statics.util import cached_property

from generic.multidispatch import multifunction

__all__ = ["Element", "ContentElement", "BinaryElement", "ContentItemElement",
           "TemplatedElementMixin", "items_to_elements"]


class Element(TreeMixin):
    """ Element."""

    is_content = False
    is_binary = False

    def __init__(self, name, children=None):
        self.name = name
        self.parent = None
        self.children = OrderedDict()

        if children is None:
            children = []
        for child in children:
            self[child.name] = child

    @property
    def link(self):
        return self.location

    def __repr__(self):
        return "<%s at %s>" % (self.__class__.__name__, self.location)


class BinaryElement(Element):
    """ Element, that wraps binary content."""

    is_content = False
    is_binary = True

    @property
    def link(self):
        return self.location

    def __init__(self, filename, name, children=None):
        super(BinaryElement, self).__init__(name, children=children)
        self.filename = filename


class ContentElement(Element):
    """ Element, that wraps textual content."""

    is_content = True
    is_binary = False

    @property
    def link(self):
        if self.is_leaf and self.extension:
            return "%s.%s" % (self.location, self.extension)
        return self.location

    def __init__(self, name, extension="html", children=None):
        Element.__init__(self, name, children=children)
        self.extension = extension

    def render(self):
        """ Render content into HTML."""
        raise NotImplementedError()


class ContentItemElement(ContentElement):
    """ Content element, that wraps ContentItem object."""

    def __init__(self, item, extension="html", children=None):
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


@multifunction(BinaryItem)
def from_item(item):
    return BinaryElement(item.filename, item.name)

@from_item.when(ContentItem)
def from_item(item):
    return ContentItemElement(item)

@from_item.when(Item)
def from_item(item):
    return Element(item.name)
