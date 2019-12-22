'''
A module with a class to organize files in directories
Version: 1.0
Author: Tomasz Piętka (tomaszpwlkp@o2.pl)
'''

import os
import shutil
from datetime import datetime

# DEFINED CLASSES

class FilesOrganization(object):
    '''Organizing files stored in one main directory in various indicated directories.'''

    def __init__(self):
        '''Class constructor.'''
        self.empty_file_prefix = 'EMPTY_'

    def label_empty_file(self, path, fullfilename):
        '''Labels an empty file with a prefix "self.empty_file_prefix". Method takes two arguments.
        path - a path to the directory in which the file is located,
        fullfilename - a full name of the file with an extension.
        '''
        if os.path.getsize(os.path.join(path, fullfilename)) == 0:
            labelled_fullfilename = self.empty_file_prefix + fullfilename
            os.rename(os.path.join(path, fullfilename), os.path.join(path, labelled_fullfilename))
            return labelled_fullfilename
        return 0

    def get_files_with_prefix(self, folder_path, prefix):
        '''Returns a list of files that start with a prefix. Method takes two arguments:
        folder_path - a path to the folder in which considered files are located.
        '''
        files_list = []
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.startswith(prefix):
                        files_list.append(entry.name)
        return files_list

    def get_files_with_suffix(self, folder_path, suffix):
        '''Returns a list of files that end with a suffix. Method takes two arguments.
        folder_path - a path to the folder in which considered files are located.
        '''
        files_list = []
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith(suffix):
                    files_list.append(entry.name)
        return files_list

    def move_files(self, files_list, source_path, destination_path):
        '''Moves files from a source folder to a destination folder. If the destination
         folder doesn't exist it creates it.
         '''
        for fullfilename in files_list:
            if not os.path.exists(destination_path):
                os.mkdir(destination_path)
            shutil.move(os.path.join(source_path, fullfilename), os.path.join(destination_path, fullfilename))
        return files_list

    def move_file(self, fullfilename, source_path, destination_path):
        '''Moves a file from a source folder to a destination folder. If the destination
        folder doesn't exist it creates it.
        '''
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        shutil.move(os.path.join(source_path, fullfilename), os.path.join(destination_path, fullfilename))
        return fullfilename

    def get_file_ctime(self, path, fullfilename):
        '''Gets and returns a formatted creation time of a filename.'''
        return datetime.fromtimestamp(os.path.getctime(os.path.join(path, fullfilename))).strftime('%Y%m%d-%H%M')

    def add_suffix_to_filename(self, path, fullfilename, suffix):
        '''Adds a creation time of a file at the end of a filename.'''
        filename, file_extension = os.path.splitext(fullfilename)
        new_fullfilename = filename + '_' + suffix + file_extension
        os.rename(os.path.join(path, fullfilename), os.path.join(path, new_fullfilename))
        return new_fullfilename