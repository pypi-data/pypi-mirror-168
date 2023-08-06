# coding:utf-8
import inspect
from typing import Any, List, Tuple
from unittest.mock import DEFAULT

from loguru import logger
DEFAULT = {
    'LOG_FILE': '/tmp/cf.log',
    'LOG_ROTATION': '100 MB',
    'LOG_RETENTION': '10 days',
}

logger.add(DEFAULT['LOG_FILE'],
           rotation=DEFAULT['LOG_ROTATION'],
           retention=DEFAULT['LOG_RETENTION'],
           enqueue=True,
           colorize=True,
           backtrace=True,
           diagnose=True)

def info(msg: str, *args, **kwargs):
    """ Please use string-format to restrict unexpected behaviour. 
    """
    msg = str(msg)
    if args:
        msg += f" {args}"

    if kwargs:
        msg += f" {kwargs}"
    logger.opt(depth=1).info(msg)

trace = logger.trace
debug = logger.debug
success = logger.success
warning = logger.warning
error = logger.exception
critical = logger.critical
exception = logger.exception

log_colors_config = {
    'DEBUG': 'white',
    'INFO': 'bold_cyan',
    'WARNING': 'bold_yellow',
    'ERROR': 'bold_red',
    'CRITICAL': 'bold_red',
}


class Logger(object):
    def debug(self, *message):
        pass 
    def info(self, *message):
        pass 
    def warning(self, *message):
        pass 
    def error(self, *message):
        pass 

    def critical(self, *message):
        self.console('critical', *message)

    def __repr__(self) -> str:
        d = {'level': self._level, 'logname': self._logname}
        return str(d)


def test():
    frames = inspect.stack()
    print(frames)
    Logger().info("Line 6666")


if __name__ == "__main__":
    log = Logger()
    log.info("测试1")
    log.debug("测试2")
    log.warning("warning")
    log.error("error")
    log.critical("critical")
    test()
