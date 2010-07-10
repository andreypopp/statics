""" Site."""

from os.path import abspath
from os.path import dirname

from configobj import ConfigObj

from statics.util import cached_generator_property
from statics.util import cached_property

__all__ = ["Site"]


class Site(ConfigObj):
    """ Rich wrapper arounf :class:`configobj.ConfigObj`."""

    @classmethod
    def from_file(cls, filename):
        filename = abspath(filename)
        here = dirname(filename)
        site = cls(filename)
        site["DEFAULT"] = {}
        site["DEFAULT"]["HERE"] = here
        return site

    @cached_generator_property
    def locations(self):
        for section in self.keys():
            if section.startswith("location:"):
                script_config = self[section]
                script_name = script_config.pop("name")
                location = section[9:]
                yield location, script_config, script_name
