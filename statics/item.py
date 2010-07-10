""" Item."""

from ordereddict import OrderedDict

from statics.tree import TreeMixin

__all__ = ["Item", "BinaryItem", "ContentItem"]


class Item(TreeMixin):

    def __init__(self, name, children=None):
        self.name = name
        self.children = OrderedDict()
        self.parent = None

        if children is None:
            children = []
        for child in children:
            self[child.name] = child

    def __repr__(self):
        return "<%s %s at %s>" % (
            self.__class__.__name__, self.name, self.location)


class BinaryItem(Item):

    def __init__(self, name, children=None, filename=None):
        super(BinaryItem, self).__init__(name, children=children)
        self.filename = filename


class ContentItem(Item):

    def __init__(self, name, children=None, filename=None):
        super(ContentItem, self).__init__(name, children=children)
        self.filename = filename

    def metadata(self):
        return {}

    def content(self):
        return self.content_provider()

    def content_provider(self):
        return open(self.filename, "r").read()
