import logging
import uuid
from time import time_ns
from logging import Logger
from fluent import handler
import traceback
from ..interface import LoggerInterface

custom_format = {
    'host': '%(hostname)s',
    'type': '%(levelname)s',
    'stack_trace': '%(exc_text)s',
    'time': '%(created)s',
    'stack_info': '%(stack_info)s',
}


class LoggerFluentd(LoggerInterface):

    # threads - number of pool threads
    def __init__(
            self,
            instance: str,
            log_name: str,
            logger_tag: str = 'fluentd',
            level: str = LoggerInterface.DEBUG,
            host: str = '',
            port: int = 0
    ):

        super().__init__()
        self.__log = Logger

        self.__instance_name = instance
        self.__logging_name = log_name

        self.__min_info = []
        self.__min_warning = []

        self.__link = ''
        self.__timer = 0

        self.__host = host
        self.__port = port
        self.__level = level
        self.__logger_tag = logger_tag

        self.__setting(host, port, level, logger_tag, log_name)

    def __setting(self, host, port, level, logger_tag, log_name):
        """
        Setting logger and console output
        """
        logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(message)s',
                            datefmt='%d/%m %H:%M')

        if self.__min_info:
            for i in self.__min_info:
                logging.getLogger(i).setLevel(logging.INFO)

        if self.__min_warning:
            for i in self.__min_warning:
                logging.getLogger(i).setLevel(logging.WARNING)

        if host and port:
            print('Has external connection')
            h = handler.FluentHandler(log_name, host=host, port=port)
        else:
            h = handler.FluentHandler(log_name)

        formatter = handler.FluentRecordFormatter(custom_format)
        h.setFormatter(formatter)

        self.__log = logging.getLogger(logger_tag)
        self.__log.setLevel(level)

        if host and port:
            self.__log.addHandler(h)

    def custom_log_name(self, log_name: str):
        self.__setting(self.__host, self.__port, self.__level, self.__logger_tag, log_name)

    def debug(self, message, class_name: str = None, method_name: str = None, tag: str = None, variables: dict = None,
              exc_info=None):
        self.__log.debug({**{self.MSG: message, self.TAG: tag}, **self.custom(variables, class_name, method_name)})

    def info(self, message, class_name: str = None, method_name: str = None, tag: str = None, variables: dict = None,
             exc_info=None):
        self.__log.info({**{self.MSG: message, self.TAG: tag}, **self.custom(variables, class_name, method_name)})

    def warning(self, message, class_name: str = None, method_name: str = None, tag: str = None, variables: dict = None,
                exc_info=None):
        self.__log.warning(
            {**{self.MSG: message, self.TAG: tag}, **self.custom(variables, class_name, method_name)})

    def error(self, message, class_name: str = None, method_name: str = None, tag: str = None, variables: dict = None,
              exc_info=None):
        self.__log.error({**{self.MSG: message, self.TAG: tag}, **self.custom(variables, class_name, method_name)})

    def critical(self, message, class_name: str = None, tag: str = None, variables: dict = None,
                 method_name: str = None,
                 exc_info=None):
        self.__log.critical(
            {**{self.MSG: message, self.TAG: tag}, **self.custom(variables, class_name, method_name)})

    def exception(self, message=None, tag: str = None, variables: dict = None, class_name: str = None,
                  method_name: str = None, exc_info=None):
        self.__log.exception(
            {**{self.MSG: 'Exception: {}'.format(message), self.TAG: tag},
             **self.custom(variables, class_name, method_name)})

    @property
    def func(self):
        return traceback.extract_stack(None, 2)[0][2]

    def custom(self, variables, class_name, method_name) -> dict:
        """
        Additional custom fields to exist custom format
        """
        append = variables if variables else {}
        duration = {'duration': self.timer} if self.__timer else {}

        return {
            **append,
            **duration,
            **{
                'class': class_name,
                'method': method_name,
                'link': self.link,
                'instance': self.__instance_name
            }
        }

    #
    #   Setters/getters ----------------------------------------------------------------------------
    #

    @property
    def link(self) -> str:
        if not self.__link:
            self.__link = str(uuid.uuid4())
        return self.__link

    @link.setter
    def link(self, value: str):
        self.__timer = time_ns()
        self.__link = value

    @property
    def name(self) -> str:
        return self.__logging_name

    @property
    def timer(self) -> float:
        return (time_ns() - self.__timer) * 1.0e-9

    @property
    def min_level_info(self) -> list:
        return self.__min_info

    @min_level_info.setter
    def min_level_info(self, value: str):
        self.__min_info.append(value)

    @property
    def min_level_warning(self) -> list:
        return self.__min_warning

    @min_level_warning.setter
    def min_level_warning(self, value: str):
        self.__min_warning.append(value)
