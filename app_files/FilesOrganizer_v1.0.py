'''
A script enabling files organization in various indicated directories.
Version: 1.0
Author: Tomasz Piętka (tomaszpwlkp@o2.pl)
'''

import configparser
from files_organization import FilesOrganization


# DEFINED FUNCTIONS

def load_settings(filename):
    '''Load settings from configuration file.'''
    settings = {}
    config = configparser.ConfigParser()
    config.read(filename)
    for section in config.sections():
        options_dictionary = {}
        for option in config.options(section):
            options_dictionary[option] = config[section][option]
        settings[section] = options_dictionary
    return settings

def rename_files_and_move(object, files_list, source_path, destination_path):
    '''Check files if they are not empty, renames them and move from a source
    path to a destination path.'''
    for full_filename in files_list:
        new_full_filename = object.add_suffix_to_filename(source_path, full_filename,
                                                          object.get_file_ctime(source_path, full_filename))
        if object.label_empty_file(source_path, new_full_filename) == 0:
            object.move_file(new_full_filename, source_path, destination_path)
    return 0

def main():
    '''Main function of the script.'''
    try:
        SETTINGS = load_settings('FilesOrganizer_cfg.ini')
        #print(SETTINGS)
        source_folder = SETTINGS['general_settings']['source_folder']
        file_prefixes = SETTINGS['filenames_startswith']
        organizer = FilesOrganization()
        for file_prefix in file_prefixes.keys():
            files_list = organizer.get_files_with_prefix(source_folder, file_prefix)
            destination_folder = file_prefixes[file_prefix]
            rename_files_and_move(organizer, files_list, source_folder, destination_folder)
    except configparser.Error:
        print('\nAn exception associated with the configuration file has occurred.\nCheck the file.')


# MAIN PROGRAM

if __name__ == "__main__":
    main()