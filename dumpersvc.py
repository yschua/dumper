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

        #f = open('test.dat', 'w+')
        #rc = None
        
        #while rc != win32event.WAIT_OBJECT_0:
        #    f.write('TEST DATA\n')
        #    f.flush()
        #    rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
            
        #f.write('SHUTTING DOWN\n')
        #f.close()

if __name__ == '__main__':
    #path = os.path.dirname(os.path.abspath(__file__))
    #sys.path.append(path)
    #with open('path.txt', 'w') as f:
    #    f.write(path)

    win32serviceutil.HandleCommandLine(DumperSvc)
