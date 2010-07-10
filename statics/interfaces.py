""" Interfaces."""

from zope.interface import Interface

__all__ = ["IItemFactory", "IScript"]


class IItemFactory(Interface):
    """ Factory for items."""

    def __call__(name, children=None, filename=None):
        """ Produce item."""


class IScript(Interface):
    """ Build script."""

    def __call__(site, config, item):
        """ Take tree of items and produce tree of elements."""
