""" Source."""

from os import listdir
from os.path import join
from os.path import isdir
from os.path import isfile
from os.path import basename
from os.path import splitext
from os.path import samefile
from sys import maxint
from collections import namedtuple
from ordereddict import OrderedDict

from statics.item import Item
from statics.item import BinaryItem
from statics.item import ContentItem
from statics.configuration import query_item_factory

__all__ = ["get_root"]


ItemInfo = namedtuple("ItemInfo", ["filename", "name", "extension"])


def split(filename):
    if isdir(filename):
        name = basename(filename)
        return name, ""
    elif isfile(filename):
        name, ext = splitext(filename)
        name = basename(name)
        if ext:
            ext = ext[1:]
        return name, ext
    else:
        raise ValueError("Wrong filename: %s" % filename) # pragma: nocover


def raw_listing(directory):
    for filename in listdir(directory):
        if not filename.startswith("."):
            full_filename = join(directory, filename)
            name, extension = split(full_filename)
            yield ItemInfo(full_filename, name, extension)


def listing(directory, extension_priority=()):
    seen = set()
    def key(item_info):
        if isdir(item_info.filename):
            return -maxint
        if item_info.extension in extension_priority:
            return extension_priority.index(item_info.extension)
        return maxint
    for item_info in sorted(raw_listing(directory), key=key):
        if not item_info.name in seen:
            seen.add(item_info.name)
            yield item_info


def text_file(filename):
    return not "\x00" in open(filename, "r").read(1024)


class Source(object):

    def __init__(self, directory, extension_priority=(),
            directory_item_name="index", static=()):
        self.directory = directory
        self.extension_priority = extension_priority
        self.directory_item_name = directory_item_name
        self.static = static

    def _build_directory(self, item_info):
        files = OrderedDict((x.name, x) for x
            in listing(item_info.filename,
                extension_priority=self.extension_priority))

        if self.directory_item_name in files \
          and text_file(files[self.directory_item_name].filename):
            info = files.pop(self.directory_item_name)
            factory = query_item_factory(info.extension, default=ContentItem)
            item = lambda children: factory(
                item_info.name, info.filename, children)
        else:
            item = lambda children: Item(item_info.name, children)
        children = [self._build(x) for x in files.values()]
        return item(children)

    def _build_file(self, item_info):
        factory = query_item_factory(item_info.extension)
        if factory is None:
            if text_file(item_info.filename):
                factory = ContentItem
            else:
                factory = BinaryItem
        return factory(item_info.name, item_info.filename)

    def _build(self, item_info):
        if self._belongs_to_static(item_info):
            return BinaryItem(item_info.name, filename=item_info.filename)
        if isdir(item_info.filename):
            return self._build_directory(item_info)
        elif isfile(item_info.filename):
            return self._build_file(item_info)

    def _belongs_to_static(self, item_info):
        return any(samefile(x, item_info.filename) for x in self.static)

    def root(self):
        item_info = ItemInfo(self.directory, "", "")
        return self._build(item_info)


def get_root(directory, extension_priority=None, directory_item_name=None,
             static=None): # pragma: nocover
    """ Return root for site."""
    if extension_priority is None:
        extension_priority = ("html", "txt", "rst", "md", "textile")
    if directory_item_name is None:
        directory_item_name = "index"
    if static is None:
        static = []
    source = Source(directory,
        extension_priority=extension_priority,
        directory_item_name=directory_item_name,
        static=static)
    return source.root()
