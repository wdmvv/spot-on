import logging
import sys

'''
Logger object
Currently exits if error is fatal
'''

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.logger = None
        self.create_logger()
    
    def create_logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        form = logging.Formatter('%(levelname)s - %(message)s')
        ch.setFormatter(form)
        logger.addHandler(ch)

        def error_handler(record):
            if record.levelno == logging.FATAL:
                print('Fatal error: ' + record.msg)
                sys.exit(1)
            return True # :^)
        
        logger.addFilter(error_handler)        

        self.logger = logger

