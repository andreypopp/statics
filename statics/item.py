""" Item data structure."""

from ordereddict import OrderedDict

from statics.tree import TreeMixin

__all__ = ["Item", "BinaryItem", "ContentItem"]


class Item(TreeMixin):
    """ Base class for items.

    Objects of that class do not represent any kind of content, but can contain
    other items inside.
    """

    def __init__(self, name, children=None):
        """ Initialize item object with `name` and `children` arguments."""
        self.name = name
        self.children = OrderedDict()
        self.parent = None

        if children is None:
            children = []
        for child in children:
            self[child.name] = child

    def __repr__(self): # pragma: nocover
        return "<%s %s at %s>" % (
            self.__class__.__name__, self.name, self.location)


class BinaryItem(Item):
    """ Item that represent binary content."""

    def __init__(self, name, filename, children=None):
        """ Initialize binary item object with `name`, `children` and
        `filename` arguments.
        """
        super(BinaryItem, self).__init__(name, children=children)
        self.filename = filename


class ContentItem(Item):
    """ Item that represent textual content.

    Objects of this class are also responsible for processing content and
    metadata. It is usual for users of statics framework to subclass this class
    and provide their own implementation of `content` or `metadata` methods.
    """

    def __init__(self, name, filename, children=None):
        """ Initialize binary item object with `name`, `children` and
        `filename` arguments.
        """
        super(ContentItem, self).__init__(name, children=children)
        self.filename = filename

    def metadata(self):
        """ Return item's metadata."""
        return {}

    def content(self):
        """ Return item's content."""
        return self.content_provider()

    def content_provider(self):
        """ Provide raw unprocessed content."""
        return open(self.filename, "r").read()
