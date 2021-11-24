import logging

class Message():
  # Handles recieving messages. Assumes two messages will be sent.
  # One message with message length and one message with message content.
  @classmethod
  def recieve_message(cls, conn) -> str:
    return conn.recv(1024).decode('utf-8')

  # Handles sending messages. Sends two messages at a time
  # One message wtih message length and one message with message content.
  @classmethod
  def send_message(cls, conn, msg) -> None:
    message = msg.encode('utf-8')
    conn.send(message)

  # Parses a message for its arg value
  # Ex ('vlc action=load client=all', 'client=') returns 'all'
  @classmethod
  def parse_msg_arg(cls, msg, search_arg) -> str:
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
    