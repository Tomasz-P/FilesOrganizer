"""
A module with classes for mail notifications
Author: Tomasz Piętka (tomaszpwlkp@o2.pl)
"""

__version__ = '2.0.0'

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from socket import gethostname, gethostbyname
from datetime import datetime

# DEFINED CLASSES

class EmailNotifications(object):
    """A class containing methods for email notifications management."""

    def __init__(self):
        """EmailNotifications class constructor."""
        self.hostname = gethostname()
        self.host_ipaddr = gethostbyname(self.hostname)

    def send_notification(self, smtp_svr, smtp_svr_port, mail_sender,
                          mail_receivers, subject_endpart, mail_body):
        """Sends event notifications to receivers by email."""
        full_subject = self.hostname + ' - IP: ' + self.host_ipaddr + ' - ' + subject_endpart
        message = MIMEMultipart()
        message['From'] = mail_sender
        message['To'] = mail_receivers
        message['Subject'] = full_subject
        message.attach(MIMEText(mail_body, 'plain'))
        text = message.as_string()
        email = smtplib.SMTP(smtp_svr, smtp_svr_port)
        email.sendmail(mail_sender, mail_receivers, text)
        email.quit()


class MailBodies(object):
    """A class containing methods for creating mails' bodies"""

    def __init__(self):
        """MailBodies class constructor."""
        self.formatted_current_date_time = datetime.now().strftime('%B %d, %Y at %H:%M')

    def list_entries_to_rowset(self, list_entries):
        """Convert a list of entries into a rowset."""
        rowset = ''
        for entry in list_entries:
            rowset += '\n' + entry
        return rowset

    def devs_without_files_empty_files_text(self, devs_without_files, empty_files):
        """Creates an email body for existing devices with no backup files and empty files."""
        text = f'\nOn {self.formatted_current_date_time} while organizing files with' \
                     f' configuration backups of SAN Storage devices\n\n' \
                     f'1) NO VALID FILES were found for the following devices:\n ' \
                     f'{self.list_entries_to_rowset(devs_without_files)}\n\n' \
                     f'2) the following EMPTY FILES were found:\n ' \
                     f'{self.list_entries_to_rowset(empty_files)}'
        return text

    def devs_without_files_text(self, devs_without_files):
        """Creates an email body for existing devices with no backup files."""
        text = f'\nOn {self.formatted_current_date_time} while organizing files with' \
                     f' configuration backups of SAN Storage devices\n\n' \
                     f'NO VALID FILES were found for the following devices:\n ' \
                     f'{self.list_entries_to_rowset(devs_without_files)}'
        return text

    def empty_files_text(self, empty_files):
        """Creates an email body for existing devices with no backup files and empty files."""
        text = f'\nOn {self.formatted_current_date_time} while organizing files with' \
                     f' configuration backups of SAN Storage devices\n\n' \
                     f'the following EMPTY FILES were found:\n ' \
                     f'{self.list_entries_to_rowset(empty_files)}'
        return text

    def files_organizing_success_text(self, valid_files):
        """Creates an email body for all valid files."""
        text = f'\nOn {self.formatted_current_date_time} files organizing was' \
                     f' SUCCESSFUL.\n\nThe following files were organized:\n' \
                     f'{self.list_entries_to_rowset(valid_files)}'
        return text

    def create_files_organizing_email_body(self, valid_files, empty_files, devs_without_files):
        """Creates a mail body for organizing files."""
        if not devs_without_files == [] and not empty_files == []:
            return self.devs_without_files_empty_files_text(devs_without_files, empty_files)
        elif not devs_without_files == [] and empty_files == []:
            return self.devs_without_files_text(devs_without_files)
        elif devs_without_files ==[] and not empty_files == []:
            return self.empty_files_text(empty_files)
        else:
            return self.files_organizing_success_text(valid_files)