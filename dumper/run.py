import logging
import os

from dumper.dir_monitor import DirMonitor

class Dumper():

    @staticmethod
    def main():
        path = 'E:\\Projects\\file-dumper\\file-dumper\\dumper.log'
        
        logging.basicConfig(
            filename=path, 
            level=logging.INFO,
            format='[%(asctime)s] %(message)s')

        logging.info('Starting dumper')
        #logging.info(os.path.dirname(os.path.abspath(__file__)))

        monitor = DirMonitor()
        monitor.run()


if __name__ == '__main__':
    Dumper.main()