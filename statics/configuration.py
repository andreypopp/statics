""" Configuration routines."""

from zope.component import getSiteManager
from zope.interface import implementedBy

from statics.interfaces import IItemFactory
from statics.interfaces import IScript

__all__ = ["add_item_factory", "query_item_factory", "add_script",
           "query_script"]


def add_item_factory(extension, item_factory):
    """ Register item factory for extension."""
    registry = getSiteManager()
    return registry.registerUtility(item_factory, IItemFactory, name=extension)


def query_item_factory(extension, default=None):
    registry = getSiteManager()
    factory = registry.queryUtility(IItemFactory, name=extension,
        default=default)
    return factory


def add_script(name, script):
    """ Register script by name."""
    registry = getSiteManager()
    return registry.registerUtility(script, IScript, name=name)


def query_script(name, default=None):
    """ Query script by name."""
    registry = getSiteManager()
    return registry.queryUtility(IScript, name=name, default=default)
