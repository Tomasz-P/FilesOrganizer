"""
A module with a class that allows creating a python command line interface for scripts.
Author: Tomasz Piętka (tomaszpwlkp@o2.pl)
"""

__version__ = '2.0.0'

import argparse

# DEFINED CLASSES

class Cli(object):
    """Enable the usage of cli with python scripts."""

    def __init__(self, app_version):
        """Class constructor."""
        self.__APP_VERSION = app_version

    def get_args_from_cli(self):
        """Creates command line interface for starting the script and gets arguments from cli.
        Returns a tuple.
        """
        cli_parser = argparse.ArgumentParser(prog=__file__,
                                             usage='%(prog)s [options] path',
                                             description='Organization of files with configuration data',
                                             add_help=True,
                                             epilog='End of help')
        cli_parser.version = self.__APP_VERSION
        cli_parser.add_argument('-v', '--version', action='version', help='show program version')
        cli_parser.add_argument('-cfg', '--config', type=str, action='store', required=True, help='configuration file')
        args = cli_parser.parse_args()
        return args.config