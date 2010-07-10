""" Define and work with tree-like structured data."""

from UserDict import DictMixin

from zope.proxy import ProxyBase
from zope.proxy import getProxiedObject
from zope.proxy import non_overridable

__all__ = ["TreeMixin", "TreeView", "externalmap"]


class TreeMixin(object, DictMixin):
    """ Mixin for classes that represent as tree-like data structures.

    This mixin assumes you store children in `children` dict attribute and
    parent in `parent` and node name in `name`. For accessing children there is
    dictionary-like interface.
    """

    @property
    def is_leaf(self):
        """ Indicates if node has no children."""
        return not self.children

    @property
    def location(self):
        """ Node location inside tree."""
        if self.parent is None:
            return "/"
        if self.parent.parent is None:
            return "/%s" % self.name
        return "%s/%s" % (self.parent.location, self.name)

    def locate(self, location):
        """ Locate children by location in form of URI."""
        if location and location[0] == "/":
            location = location[1:]
        if not location:
            return self
        current = self
        for part in location.split("/"):
            if part:
                current = current[part]
        return current

    def setlocation(self, location, tree):
        if location and location[-1] == "/":
            location = location[:-1]
        try:
            location, name = location.rsplit("/", 1)
        except ValueError: # ... value to unpack
            raise ValueError("Location should not point to root node.")
        node = self.locate(location)
        node[name] = tree

    def __setitem__(self, name, child):
        """ Set children by name.

        Also see :class:`UserDict.DictMixin`.
        """
        child.parent = self
        self.children[name] = child

    def __getitem__(self, name):
        """ Get item by name.

        Also see :class:`UserDict.DictMixin`.
        """
        return self.children[name]

    def __delitem__(self, name):
        """ Delete item by name.

        Also see :class:`UserDict.DictMixin`.
        """
        child = self.children.pop(name)
        child.parent = None
        return child

    def keys(self):
        """ See :class:`UserDict.DictMixin`."""
        return self.children.keys()

    def __contains__(self, name):
        """ See :class:`UserDict.DictMixin`."""
        return name in self.children


class TreeView(ProxyBase):
    """ View for tree, that provide immutability and can restrict tree to its
    subtree."""

    # XXX: Very inefficient implementation, but I don't care right now.

    __slots__ = ("exclude", )

    def __new__(cls, tree, exclude=None):
        return ProxyBase.__new__(cls, tree)

    def __init__(self, tree, exclude=None):
        self.exclude = exclude

    @non_overridable
    def __setitem__(self, name, child):
        raise TypeError()

    @non_overridable
    def __delitem__(self, name):
        raise TypeError()

    @non_overridable
    def keys(self):
        proxied =  getProxiedObject(self)
        return [k for k in proxied.keys()
                    if not proxied[k].location in self.exclude]

    @non_overridable
    def __getitem__(self, name):
        child = getProxiedObject(self)[name]
        if child.location in self.exclude:
            raise KeyError()
        return type(self)(child, exclude=self.exclude)

    @non_overridable
    def __contains__(self, name):
        proxied =  getProxiedObject(self)
        return name in proxied and not proxied[name].location in self.exclude


def externalmap(fun, tree):
    """ Map to `tree` to another tree by applying `fun` to each node and
    treating the result as resulting node.

    Resulting tree structure maybe superset of original tree.
    """
    queue = [(None, None, tree)]
    root = None
    while queue:
        name, parent, node = queue.pop(0)
        mapped_node = fun(node)
        if not parent is None:
            parent[name] = mapped_node
        else:
            root = mapped_node
        for child_name, child in node.items():
            queue.append((child_name, mapped_node, child))
    return root
