import logging

class Message():
  """
  Message class offers static methods to help with reading and writings messages
  between clients and servers.
  """

  @classmethod
  def recieve_message(cls, conn) -> str:
    """
    Recives a message from the server
    """
    return conn.recv(1024).decode('utf-8')

  @classmethod
  def send_message(cls, conn, msg) -> None:
    """
    Sends a message to the server
    """
    message = msg.encode('utf-8')
    conn.send(message)

  @classmethod
  def parse_msg_arg(cls, msg, search_arg) -> str:
    """
    Parses a message for its arg value

    Ex ('vlc action=load client=all', 'client=') returns 'all'
    """
    args = msg.split(" ")
    arg_val = ""
    for arg in args:
      if search_arg in arg:
        arg_val = arg.split(search_arg)[1]
    return arg_val

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
    