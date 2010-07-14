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


def configure():
    """ Make site specific configurations."""
    configuration.add_script("pages", pages.pages)


@cli.command("build")
def do_build(args):
    site = Site(CONFIG_FILENAME)
    element = build.build(site, site.root)
    build.layout(element, site.build_directory)


@cli.command("clean")
def do_clean(args):
    site = Site(CONFIG_FILENAME)
    rmtree(site.build_directory)
    mkdir(site.build_directory)


if __name__ == "__main__":
    configure()
    cli.run()
