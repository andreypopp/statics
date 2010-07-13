""" Tests for :module:`statics.build`."""

import unittest

from statics.tests.util import TestWithLocalRegistry

__all__ = ["TestBuild"]


class TestBuild(unittest.TestCase, TestWithLocalRegistry):

    def createItem(self):
        from statics.item import Item
        return Item("root", [
            Item("a"),
            Item("b", [
                Item("ba"),
                Item("bb")]),
            Item("c")])

    def test_it(self):
        def dummy_script1(site, config, item):
            def fun(item):
                from statics.element import Element
                return Element(item.name)
            from statics.tree import externalmap
            return externalmap(fun, item)

        def dummy_script2(site, config, item):
            element = dummy_script1(site, config, item)
            from statics.element import Element
            element["added"] = Element("added")
            return element

        from statics.configuration import add_script
        add_script("script1", dummy_script1)
        add_script("script2", dummy_script2)
        site = None
        locations = [("/", {}, "script1"), ("/b", {}, "script2")]
        root_item = self.createItem()
        from statics.build import build
        root_element = build(site, root_item, locations=locations)
        self.assertTrue("a" in root_element)
        self.assertTrue("b" in root_element)
        self.assertTrue("c" in root_element)
        self.assertTrue(not "added" in root_element)
        b_element = root_element["b"]
        self.assertTrue("ba" in b_element)
        self.assertTrue("bb" in b_element)
        self.assertTrue("added" in b_element)

    def test_no_root_script(self):
        locations = [("/b", {}, "script2")]
        root_item = self.createItem()
        site = None
        from statics.build import build
        self.assertRaises(ValueError, build,site,root_item, locations=locations)

    def test_no_script_fount(self):
        locations = [("/", {}, "script")]
        root_item = self.createItem()
        site = None
        from statics.build import build
        self.assertRaises(ValueError, build,site,root_item, locations=locations)
