
import logging
import os
from datetime import datetime

from typing import Union, Optional
from logging import FileHandler
from logging import StreamHandler

from rkt_lib_toolkit.tool.Tool import Tool, Singleton
from rkt_lib_toolkit.exception.LoggerException import InvalidLogLevelError, LogIsNotDirError


class Logger(metaclass=Singleton):
    """
    Custom logger lib

    """
    __slots__ = ["_me", "_tool", "_logger", "_loggers", "_log_file", "_formatter", "_levels_dict", "_Logger_formatter",
                 "_log_dir_path"
                 ]

    def __init__(self, caller_class: str, log_dir_path: str = "log") -> None:
        self._me = self.__class__.__name__
        self._tool = Tool()
        self._logger = logging.getLogger(name=self._me)
        self._loggers = {}

        self._log_dir_path = self._tool.get_dir(log_dir_path)

        if not self._log_dir_path:
            log_dir_path = f"{self._tool.formatted_from_os(self._tool.get_cwd())}{log_dir_path}"
            if not os.path.exists(log_dir_path):
                os.mkdir(log_dir_path)
            elif not os.path.isdir(log_dir_path):
                raise LogIsNotDirError(f"\"log\" isn't a directory")
            self._log_dir_path = self._tool.get_dir(log_dir_path)

        self._log_file = f'{self._log_dir_path}output_{datetime.today().date()}.log'
        self._formatter = logging.Formatter(f'%(asctime)s :: [{caller_class}] :: %(levelname)s :: %(message)s',
                                            "%d/%m/%Y %H:%M:%S")
        self._Logger_formatter = logging.Formatter(f'%(asctime)s :: [Logger] :: %(levelname)s :: %(message)s',
                                                   "%d/%m/%Y %H:%M:%S")
        self._levels_dict = {}
        self._init()

    def _init(self) -> None:
        """
        Check and correct (if necessary) mandatory folders or quit in case of inability to correct
        Set private "_levels_dict" var :
            CRITICAL 50   The whole program is going to hell.
            ERROR    40   Something went wrong.
            WARNING  30   To warn that something deserves attention: triggering a particular mode,
                          detecting a rare situation, an optional lib can be installed.
            INFO     20   To inform about the running of the program. For example: “Starting CSV parsing”
            DEBUG    10   To dump information when you are debugging. Like knowing what's in that fucking dictionary.

        REMEMBER :
            Each time you send a message, the logger (and each handler) will compare the lvl of the message with its own
            if the level of the message is lower than his, he ignores it, otherwise he writes it.
        """

        self._levels_dict = {50: "critical", 40: "error", 30: "warning", 20: "info", 10: "debug"}

        self._logger.setLevel(level=logging.DEBUG)
        self.set_logger(caller_class=self._me)

    def set_logger(self, caller_class: str, out_file: Optional[str] = "", output: str = "both",
                   level: Union[int, str] = "INFO") -> None:
        """
        Set and store new Logger

        :param out_file:
        :param str caller_class: name of class who want write log use to get Logger of it
        :param str output: output type
        :param str or int level:
        :return: None
        """
        if out_file:
            self._log_file = f'{self._log_dir_path}{out_file}_{datetime.today().date()}.log'

        handlers = []
        if caller_class != self._me:
            self.add(level="info", caller=self._me, message=f"Create logger for '{caller_class}'")

        if output in ["stream", "both"]:
            handlers.append(StreamHandler())

        if output in ["file", "both"]:
            handlers.append(FileHandler(filename=self._log_file, mode="a"))

        self._add_handlers(caller_class=caller_class, handlers=handlers, level=level)

    def _add_handlers(self, caller_class: str, handlers: list, level: str = "INFO") -> None:
        """
        Generic method to add message with a log level

        :param str caller_class: name of class who want write log use to get Logger of it
        :param str level: log level
        :param list handlers: list of handker need to be add in the logger
        :return:
        """
        log = logging.getLogger(name=caller_class)
        log.setLevel(level=getattr(logging, f'{level}'))
        self._formatter = logging.Formatter(f'%(asctime)s :: [{caller_class}] :: %(levelname)s :: %(message)s',
                                            "%d/%m/%Y %H:%M:%S")

        for handler in handlers:
            handler.setLevel(level=logging.getLevelName(level))
            handler.setFormatter(fmt=self._formatter if caller_class != "Logger" else self._Logger_formatter)
            log.addHandler(hdlr=handler)
            self._loggers[caller_class] = log
            if caller_class != self._me:
                self.add(level="info", caller=self._me,
                         message=f"add '{type(handler).__name__}' in '{caller_class}' logger")

    def add(self, caller: str, message: str, level: Union[int, str] = 20) -> None:
        """
        Generic method to add message with a log level

        :rtype: object
        :param str caller: name of class who want write log use to get Logger of it
        :param str level: log level
        :param str message: message to log
        :return:
        """
        if isinstance(level, int):
            if level not in self._levels_dict.keys():
                self.add(level=50, caller=self._me,
                         message=f"You try to add a message in the logger with non existing value of log level")
                raise InvalidLogLevelError(f"Log level {level} doesn't exist")
            level = self._levels_dict[level]
        getattr(self._loggers[caller], f'{level.lower()}')(message)

    def get_logger_file(self, logger_name: str) -> Optional[str]:
        try:
            for handler in self._loggers[logger_name].handlers:
                if isinstance(handler, FileHandler):
                    return handler.baseFilename
        except KeyError:
            return None
