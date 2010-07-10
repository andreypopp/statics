""" Tests for :module:`statics.site`."""

import unittest

__all__ = ["TestSite"]


class TestSite(unittest.TestCase):

    def test_locations(self):
        from statics.site import Site
        site = Site({
            "location:/": {"name": "location_root", "k": "v"},
            "location:/a": {"name": "location_a", "k1": "v1"}})
        locations = dict((l, (n, c)) for (l, c, n) in site.locations)
        self.assertEqual(len(locations), 2)
        self.assertTrue("/" in locations)
        location_root = locations["/"]
        self.assertEqual(("location_root", {"k": "v"}), location_root)
        self.assertTrue("/a" in locations)
        location_a = locations["/a"]
        self.assertEqual(("location_a", {"k1": "v1"}), location_a)
