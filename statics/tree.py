""" Define and work with tree-like structured data.

This module provides :class:`TreeMixin`, :class:`TreeView` and a couple of
useful functions to work with trees.
"""

from UserDict import DictMixin

from zope.proxy import ProxyBase
from zope.proxy import getProxiedObject
from zope.proxy import non_overridable

__all__ = ["TreeMixin", "TreeView", "externalmap", "print_tree"]


class TreeMixin(object, DictMixin):
    """ Mixin for classes that represent tree-like data structures.

    This mixin assumes you store children nodes in `children` dict-like
    attribute, parent node in `parent` attribute and node name in `name`.

    This mixin inherits from :class:`UserDict.DictMixin` to provide dict-like
    interface to node's children.

    For uses of this mixin see :class:`statics.item.Item` and
    :class:`statics.element.Element` classes.
    """

    @property
    def is_leaf(self):
        """ Property, that is true if node has no children."""
        return not self.children

    @property
    def location(self):
        """ Node location inside tree.

        Node's location is a string that is like an XPath location.
        """
        if self.parent is None:
            return "/"
        if self.parent.parent is None:
            return "/%s" % self.name
        return "%s/%s" % (self.parent.location, self.name)

    def locate(self, location):
        """ Locate children inside node by providing its location."""
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
        """ Set `tree` node at specified `location` inside current node."""
        if location and location[-1] == "/":
            location = location[:-1]
        try:
            location, name = location.rsplit("/", 1)
        except ValueError: # ... value to unpack
            raise ValueError("Location should not point to root node.")
        node = self.locate(location)
        node[name] = tree

    def __setitem__(self, name, child):
        """ Set children to node.

        Also see :class:`UserDict.DictMixin`.
        """
        child.parent = self
        child.name = name
        self.children[name] = child

    def __getitem__(self, name):
        """ Get node's children by name.

        Also see :class:`UserDict.DictMixin`.
        """
        return self.children[name]

    def __delitem__(self, name):
        """ Delete children from node by name.

        Also see :class:`UserDict.DictMixin`.
        """
        child = self.children.pop(name)
        child.parent = None
        return child

    def keys(self):
        """ Return names of all node's children.

        Also see :class:`UserDict.DictMixin`.
        """
        return self.children.keys()

    def __contains__(self, name):
        """ Returns true if node has child with specified `name`.

        Also see :class:`UserDict.DictMixin`."""
        return name in self.children


class TreeView(ProxyBase):
    """ View for tree.

    View is used to force immutability on tree data structure and possible to
    restrict tree to specified subtree.
    """

    # XXX: Very inefficient implementation, but I don't care right now.

    __slots__ = ("exclude", "_view_root_location")

    def __new__(cls, tree, exclude=None, _view_root_location=None):
        return ProxyBase.__new__(cls, tree)

    def __init__(self, tree, exclude=None, _view_root_location=None):
        """ Initialize tree view.

        View initialized by providing `tree` node that would be used as view's
        root node. Also there is `exlude` argument that is actually can be any
        iterable of locations inside `tree` for those access would restricted.
        """
        if exclude is None:
            exclude = []
        if _view_root_location is None:
            _view_root_location = self.location
        self.exclude = exclude
        self._view_root_location = _view_root_location

    def _proxy_to(self, obj):
        return type(self)(obj, exclude=self.exclude,
            _view_root_location=self._view_root_location)

    @property
    def parent(self):
        proxied = getProxiedObject(self)
        if self.location == self._view_root_location:
            return None
        return self._proxy_to(proxied.parent)

    @non_overridable
    def __getitem__(self, name):
        child = getProxiedObject(self)[name]
        if child.location in self.exclude:
            raise KeyError()
        return self._proxy_to(child)

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


def print_tree(tree, ident=0):
    """ Print `tree` on stdout.

    Maybe useful for debugging.
    """
    if ident:
        print ident*" ", tree
    else:
        print tree
    for child in tree.values():
        print_tree(child, ident=ident+1)
