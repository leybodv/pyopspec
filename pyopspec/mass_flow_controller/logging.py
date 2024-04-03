"""
Module for instantiating and configuring logger
"""

import logging
from pathlib import Path

logging_levels = {
                    'BronkhorstMassFlowController':logging.INFO,
                 }

def get_logger(name:str, logfilename:str) -> logging.Logger:
    """
    Get logger with corresponding name configured to log to stdout.

    parameters
    ----------
    name:str
        name of returned logger

    returns
    -------
    logger:logging.Logger
        configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging_levels[name])
    logger.propagate = False

    logfile = Path(logfilename).absolute()
    logfile.parent.mkdir(parents=True, exist_ok=True)
    if not logger.handlers: # create handlers if there are no handlers with this logger already (see https://stackoverflow.com/a/6729713/5267276)
        ch = logging.FileHandler(filename=logfile)
        ch.setLevel(logging_levels[name])
        formatter = logging.Formatter(fmt='[%(asctime)s] %(name)s.%(funcName)s: %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
