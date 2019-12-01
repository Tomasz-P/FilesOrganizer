'''
A script enabling files organization in various indicated directories.
Version: 1.0
Author: Tomasz Piętka (tomaszpwlkp@o2.pl)
'''

import configparser


# DEFINED FUNCTIONS
def main():
    '''Main function of the script.'''
    settings = load_settings('FilesOrganizer_cfg.ini')
    print(settings)


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


# MAIN PROGRAM

if __name__ == "__main__":
    main()
