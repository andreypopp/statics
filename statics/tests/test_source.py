""" Tests for :module:`statics.source`."""

import unittest

__all__ = ["TestSource"]


class TestSource(unittest.TestCase):

    def createTemporaryStructure(self, spec, root=None):
        from os import mkdir
        from os.path import join
        from tempfile import mkdtemp
        if root is None:
            root = mkdtemp()
        for name, value in spec.items():
            if isinstance(value, dict):
                new_root = join(root, name)
                mkdir(new_root)
                self.createTemporaryStructure(value, root=new_root)
            else:
                open(join(root, name), "w").write(value)
        return root

    def test_it(self):
        from statics.source import Source
        from statics.item import BinaryItem
        from statics.item import ContentItem
        from statics.item import Item
        from os.path import join
        tempdir = self.createTemporaryStructure({
            "a.html": "data_a.html",
            "binary": "\x00",
            "a": {
                "index.html": "data_index.html",
                "index.txt": "data_index.txt",
                "aa.html": "data_aa.html",
                "aa.txt": "data_aa.txt"
            },
            "static": {},
            "b.html": "data_b.html",
            "c": {},
        })

        source = Source(tempdir, extension_priority=("txt", "html"),
            exclude=[join(tempdir, "static")])

        root = source.root()
        self.assertEqual(root.name, "")
        self.assertEqual(len(root), 5)
        self.assertTrue(isinstance(root, Item))

        self.assertTrue("static" in root)
        static = root["static"]
        self.assertEqual(len(static), 0)
        self.assertTrue(isinstance(static, BinaryItem))

        self.assertTrue("a" in root)
        a = root["a"]
        self.assertEqual(a.content_provider(), "data_index.txt")
        self.assertEqual(len(a), 1)
        self.assertTrue(isinstance(a, ContentItem))

        self.assertTrue("aa" in a)
        aa = a["aa"]
        self.assertEqual(aa.content_provider(), "data_aa.txt")
        self.assertTrue(isinstance(aa, ContentItem))

        self.assertTrue("b" in root)
        b = root["b"]
        self.assertEqual(len(b), 0)
        self.assertEqual(b.content_provider(), "data_b.html")
        self.assertTrue(isinstance(b, ContentItem))

        self.assertTrue("c" in root)
        c = root["c"]
        self.assertEqual(len(c), 0)
        self.assertTrue(isinstance(c, Item))

        self.assertTrue("binary" in root)
        binary = root["binary"]
        self.assertEqual(len(binary), 0)
        self.assertTrue(isinstance(binary, BinaryItem))
        self.assertEqual(binary.filename, join(tempdir, "binary"))

        from shutil import rmtree
        rmtree(tempdir)
