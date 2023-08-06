from deka_plog.log_manager import LogManager, MyLogger, MyRootLogger
from typing import Union


def get_default_logger() -> Union[MyLogger, MyRootLogger]:
    log_manager = LogManager('DUBBO')
    logger = log_manager.get_builder().builder()
    return logger


class Logger:
    logger = None
