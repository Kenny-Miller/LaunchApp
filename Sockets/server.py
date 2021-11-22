import socket, logging, types, queue, selectors
from logging import Logger
from types import SimpleNamespace

class Server():
  def __init__(self, host='127.0.0.1', port='5050') -> None:
    self.host = host 
    self.port = int(port)
    self.selector = selectors.DefaultSelector()
    self.running = False
    self.listener = None
    self.logger = self.create_logger()
    self.connections = {}

  # Configure the logger the server uses
  def create_logger(self) -> Logger:
    logger = logging.getLogger('server')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

  # Sets up server listener to accept new connections and begin running for sockets
  def start_server(self) -> None:
    self.logger.debug('[STARTUP] starting server')
    self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.listener.bind((self.host, self.port))
    self.listener.setblocking(False)
    self.listener.listen()
    data = types.SimpleNamespace(type='listener')
    self.selector.register(self.listener, selectors.EVENT_READ, data=data)
    self.logger.debug(f'[STARTUP] server is now running on: {self.host}:{self.port}')

    self.running = True
    while self.running:
      events = self.selector.select(timeout=None)
      for key, mask in events:
        if key.data.type == 'listener':
          self.accept_connection(key.fileobj)
        else:
          self.handle_read(key.fileobj, key.data, mask)
          self.handle_write(key.fileobj, key.data, mask)
    
  def accept_connection(self,sock):
    (conn, addr) = sock.accept()
    self.logger.debug(f'[CONNECTION] server established a connection with {addr}')
    conn.setblocking(False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = SimpleNamespace(conn=conn, addr=addr, type='undefined', msg_queue=queue.Queue())
    self.selector.register(conn, events, data)
    self.connections[addr] = data

  def handle_read(self, conn, data, mask):
    if mask & selectors.EVENT_READ:
      msg = conn.recv(1024).decode('utf-8')
      self.logger.debug(f'[MESSAGE] recieve message "{msg}" from {data.addr}')
      if not msg:
        self.logger.debug(f'[CLOSE] closing connection to {data.addr}')
        del self.connections[data.addr]
        self.selector.unregister(conn)
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
      if msg == 'shutdown':
        self.shutdown_sever()       
      if msg == 'echo':
        data.msg_queue.put(msg)

  def handle_write(self, conn, data, mask):
    if mask & selectors.EVENT_WRITE:
      try:
        outbound_msg = data.msg_queue.get_nowait()
      except queue.Empty:
        pass
      else:
        self.broadcast_message(outbound_msg)
        #msg = outbound_msg.encode('utf-8')
        #conn.send(msg)

  # Closes all connections and stops running for new connections
  def shutdown_sever(self) -> None:
    self.listener.close()
    self.selector.unregister(self.listener)
    self.logger.debug(f'[SHUTDOWN] shutting down server')
    self.running = False
    
    for (key, val) in self.connections.items():
      conn = val.conn
      conn.shutdown(socket.SHUT_RDWR)
      conn.close()
      self.selector.unregister(conn)
    self.connections = {}  

  # Sends a message to all clients of specified type: msg_type.
  def broadcast_message(self, msg) -> None:
    #msg_type = msg.split("client=")[1]
    msg_type = 'all'
    for (key, val) in self.connections.items():
      conn = val.conn
      conn_type = val.type
      #if(msg_type != 'user' and conn_type == 'all'):
       # msg = msg.encode('utf-8')
      #  conn.send(msg)
      #if(msg_type == conn_type):
      outbound_msg = msg.encode('utf-8')
      conn.send(outbound_msg)


def main():
  server = Server(host='192.168.50.36')
  server.start_server()

if __name__ == "__main__":
  main()