import os
import sys
import time
import configparser
import logging

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path, '..'))

from dumper.dir_monitor import DirMonitor
    
class Dumper():

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(path, '..', 'config.ini'))

        logging.basicConfig(
            filename=os.path.join(path, '..', 'dumper.log'), 
            level=logging.DEBUG,
            format='[%(asctime)s] %(message)s')

    def get_monitor(self):
        return DirMonitor(self.config)


    def run_script(self):
        logging.info('SCRIPT started')
        monitor = DirMonitor(self.config)
        monitor.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop()
            monitor.join()
            logging.info('SCRIPT stopped')
            sys.exit()

if __name__ == '__main__':
    dumper = Dumper()
    dumper.run_script()
