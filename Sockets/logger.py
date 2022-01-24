import logging

class Logger():
  @classmethod
  def create_logger(cls, type) -> logging.Logger:
    """
    Creates a custom logger for the client/server.
    """
    logger = logging.getLogger(type)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
    