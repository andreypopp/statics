""" Command line utilities."""

# TODO: This is subject to refactoring.

import sys

__all__ = ["run", "command", "message", "error", "progress"]


def message(msg):
    print>>sys.stderr, msg


def error(msg, code=1):
    message("error: %s" % msg)
    sys.exit(code)


def progress(msg):
    message("progress: %s" % msg)


def run():
    """ Run statics command line interface."""
    objs = sys._getframe().f_back.f_globals
    commands = {}
    for k, v in objs.items():
        if hasattr(v, "__call__") and hasattr(v, "__command_name__"):
            commands[v.__command_name__] = v
    if len(sys.argv) < 2:
        error("Please provide command to run.")
    prog_name, command_name, args = sys.argv[0], sys.argv[1], sys.argv[2:]
    if not command_name in commands:
        error("No such command '%s'" % command_name)
    command = commands[command_name]
    progress("Running '%s' command." % command_name)
    command(args)


def command(name):
    """ Mark function as command."""
    def command_decorator(func):
        func.__command_name__ = name
        return func
    return command_decorator


def statics_init():
    """ Script for initializing statics site."""
    import shutil
    import os.path
    import optparse
    import pkg_resources
    parser = optparse.OptionParser()
    options, args = parser.parse_args()
    if not args:
        error("Please provide directory where you want to initialize statics.")
    directory = os.path.abspath(args[0])
    if os.path.exists(directory):
        error("Directory '%s' already exists." % directory)
    if not os.path.exists(os.path.dirname(directory)):
        error("Parent directory '%s' does not exists." %
              os.path.dirname(directory))
    progress("Creating statics site in '%s'" % directory)
    shutil.copytree(pkg_resources.resource_filename("statics", "skeleton"),
                    directory)
    progress("Complete.")
