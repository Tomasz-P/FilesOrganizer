"""
A script enabling files organization in various indicated directories.
Version: 2.0.0
Author: Tomasz Piętka (tomaszpwlkp@o2.pl)
"""

from files_organization import FilesOrganization
from events_logging import Logger
from email_notification import EmailNotifications
from email_notification import MailBodies
import logging
import configparser
import argparse


# DEFINED FUNCTIONS

def load_settings(filename):
    """Load settings from configuration file."""
    settings = {}
    config = configparser.ConfigParser()
    config.read(filename)
    for section in config.sections():
        options_dictionary = {}
        for option in config.options(section):
            options_dictionary[option] = config[section][option]
        settings[section] = options_dictionary
    return settings

def get_args_from_cli():
    """Creates command line interface for starting the script and gets arguments from cli."""
    cli_parser = argparse.ArgumentParser(prog=__file__,
                                         usage='%(prog)s [options] path',
                                         description='Organization of files with configuration data',
                                         add_help=True,
                                         epilog='End of help')
    cli_parser.version = '2.0.0'
    cli_parser.add_argument('-v', '--version', action='version', help='show program version')
    cli_parser.add_argument('-cfg', '--config', type=str, action='store', required=True, help='configuration file')
    args = cli_parser.parse_args()
    return args.config

def rename_files_and_move(object, files_list, source_path, destination_path):
    """Check files if they are not empty, renames them and move from a source
    path to a destination path.
    """
    correct_files = []
    empty_files= []
    for full_filename in files_list:
        new_full_filename = object.add_suffix_to_filename(source_path, full_filename,
                                                          object.get_file_ctime(source_path, full_filename))
        returned_filename = object.label_empty_file(source_path, new_full_filename)
        if returned_filename == new_full_filename:
            # Executed if the file is not empty - returned unchanged 'new_full_filename'.
            correct_files.append(returned_filename)
            object.move_file(new_full_filename, source_path, destination_path)
            print(f'File {new_full_filename} moved from {source_path} to {destination_path}')
            logging.info(f'File {new_full_filename} moved from {source_path} to {destination_path}.')
        else:
            # Executed if the file is empty - returned changed 'labelled fullfilename'.
            empty_files.append(returned_filename)
            print(f'File {new_full_filename} is empty. Not moved.')
            logging.warning(f'File {new_full_filename} is empty. It was not moved.')
    return correct_files, empty_files

def main():
    """Main function of the script."""
    CONFIG_FILE = get_args_from_cli()
    try:
        # Settings used by the script code.
        SETTINGS = load_settings(CONFIG_FILE)
        source_folder = SETTINGS['general_settings']['source_folder']
        file_prefixes_to_dirs_name = SETTINGS['filenames_startswith']
        log_filename = SETTINGS['general_settings']['logfilename']
        log_level = SETTINGS['general_settings']['log_level']
        smtp_server = SETTINGS['email_notification_settings']['smtp_server']
        smtp_server_port = int(SETTINGS['email_notification_settings']['smtp_server_port'])
        email_sender = SETTINGS['email_notification_settings']['mail_sender']
        email_receivers = SETTINGS['email_notification_settings']['mail_receivers']
        email_subject = 'The results of organizing files.'

        logger = Logger()
        logger.archive_logfile(log_filename, 5242880)
        logger.set_logging_params(log_filename, log_level)
        logging.info('The program started.')
        logging.info(f'Settings loaded from file "{CONFIG_FILE}". Parameters in dictionary format: {SETTINGS}.')
        organizer = FilesOrganization(logging_status='ON')
        devs_without_files = []
        valid_files = []
        empty_files = []
        for file_prefix in file_prefixes_to_dirs_name.keys():
            files_list = organizer.get_files_with_prefix(source_folder, file_prefix)
            destination_folder = file_prefixes_to_dirs_name[file_prefix]
            if files_list == []:
                devs_without_files.append(destination_folder.split('/')[-1])
                print(f'No files wih prefix {file_prefix} found')
                logging.info(f'No files with prefix {file_prefix} found.')
            else:
                cf, ef = rename_files_and_move(organizer, files_list, source_folder, destination_folder)
                valid_files += cf
                empty_files += ef
                logging.info(f'Files with prefix "{file_prefix}" isolated: {files_list}.')
                logging.debug(f'Destination folder for prefix {file_prefix} specified as {destination_folder}.')
        body = MailBodies()
        email_body = body.create_files_organizing_email_body(valid_files, empty_files, devs_without_files)
        notify = EmailNotifications()
        notify.send_notification(smtp_server, smtp_server_port, email_sender, email_receivers, email_subject, email_body)
        logging.info(f'A notification email sent to {email_receivers}.')
        logging.info('The program finished.')
    except FileNotFoundError as fnfe:
        print('\nConfig file not found!\nDetails in logfile.', fnfe)
        logging.error('The program finished with exception: ', exc_info=True)
    except configparser.Error as cpe:
        print('\nAn exception associated with the configuration file has occurred.\n'
              'Check the configuration file. Details in logfile.', cpe)
        logging.error(f'An error with configuration file occurred:', exc_info=True)
    except:
        print('\nError occurred during program execution!.'
              '\nCheck the logfile for details.')
        logging.error(f'An error occurred during program execution: ', exc_info=True)

# MAIN PROGRAM

if __name__ == "__main__":
    main()