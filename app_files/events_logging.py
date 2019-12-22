'''
A module with a class that allows to set event logging parameters
Version: 1.0
Author: Tomasz Piętka (tomaszpwlkp@o2.pl)
'''

import logging
import os


# DEFINED CLASSES

class LoggingParams(object):
    '''Setting desired logging parameters.'''

    def __init__(self):
        '''Class constructor.'''
        self.logging_format = '%(asctime)s - %(levelname)s - %(message)s'
        self.logfile_mode = 'a'

    def set_logging_params(self, logfilename, logging_level, logfile_maxsize):
        '''Sets parameters of logging events.'''
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
            logging.basicConfig(filename=logfilename, filemode=self.logging_format, level=logging.INFO,
                                format=self.logging_format)
        else:
            logging.basicConfig(filename=logfilename, filemode=self.logfile_mode, level=logging.DEBUG,
                                format=self.logging_format)
        return 0

    def start_new_logfile(self, logfilename, logfile_maxsize):
        '''Method changes the name of the previous logfile by adding a suffix
        and starts a new one with the name of the previous one. If the logfile
        doesn't exists it creates one with the given name.
        '''
        if not os.path.exists(logfilename):
            pass
        if os.path.getsize(logfilename) >= int(logfile_maxsize):
            add_suffix_to_logfilename()