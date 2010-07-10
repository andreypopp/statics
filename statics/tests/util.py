""" Test utilities."""

from zope.component import getSiteManager
from zope.component.registry import Components

__all__ = ["TestWithLocalRegistry"]


class TestWithLocalRegistry(object):

    def setUp(self):
        registry = Components()
        getSiteManager.set_hook(lambda: registry)

    def tearDown(self):
        getSiteManager.reset()
