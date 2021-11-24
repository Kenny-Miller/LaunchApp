import socket
from abc import ABCMeta, abstractmethod
from message import Message

class Client(metaclass=ABCMeta):
  """
  Abstract class for client tcp connections

  Provides baseline implementation of functions used to establish and close a connection to a server
  as well as create a logger.
  """
  
  @abstractmethod
  def __init__(self, server, port, type) -> None:
    self.server = server
    self.port = int(port)
    self.type = type
    self.running = False
    self.conn = None
    self.logger = Message.create_logger(self.type)

  def establish_connection(self) -> None:
    """
    Tries to establish a connection between the client and server.
    
    Initializes a socket a connection and then sends a message to the server telling it what type of client it is [user|left|middle|right].
    """
    self.logger.debug('[STARTUP] starting client')
    self.running = True
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.conn.connect((self.server, self.port))
    self.logger.info(f'[Connection] client connected to {self.server}:{self.port}')
    # Tell server what type of client this is
    self.logger.info(f'[Connection] telling server client is type: {self.type}')
    Message.send_message(conn=self.conn, msg=f'type type={self.type}')

  def close_connection(self) -> None:
    """
    Tries to close the connection between the client and server.
    """
    self.logger.info('[Shutdown] shutting down client connection')
    self.conn.shutdown(socket.SHUT_RDWR)
    self.conn.close()

  @abstractmethod
  def handle(self):
    """
    Runs the main loop of the client

    Not Implemented
    """
    raise NotImplementedError()

  
