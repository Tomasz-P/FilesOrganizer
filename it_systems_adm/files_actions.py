"""
A module with a class to organize files in directories
Author: Tomasz Piętka (tomaszpwlkp@o2.pl)
"""

__version__ = '2.0.0'

import os
import shutil
import logging
from datetime import datetime

# DEFINED CLASSES

class FilesOrganization(object):
    """Organizing files stored in one main directory in various indicated directories."""

    def __init__(self, logging_status='OFF'):
        """Class constructor."""
        if logging_status == 'ON':
            logging.info(f'Logging status for methods in FilesOrganization class is "ON".')
        self.empty_file_prefix = 'EMPTY_'
        self.logging_status = logging_status

    def label_empty_file(self, path, fullfilename):
        """Labels an empty file with a prefix "self.empty_file_prefix". Method takes two arguments.
        path - a path to the directory in which the file is located,
        fullfilename - a full name of the file with an extension.
        """
        if os.path.getsize(os.path.join(path, fullfilename)) == 0:
            labelled_fullfilename = self.empty_file_prefix + fullfilename
            os.rename(os.path.join(path, fullfilename), os.path.join(path, labelled_fullfilename))
            if self.logging_status == 'ON':
                logging.debug(f'File {fullfilename} labelled with {self.empty_file_prefix} prefix.')
            return labelled_fullfilename
        else:
            return fullfilename

    def get_files_with_prefix(self, folder_path, prefix):
        """Returns a list of files that start with a prefix. Method takes two arguments:
        folder_path - a path to the folder in which considered files are located.
        """
        files_list = []
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.startswith(prefix):
                    files_list.append(entry.name)
                    if self.logging_status == 'ON':
                        logging.debug(f'File {entry.name} starts with prefix {prefix} and was appended to list {files_list}.')
        return files_list

    def get_files_with_suffix(self, folder_path, suffix):
        """Returns a list of files that end with a suffix. Method takes two arguments.
        folder_path - a path to the folder in which considered files are located.
        """
        files_list = []
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith(suffix):
                    files_list.append(entry.name)
                    if self.logging_status == 'ON':
                        logging.debug(f'File {entry.name} starts with suffix {suffix} and was appended to list {files_list}.')
        return files_list

    def move_files(self, files_list, source_path, destination_path):
        """Moves files from a source folder to a destination folder. If the destination
         folder doesn't exist it creates it.
         """
        for fullfilename in files_list:
            if not os.path.exists(destination_path):
                os.mkdir(destination_path)
                if self.logging_status == 'ON':
                    logging.info(f'Folder {destination_path} was created.')
            shutil.move(os.path.join(source_path, fullfilename), os.path.join(destination_path, fullfilename))
            if self.logging_status == 'ON':
                logging.info(f'File "{fullfilename}" was moved from {source_path} to {destination_path}.')
        return files_list

    def move_file(self, fullfilename, source_path, destination_path):
        """Moves a file from a source folder to a destination folder. If the destination
        folder doesn't exist it creates it.
        """
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        shutil.move(os.path.join(source_path, fullfilename), os.path.join(destination_path, fullfilename))
        if self.logging_status == 'ON':
            logging.info(f'File "{fullfilename}" was moved from {source_path} to {destination_path}.')
        return fullfilename

    def get_file_ctime(self, path, fullfilename):
        """Gets and returns a formatted creation time of a filename."""
        file_ctime = datetime.fromtimestamp(os.path.getctime(os.path.join(path, fullfilename)))
        if self.logging_status == 'ON':
            logging.debug(f'The creation time of file {fullfilename} is {file_ctime.strftime("%Y%m%d-%H%M")}.')
        return file_ctime.strftime('%Y%m%d-%H%M')

    def add_suffix_to_filename(self, path, fullfilename, suffix):
        """Adds a creation time of a file at the end of a filename."""
        filename, file_extension = os.path.splitext(fullfilename)
        new_fullfilename = filename + '_' + suffix + file_extension
        os.rename(os.path.join(path, fullfilename), os.path.join(path, new_fullfilename))
        if self.logging_status == 'ON':
            logging.debug(f'Suffix {suffix} was added to filename {fullfilename} - new filename: {new_fullfilename}.')
        return new_fullfilename