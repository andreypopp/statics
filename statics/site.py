""" Site."""

from jinja2 import Environment
from jinja2 import FileSystemLoader
from configobj import ConfigObj

from statics.util import cached_generator_property
from statics.util import cached_property
from statics.source import get_root

__all__ = ["BaseSite", "Site"]


class BaseSite(ConfigObj):
    """ Rich wrapper around :class:`configobj.ConfigObj`."""

    @cached_generator_property
    def locations(self):
        """ Locations' specifications."""
        for section in self.keys():
            if section.startswith("location:"):
                script_config = self[section]
                script_name = script_config.pop("name")
                location = section[9:]
                yield location, script_config, script_name

    @cached_property
    def templates(self):
        """ Configured Jinja2 template environment."""
        templates = self["templates"]["directory"]
        return Environment(loader=FileSystemLoader(templates))


class Site(BaseSite):

    @property
    def build_directory(self):
        return self["build"]["directory"]

    @cached_property
    def root(self):
        directory = self["source"]["directory"]
        extension_priority = self["source"].get("extension_priority")
        directory_item_name = self["source"].get("directory_item_name")
        if "exclude" in self["source"]:
            exclude = self["source"].as_list("exclude")
        else:
            exclude = None
        return get_root(
            directory, extension_priority=extension_priority,
            directory_item_name=directory_item_name,
            exclude=exclude)
