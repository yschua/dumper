import sys
import os
import logging

import win32service
import win32serviceutil
import win32event

from dumper.run import Dumper

class DumperSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "DumperSvc"
    _svc_display_name_ = "Dumper Service"
    _svc_description_ = "FTP file dumper"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    
    def SvcDoRun(self):
        self.main()
    
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        logging.info('Stopping dumper')
        
    def main(self):
        Dumper.main()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DumperSvc)
