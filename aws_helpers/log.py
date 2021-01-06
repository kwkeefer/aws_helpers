import logging


def logger_setup(name: str) -> logging.Logger:
    """ Creates a logger object with a standard format.

    Args:
        name: name of logger to use (example: __name__)

    Returns:
        logging.Logger object

    """
    logger = logging.getLogger(name)
    if len(logging.getLogger().handlers) > 0:
        # for AWS lambda environments
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)
    if not logger.handlers:
        logger.propagate = False
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%m-%d-%Y %H:%M:%S')
        console.setFormatter(formatter)
    return logger
