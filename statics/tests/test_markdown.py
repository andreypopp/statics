""" Tests for :module:`statics.markdown`."""

import unittest

__all__ = ["TestMarkdownItem"]


class TestMarkdownItem(unittest.TestCase):

    def createFile(self, content):
        import tempfile
        f = tempfile.NamedTemporaryFile()
        f.write(content)
        f.flush()
        return f

    def test_it(self):
        from statics.markdown import MarkdownItem
        f = self.createFile("some markdown document.")
        item = MarkdownItem("name", f.name)
        self.assertEqual(item.name, "name")
        self.assertEqual(item.metadata(), {})
        self.assertEqual(item.content(), "<p>some markdown document.</p>")

    def test_with_metadate(self):
        from statics.markdown import MarkdownItem
        f = self.createFile("Title: A Title\nList: Value1\n\tValue2\n\ncontent")
        item = MarkdownItem("name", f.name)
        self.assertEqual(item.name, "name")
        self.assertEqual(item.metadata(), {"title": "A Title",
                                           "list": ["Value1", "Value2"]})
        self.assertEqual(item.content(), "<p>content</p>")
