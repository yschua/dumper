import os
import logging

import win32file
import win32con
import win32event
import pywintypes
import winnt

from threading import Thread
from dumper.file_uploader import FileUploader

class DirMonitor(Thread):
    
    def __init__(self, config):
        Thread.__init__(self)

        self._path = config['Settings']['dump_dir']
        self._buffer = win32file.AllocateReadBuffer(1024)
        self._overlapped = pywintypes.OVERLAPPED()
        self._overlapped.hEvent = win32event.CreateEvent(None, True, 0, None)
        self._overlapped.object = self._path
        self._stop_event = win32event.CreateEvent(None, True, 0, None)

        self._uploader = FileUploader(config)

    def __del__(self):
        self._stop()

    def stop(self):
        win32event.SetEvent(self._stop_event)

    def _async_watch(self):
        win32file.ReadDirectoryChangesW(
            self._hDir,
            self._buffer,
            False,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME,
            self._overlapped)

    def run(self):
        logging.info('Monitoring \'{}\''.format(self._path))

        self._hDir = win32file.CreateFile(
            self._path,
            winnt.FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ |
                win32con.FILE_SHARE_WRITE |
                win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS |
                win32file.FILE_FLAG_OVERLAPPED,
            None)

        self._async_watch()

        while True:
            rc = win32event.WaitForMultipleObjects(
                [self._stop_event, self._overlapped.hEvent],
                False,
                1000)
            if rc == win32event.WAIT_TIMEOUT:
                continue
            if rc == win32event.WAIT_OBJECT_0:
                break

            bytes = win32file.GetOverlappedResult(
                self._hDir, 
                self._overlapped, 
                True)

            result = win32file.FILE_NOTIFY_INFORMATION(self._buffer, bytes)

            for action, name in result:
                if action == winnt.FILE_ACTION_ADDED:
                    self._uploader.upload(os.path.join(self._path, name))
                    self._async_watch()
