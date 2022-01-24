import socket
import threading
from abc import ABCMeta, abstractmethod
from logger import Logger

class Client(metaclass=ABCMeta):

  @abstractmethod
  def __init__(self, server, port, type, data_queue) -> None:
    self.server = server
    self.port = int(port)
    self.type = type
    self.running = False
    self.conn = None
    self.data_queue = data_queue
    self.logger = Logger.create_logger(type)
    thread = threading.Thread(target=self.handle, args=())
    thread.daemon = True
    thread.start()

  def establish_connection(self) -> None:
    self.running = True
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.conn.connect((self.server, self.port))
    self.logger.info(f"[Message] Connecting to {self.server}:{self.port}")
    self.conn.send(f'type {self.type}'.encode('utf-8'))

  def close_connection(self) -> None:
    self.conn.shutdown(socket.SHUT_RDWR)
    self.conn.close()

  @abstractmethod
  def handle(self):
    raise NotImplementedError()

  
