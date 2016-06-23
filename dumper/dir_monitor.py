import os
import win32file
import win32con
import winnt
import logging
import configparser
import threading

from dumper.file_uploader import FileUploader

class DirMonitor:
    
    def __init__(self):
        config = configparser.ConfigParser()
        path = os.path.dirname(os.path.abspath(__file__)) + '\\..\\config.ini'
        config.read(path)

        self._path = config['Settings']['dump_dir']

        self._uploader = FileUploader()
        
    def run(self):
        t = threading.Thread(target=self._monitor)
        t.start()
        t.join()

    def _monitor(self):
        logging.info('Monitoring \'{}\''.format(self._path))

        h_dir = win32file.CreateFile(
            self._path,
            winnt.FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ |
                win32con.FILE_SHARE_WRITE |
                win32con.FILE_SHARE_DELETE,
            None, 
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None)

        while True:
            result = win32file.ReadDirectoryChangesW(
                h_dir,
                1024,
                False,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME,
                None,
                None)

            for action, name in result:
                if action == winnt.FILE_ACTION_ADDED:
                    filepath = os.path.join(self._path, name)
                    self._uploader.upload(filepath)

