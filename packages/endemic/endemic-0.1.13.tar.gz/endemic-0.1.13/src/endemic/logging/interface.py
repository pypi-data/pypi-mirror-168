import logging
from abc import ABCMeta, abstractmethod


class LoggerInterface:
    MSG = 'message'
    TAG = 'tag'

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    EXCEPTION = logging.ERROR
    CRITICAL = logging.CRITICAL

    __metaclass__ = ABCMeta

    @abstractmethod
    def info(self, message, class_name: str = None, tag: str = None, variables: dict = None, method_name: str = None,
             exc_info=None):
        pass

    @abstractmethod
    def error(self, message, class_name: str = None, tag: str = None, variables: dict = None, method_name: str = None,
              exc_info=None):
        pass

    @abstractmethod
    def critical(self, message, class_name: str = None, tag: str = None, variables: dict = None,
                 method_name: str = None, exc_info=None):
        pass

    @abstractmethod
    def debug(self, message, class_name: str = None, tag: str = None, variables: dict = None, method_name: str = None,
              exc_info=None):
        pass

    @abstractmethod
    def exception(self, message, class_name: str = None, tag: str = None, variables: dict = None,
                  method_name: str = None, exc_info=None):
        pass

    @abstractmethod
    def warning(self, message, class_name: str = None, tag: str = None, variables: dict = None,
                method_name: str = None, exc_info=None):
        pass
