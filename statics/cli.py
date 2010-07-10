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
        if hasattr(v, "__call__") and hasattr(v, "__command__"):
            commands[k] = v
    if len(sys.argv) < 2:
        error("Please provide command to run.")
    prog_name, command_name, args = sys.argv[0], sys.argv[1], sys.argv[2:]
    if not command_name in commands:
        error("no such command '%s'" % command_name)
    command = commands[command_name]
    command(args)


def command(func):
    """ Mark function as command."""
    func.__command__ = True
    return func
