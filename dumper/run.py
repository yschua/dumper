import os
import sys
import configparser
import logging

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path, '..'))

from dumper.dir_monitor import DirMonitor
    
class Dumper():

    @staticmethod
    def main():
        config = configparser.ConfigParser()
        config.read(os.path.join(path, '..', 'config.ini'))

        logging.basicConfig(
            filename=os.path.join(path, '..', 'dumper.log'), 
            level=logging.INFO,
            format='[%(asctime)s] %(message)s')
        logging.info('Starting dumper')

        monitor = DirMonitor(config)
        monitor.start()

if __name__ == '__main__':
    Dumper.main()
