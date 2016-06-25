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
            level=logging.INFO,
            format='[%(asctime)s] %(message)s')

    def run_service(self):
        pass

    def run_script(self):
        monitor = DirMonitor(self.config)
        monitor.start()
        logging.info('Dumper script started')

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop()
            monitor.join()
            logging.info('Dumper script stopped')
            sys.exit()

if __name__ == '__main__':
    dumper = Dumper()
    dumper.run_script()
