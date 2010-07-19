""" Build."""

from os import mkdir
from os.path import join
from os.path import isdir
from os.path import isfile
from os.path import exists
from shutil import copy
from shutil import copytree

from generic.multidispatch import multifunction

from statics.tree import TreeView
from statics.configuration import query_script
from statics.element import ContentElement
from statics.element import Element
from statics.element import BinaryElement

__all__ = ["build", "layout"]


def ordered_locations(locations):
    return sorted(locations, reverse=True)


def build(site, root, locations=None):
    """ Build `site`."""
    if locations is None:
        locations = site.locations # pragma: nocover
    if not "/" in [l for l, c, s in locations]:
        raise ValueError("No script found for root (/) location.")

    builded = []
    for location, script_config, script_name in ordered_locations(locations):
        view = TreeView(root,
            exclude=[l for l, n, c in locations if not l == location])
        item = view.locate(location)
        script = query_script(script_name)
        if script is None:
            raise ValueError("No script registered for name '%s'" % script_name)
        builded.append((location, script(site, script_config, item)))

    root_element = builded.pop()[1]
    for location, element in reversed(builded):
        root_element.setlocation(location, element)

    return root_element


@multifunction(BinaryElement)
def layout(element, directory):
    if isdir(element.filename):
        copytree(element.filename, join(directory, element.name))
    elif isfile(element.filename):
        copy(element.filename, directory)
    return directory


@layout.when(ContentElement)
def layout(element, directory):
    if element.is_leaf:
        filename = join(directory, "%s.%s" % (element.name, element.extension))
        open(filename, "w").write(element.render().encode("utf-8"))
        return directory
    else:
        directory = join(directory, element.name)
        if not exists(directory):
            mkdir(directory)
        filename = join(directory, "index.%s" % element.extension)
        open(filename, "w").write(element.render().encode("utf-8"))
        for child in element.values():
            layout(child, directory)
        return directory


@layout.when(Element)
def layout(element, directory):
    directory = join(directory, element.name)
    if not exists(directory):
        mkdir(directory)
    for child in element.values():
        layout(child, directory)
    return directory
