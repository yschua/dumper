import ftplib
import ntpath
import logging
import configparser
import win32clipboard
import urllib.parse

import os

class FileUploader:
    
    def __init__(self):
        config = configparser.ConfigParser()
        curr_path = os.path.dirname(os.path.abspath(__file__))
        config.read(curr_path + '\\..\\config.ini')

        self._host = config['Server']['host']
        self._user = config['Server']['user']
        self._passwd = config['Server']['password']
        self._path = config['Server']['remote_path']
        self._url = config['Server']['url']

        # test ftp login

    def upload(self, filepath):
        try:
            with ftplib.FTP(self._host, self._user, self._passwd) as ftp:
                ftp.cwd(self._path)
                name = ntpath.basename(filepath)
                logging.info('Upload \'{}\''.format(name))
                msg = ftp.storbinary('STOR ' + name, open(filepath, 'rb'))
                logging.info(msg)

            self._copy_to_clipboard(name)
        except ftplib.all_errors as e:
            logging.exception(e, exc_info=False)
    
    def _copy_to_clipboard(self, name):
        url = self._url + urllib.parse.quote(name)
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(url)
        win32clipboard.CloseClipboard()
        logging.info('Copied to clipboard \'{}\''.format(url))
