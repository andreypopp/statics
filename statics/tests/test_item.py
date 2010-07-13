""" Tests for :module:`statics.item`."""

import unittest

__all__ = []


class TestItem(unittest.TestCase):

    def test_it(self):
        from statics.item import Item
        item = Item("root", [Item("a"), Item("b", [Item("ba"), Item("bb")])])
        self.assertEqual(item.name, "root")
        self.assertEqual(item.parent, None)
        self.assertEqual(len(item), 2)
        self.assertTrue("a" in item)
        self.assertTrue("b" in item)
        b = item["b"]
        self.assertEqual(b.name, "b")
        self.assertEqual(b.parent, item)
        self.assertEqual(len(b), 2)
        self.assertTrue("ba" in b)
        self.assertTrue("bb" in b)
        ba = b["ba"]
        self.assertEqual(ba.name, "ba")
        self.assertEqual(ba.parent, b)
        self.assertEqual(len(ba), 0)
        bb = b["bb"]
        self.assertEqual(bb.name, "bb")
        self.assertEqual(bb.parent, b)
        self.assertEqual(len(bb), 0)


class TestBinaryItem(unittest.TestCase):

    def test_it(self):
        from statics.item import BinaryItem
        item = BinaryItem("name", "filename")
        self.assertEqual(item.name, "name")
        self.assertEqual(item.parent, None)
        self.assertEqual(len(item), 0)
        self.assertEqual(item.filename, "filename")


class TestContentItem(unittest.TestCase):

    def test_it(self):
        from statics.item import ContentItem
        import tempfile
        content_file = tempfile.NamedTemporaryFile()
        content_file.write("content")
        content_file.flush()
        item = ContentItem("name", content_file.name)
        self.assertEqual(item.name, "name")
        self.assertEqual(item.parent, None)
        self.assertEqual(len(item), 0)
        self.assertEqual(item.filename, content_file.name)
        self.assertEqual(item.metadata(), {})
        self.assertEqual(item.content(), "content")
