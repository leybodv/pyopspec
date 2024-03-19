"""
Module for instantiating and configuring logger
"""

import logging
from datetime import datetime

logging_levels = {
                    'WatlowFurnaceController':logging.INFO
                 }

def get_logger(name:str, logdir:str) -> logging.Logger:
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

    # ch = logging.StreamHandler()
    ch = logging.FileHandler(filename=logdir + f'/{datetime.now():%Y%m%d_%H%M%S}.log')
    ch.setLevel(logging_levels[name])

    formatter = logging.Formatter(fmt='[%(asctime)s] %(name)s.%(funcName)s: %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger
