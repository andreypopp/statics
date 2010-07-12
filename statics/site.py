""" Site."""

from jinja2 import Environment
from jinja2 import FileSystemLoader
from configobj import ConfigObj

from statics.util import cached_generator_property
from statics.util import cached_property

__all__ = ["Site"]


class Site(ConfigObj):
    """ Rich wrapper around :class:`configobj.ConfigObj`."""

    @cached_generator_property
    def locations(self):
        """ Locations."""
        for section in self.keys():
            if section.startswith("location:"):
                script_config = self[section]
                script_name = script_config.pop("name")
                location = section[9:]
                yield location, script_config, script_name

    @cached_property
    def templates(self):
        templates = self["templates"]["directory"]
        return Environment(loader=FileSystemLoader(templates))
