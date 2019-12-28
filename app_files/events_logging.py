"""
A module with a class that allows to set event logging parameters
Author: Tomasz Piętka (tomaszpwlkp@o2.pl)
"""

__version__ = '2.0.0'

import logging
import os
from datetime import datetime
from files_organization import FilesOrganization


# DEFINED CLASSES

class Logger(object):
    """Setting desired logging parameters."""

    def __init__(self):
        """Class constructor."""
        self.logging_format = '%(asctime)s - %(levelname)s - %(message)s'
        self.logfile_mode = 'a'

    def set_logging_params(self, logfilename, logging_level):
        """Sets parameters of logging events."""
        if logging_level == 'CRITICAL':
            logging.basicConfig(filename=logfilename, filemode=self.logfile_mode, level=logging.CRITICAL,
                                format=self.logging_format)
        elif logging_level == 'ERROR':
            logging.basicConfig(filename=logfilename, filemode=self.logfile_mode, level=logging.ERROR,
                                format=self.logging_format)
        elif logging_level == 'WARNING':
            logging.basicConfig(filename=logfilename, filemode=self.logfile_mode, level=logging.WARNING,
                                format=self.logging_format)
        elif logging_level == 'INFO':
            logging.basicConfig(filename=logfilename, filemode=self.logfile_mode, level=logging.INFO,
                                format=self.logging_format)
        else:
            logging.basicConfig(filename=logfilename, filemode=self.logfile_mode, level=logging.DEBUG,
                                format=self.logging_format)
        return 0

    def archive_logfile(self, logfilename, logfile_maxsize):
        """Method changes the name of the current logfile by adding a suffix
        and starts a new one with the name of the previous one. If the logfile
        doesn't exist it creates one with the given name.
        """
        if os.path.exists(logfilename) and (os.path.getsize(logfilename) >= int(logfile_maxsize)):
            log_organizer = FilesOrganization()
            return log_organizer.add_suffix_to_filename('.', logfilename, self.get_current_date())
        else:
            return 0

    def get_current_date(self):
        """Gets current date and formats it to create a suffix for file."""
        current_date = datetime.now()
        return datetime.strftime(current_date, '%Y%m%d%H%M')