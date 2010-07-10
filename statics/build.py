""" Build."""

from os import mkdir
from os.path import join
from shutil import copy

from statics.tree import TreeView
from statics.configuration import query_script
from statics.element import ContentElement
from statics.element import Element
from statics.element import BinaryElement

__all__ = ["build", "layout"]


def ordered_locations(locations):
    return sorted(locations, reverse=True)


def build(site, root_item, locations=None):
    """ Build `site`."""
    if locations is None:
        locations = site.locations
    if not "/" in [l for l, c, s in locations]:
        raise ValueError("No script found for root (/) location.")

    builded = []
    for location, script_config, script_name in ordered_locations(locations):
        view = TreeView(root_item,
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


def layout(element, directory):
    if isinstance(element, ContentElement):
        return layout_content(directory, element)
    elif isinstance(element, BinaryElement):
        return layout_binary(directory, element)
    elif isinstance(element, Element):
        return layout_container(directory, element)


def layout_container(directory, element):
    if element.name:
        new_directory = join(directory, element.name)
        mkdir(new_directory)
    else:
        new_directory = directory
    for child in element.values():
        layout(new_directory, child)
    return new_directory


def layout_content(directory, element):
    new_directory = layout_container(directory, element)
    open(join(new_directory, "index.html"), "w").write(element.render())
    return new_directory


def layout_binary(directory, element):
    copy(element.filename, directory)
    return directory
