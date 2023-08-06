import logging


def add_log_handler(logger: logging.Logger, hndlr: logging.StreamHandler):
    """Add log handler to the passed logger

    Parameters
    ----------
    logger : logging.Logger
        the logger to which handler (<hndlr>) is to be added
    hndlr : logging.StreamHandler
        handler which is to be added to logger
    """
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    hndlr.setFormatter(formatter)
    logger.addHandler(hndlr)


def set_log_level(logger: logging.Logger, level_str: str):
    """Set logging level for a logger

    Parameters
    ----------
    logger : logging.Logger
        the logger whose level is to be set
    level_str : str
        the log level, can be critical, error, warn,
        warning, info, or debug.

    Raises
    ------
    ValueError
        if level_str is not in (critical, error, warn,
        warning, info, debug)
    """
    levels = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warn": logging.WARNING,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }
    level = levels.get(level_str.lower())
    if level is None:
        logger.error("Incorrect log level passed")
        raise ValueError(
            f"log level given: {level_str}"
            f" -- must be one of: {' | '.join(levels.keys())}"
        )
    else:
        logger.setLevel(level)
