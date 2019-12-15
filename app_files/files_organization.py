'''
A module with a class to organize files in directories
Version: 1.0
Author: Tomasz Piętka (tomaszpwlkp@o2.pl)
'''

import os
import shutil

# DEFINED CLASSES

class FilesOrganization(object):
    '''Organizing files stored in one main directory in various indicated directories.'''

    def __init__(self):
        '''Class constructor.'''
        pass

    def label_empty_file(self, path, full_filename):
        '''Labels an empty file with a prefix EMPTY_.'''
        if os.path.getsize(os.path.join(path, full_filename)) == 0:
            os.rename(os.path.join(path, full_filename), os.path.join(path, 'EMPTY_' + full_filename))
            return full_filename

    def get_files_with_prefix(self, folder_path, prefix):
        '''Returns a list of files that start with a prefix.'''
        files_list = []
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.startswith(prefix):
                    files_list.append(entry.name)
        return files_list

    def get_files_with_suffix(self, folder_path, suffix):
        '''Returns a list of files that end with a suffix.'''
        files_list = []
        with os.scandir(folder_path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith(suffix):
                    files_list.append(entry.name)
        return files_list

    def move_file(self, filename, source_path, destination_path):
        '''Moves a file from a source folder to a destination folder. If the destination
         folder doesn't exist it creates it.
         '''
        if not os.path.exists(destination_path):
            os.mkdir(destination_path)
        shutil.move(os.path.join(source_path, filename), os.path.join(destination_path, filename))
        return filename

