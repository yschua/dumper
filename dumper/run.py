import logging
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dumper.dir_monitor import DirMonitor
    
class Dumper():

    @staticmethod
    def main():
        curr_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(curr_path, '..', 'dumper.log')
        
        logging.basicConfig(
            filename=path, 
            level=logging.INFO,
            format='[%(asctime)s] %(message)s')

        logging.info('Starting dumper')

        monitor = DirMonitor()
        monitor.run()

if __name__ == '__main__':
    Dumper.main()