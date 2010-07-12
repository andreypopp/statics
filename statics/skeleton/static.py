#! /usr/bin/env python

from os import mkdir
from os.path import join
from os.path import abspath
from os.path import dirname
from shutil import rmtree

from statics import configuration
from statics import site
from statics import source
from statics import build
from statics import cli
from statics import pages


CONFIG_FILENAME = join(dirname(abspath(__file__)), "site.conf")


class Site(site.Site):

    def __init__(self, filename):
        super(Site, self).__init__(filename)
        # Useful for specifying path, relative to site directory.
        self["DEFAULT"] = {}
        self["DEFAULT"]["HERE"] = dirname(filename)
        # Some shortcuts
        self.build_directory = self["build"]["directory"]


def get_root(site):
    directory = site["source"]["directory"]
    extension_priority = site["source"].get("extension_priority")
    directory_item_name = site["source"].get("directory_item_name")
    if "static" in site["source"]:
        static = site["source"].as_list("static")
    else:
        static = None
    return source.get_root(
        directory, extension_priority=extension_priority,
        directory_item_name=directory_item_name,
        static=static)


def configure():
    """ Make site specific configurations."""
    configuration.add_script("pages", pages.pages)


@cli.command("build")
def do_build(args):
    site = Site(CONFIG_FILENAME)
    cli.progress("Building tree of items.")
    item = get_root(site)
    cli.progress("Mapping tree of items to tree of elements with scripts.")
    element = build.build(site, item)
    cli.progress("Laying out tree of elements to filesystem.")
    build.layout(element, site.build_directory)
    cli.progress("Build complete.")


@cli.command("clean")
def do_clean(args):
    site = Site(CONFIG_FILENAME)
    cli.progress("Removing build directory.")
    rmtree(site.build_directory)
    mkdir(site.build_directory)


if __name__ == "__main__":
    configure()
    cli.run()
