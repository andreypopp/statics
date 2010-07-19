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

from generic.multidispatch import multifunction
from generic.multidispatch import multimethod
from generic.multidispatch import has_multimethods

from statics.item import Item
from statics.item import BinaryItem
from statics.item import ContentItem
from statics.configuration import query_item_factory

__all__ = ["get_root"]


class NodeInfo(namedtuple("NodeInfo", ["filename", "name", "extension"])):

    @property
    def basename(self):
        if self.extension:
            return "%s.%s" % (self.name, self.extension)
        return self.name


class FileInfo(NodeInfo):
    """ Named tuple for storing information about file."""


class DirectoryInfo(NodeInfo):
    """ Named tuple for storing information about directory."""


def fileinfo(filename, name=None):
    """ Construct :class:`FileInfo` object from filename, posible overriding
    name by ``name`` argument."""
    if isdir(filename):
        if name is None:
            name = basename(filename)
        return DirectoryInfo(filename=filename, name=name, extension=None)
    elif isfile(filename):
        name_, extension = splitext(filename)
        if name is None:
            name = basename(name_)
        if extension:
            extension = extension[1:]
        return FileInfo(filename=filename, name=name, extension=extension)
    else:
        raise ValueError("Wrong filename: %s" % filename) # pragma: nocover


def listing(directory):
    """ Generate :class:`ItemInfo` objects from all non-hidden files and
    directories inside ``directory``.
    """
    for filename in listdir(directory):
        if not filename.startswith("."):
            yield fileinfo(join(directory, filename))


def unique_sorted_listing(directory, extension_priority=()):
    """ Generates :class:`ItemInfo` objects that are unique (by name) and
    sorted with respect to ``extension_priority``."""
    seen = set()
    @multifunction(DirectoryInfo)
    def key(dirnfo):
        return -maxint
    @key.when(FileInfo)
    def key(fileinfo):
        if fileinfo.extension in extension_priority:
            return extension_priority.index(fileinfo.extension)
        return maxint
    for fileinfo in sorted(listing(directory), key=key):
        if not fileinfo.name in seen:
            seen.add(fileinfo.name)
            yield fileinfo


def text_file(filename):
    """ Returns true if given ``filename`` points to text file."""
    return not "\x00" in open(filename, "r").read(1024)


@has_multimethods
class Source(object):

    def __init__(self, directory, extension_priority=(),
            directory_item_name="index", exclude=()):
        self.directory = directory
        self.extension_priority = extension_priority
        self.directory_item_name = directory_item_name
        self.exclude = exclude

    @multimethod(DirectoryInfo)
    def _build(self, dirinfo):
        if self._belongs_to_exclude(dirinfo):
            return BinaryItem(dirinfo.name, filename=dirinfo.filename)
        files = OrderedDict((x.name, x) for x
            in unique_sorted_listing(dirinfo.filename,
                extension_priority=self.extension_priority))

        if self.directory_item_name in files \
          and text_file(files[self.directory_item_name].filename):
            info = files.pop(self.directory_item_name)
            factory = query_item_factory(info.extension, default=ContentItem)
            item = lambda children: factory(
                dirinfo.name, info.filename, info.extension, children=children)
        else:
            item = lambda children: Item(dirinfo.name, children=children)
        children = [self._build(x) for x in files.values()]
        return item(children)

    @_build.when(FileInfo)
    def _build(self, fileinfo):
        if self._belongs_to_exclude(fileinfo):
            return BinaryItem(fileinfo.name, filename=fileinfo.filename)
        factory = query_item_factory(fileinfo.extension)
        if factory is None:
            if text_file(fileinfo.filename):
                return ContentItem(fileinfo.name, fileinfo.filename)
            else:
                return BinaryItem(fileinfo.basename, fileinfo.filename)
        else:
            return factory(fileinfo.name, fileinfo.filename)

    def _belongs_to_exclude(self, fileinfo):
        return any(samefile(x, fileinfo.filename) for x in self.exclude)

    def root(self):
        return self._build(fileinfo(self.directory, name=""))


def get_root(directory, extension_priority=None, directory_item_name=None,
             exclude=None): # pragma: nocover
    """ Return root for site."""
    if extension_priority is None:
        extension_priority = ("html", "txt", "rst", "md", "textile")
    if directory_item_name is None:
        directory_item_name = "index"
    if exclude is None:
        exclude = []
    source = Source(directory,
        extension_priority=extension_priority,
        directory_item_name=directory_item_name,
        exclude=exclude)
    return source.root()
