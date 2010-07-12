""" Tests for :module:`statics.tree`."""

import unittest

from statics.tree import TreeMixin

__all__ = ["TestTreeMixin", "TestExternalMap", "TestLineage"]


class Tree(TreeMixin):

    def __init__(self, name, data=None, **children):
        self.name = name
        self.data = data
        self.parent = None
        self.children = {}
        for child_name, child in children.items():
            self[child_name] = child


def createTestTree():
    root = Tree(None,
        a=Tree("a",
            aa=Tree("aa"),
            ab=Tree("ab")),
        b=Tree("b"),
        c=Tree("c"))
    return root


class TestTreeMixin(unittest.TestCase):

    def test___getitem__(self):
        root = createTestTree()
        a = root["a"]
        self.assertTrue(a.parent is root)
        self.assertTrue(isinstance(a, Tree))
        self.assertRaises(KeyError, root.__getitem__, "d")

    def test___setitem__(self):
        root = createTestTree()
        d = Tree("d")
        root["d"] = d
        self.assertTrue(d.parent is root)
        d_ = root["d"]
        self.assertTrue(d is d_)
        c = Tree("c")
        c_ = root["c"]
        root["c"] = c
        c__ = root["c"]
        self.assertTrue(not c__ is c_)
        self.assertTrue(c__ is c)

    def test___delitem__(self):
        root = createTestTree()
        del root["c"]
        self.assertRaises(KeyError, root.__getitem__, "c")

    def test_keys(self):
        root = createTestTree()
        self.assertTrue("a" in root.keys())
        self.assertTrue("b" in root.keys())
        self.assertTrue("c" in root.keys())

    def test___contains__(self):
        root = createTestTree()
        self.assertTrue("a" in root)
        self.assertTrue("b" in root)
        self.assertTrue("c" in root)

    def test_locate(self):
        root = createTestTree()
        self.assertEqual(root, root.locate(""))
        self.assertEqual(root, root.locate("/"))
        self.assertEqual(root, root.locate("//"))
        self.assertEqual(root["a"], root.locate("/a"))
        self.assertEqual(root["a"], root.locate("/a/"))
        self.assertEqual(root["b"], root.locate("/b"))
        self.assertEqual(root["b"], root.locate("//b"))
        self.assertEqual(root["a"]["aa"], root.locate("/a/aa"))

    def test_location(self):
        root = createTestTree()
        self.assertEqual(root.location, "/")
        self.assertEqual(root["a"].location, "/a")
        self.assertEqual(root["b"].location, "/b")
        self.assertEqual(root["a"]["aa"].location, "/a/aa")

    def test_setlocation(self):
        root = createTestTree()
        root2 = createTestTree()
        root.setlocation("/d", root2)
        self.assertTrue("d" in root)
        self.assertTrue("a" in root["d"])
        self.assertTrue("aa" in root["d"]["a"])

        self.assertRaises(ValueError, root.setlocation, "/", root2)
        self.assertRaises(ValueError, root.setlocation, "", root2)

        self.assertRaises(KeyError, root.setlocation, "/e/a", root2)


class TestTreeView(unittest.TestCase):

    def test___setitem__(self):
        from statics.tree import TreeView
        tree = createTestTree()
        view = TreeView(tree)
        def setitem():
            view["a"] = "b"
        self.assertRaises(TypeError, setitem)

    def test___delitem__(self):
        from statics.tree import TreeView
        tree = createTestTree()
        view = TreeView(tree)
        def delitem():
            del view["a"]
        self.assertRaises(TypeError, delitem)

    def test_excluded_view(self):
        from statics.tree import TreeView
        tree = createTestTree()
        view = TreeView(tree, exclude=["/a/aa", "/c"])
        self.assertEqual(view.location, "/")
        self.assertTrue("a" in view)
        self.assertTrue("b" in view)
        self.assertTrue(not "c" in view)
        self.assertTrue(not "c" in view.keys())
        def getitem_c():
            return view["c"]
        self.assertRaises(KeyError, getitem_c)
        view_a = view["a"]
        self.assertTrue(not "aa" in view_a)
        self.assertTrue("ab" in view_a)
        self.assertTrue(not "aa" in view_a.keys())
        def getitem_a_aa():
            return view_a["aa"]
        self.assertRaises(KeyError, getitem_a_aa)
        self.assertTrue(not "aa" in view_a.parent["a"])

    def test_child_view(self):
        from statics.tree import TreeView
        tree = createTestTree()
        view = TreeView(tree["a"])
        self.assertTrue("aa" in view)
        self.assertTrue("ab" in view)
        self.assertTrue(view.parent is None)
        self.assertEqual(view.location, "/a")
        self.assertEqual(view["aa"].location, "/a/aa")

class TestExternalMap(unittest.TestCase):

    def test_it(self):
        from statics.tree import externalmap
        root = Tree("root", 1,
                    a=Tree("a", 2,
                           aa=Tree("aa", 3),
                           ab=Tree("ab", 4)),
                    b=Tree("b", 5))
        def fun(node):
            return Tree(node.name, node.data+1)
        mapped = externalmap(fun, root)
        self.assertEqual(mapped.data, 2)
        self.assertEqual(mapped["a"].data, 3)
        self.assertEqual(mapped["a"]["aa"].data, 4)
        self.assertEqual(mapped["a"]["ab"].data, 5)
        self.assertEqual(mapped["b"].data, 6)
