import sys
import os
import logging
import time

import win32service
import win32serviceutil
import win32event

from dumper.run import Dumper

class DumperSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "DumperSvc"
    _svc_display_name_ = "Dumper Service"
    _svc_description_ = "FTP file dumper"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        dumper = Dumper()
        self.monitor = dumper.get_monitor()
    
    def SvcDoRun(self):
        logging.info('SERVICE started')
        self.monitor.start()
        self.monitor.join()
    
    def SvcStop(self):
        self.monitor.stop()
        logging.info('SERVICE stopped')

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DumperSvc)
