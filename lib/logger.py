from logging import handlers
import logging
from lib.path import SYSTEMPATH


class Logger(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not Logger.__instance:
            Logger.__instance = object.__new__(cls, *args)
        return Logger.__instance

    def __init__(self):

        self.formater = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s')

        self.logger = logging.getLogger('log')
        self.logger.setLevel(logging.DEBUG)

        self.filelogger = handlers.RotatingFileHandler(SYSTEMPATH,
                                                       maxBytes=5242880,
                                                       backupCount=3
                                                       )
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.DEBUG)

        self.filelogger.setFormatter(self.formater)
        self.console.setFormatter(self.formater)
        self.logger.addHandler(self.filelogger)
        self.logger.addHandler(self.console)

    def log(self):
        return self.logger


logger = Logger().log()