""" Site."""

from configobj import ConfigObj

from statics.util import cached_generator_property
from statics.util import cached_property

__all__ = ["Site"]


class Site(ConfigObj):
    """ Rich wrapper arounf :class:`configobj.ConfigObj`."""

    @cached_generator_property
    def locations(self):
        for section in self.keys():
            if section.startswith("location:"):
                script_config = self[section]
                script_name = script_config.pop("name")
                location = section[9:]
                yield location, script_config, script_name
