""" Tests for :module:`statics.configuration`."""

import unittest

from statics.tests.util import TestWithLocalRegistry

__all__ = ["TestAddItemFactory", "TestAddQueryScript"]


class TestAddQueryFactory(unittest.TestCase, TestWithLocalRegistry):

    def test_it(self):
        from statics.configuration import query_item_factory
        from statics.configuration import add_item_factory
        class ItemFactory(object):
            pass
        add_item_factory("ext", ItemFactory)
        self.assertEqual(query_item_factory("ext"), ItemFactory)
        self.assertEqual(query_item_factory("ext2"), None)


class TestAddQueryScript(unittest.TestCase, TestWithLocalRegistry):

    def test_it(self):
        from statics.configuration import query_script
        from statics.configuration import add_script
        class Script(object):
            pass
        add_script("name", Script)
        self.assertEqual(query_script("name"), Script)
        self.assertEqual(query_script("name2"), None)
