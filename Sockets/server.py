import socket, logging, types, queue, selectors
from logging import Logger
from types import SimpleNamespace

from message import Message

class Server():
  def __init__(self, host='127.0.0.1', port='5050') -> None:
    self.host = host 
    self.port = int(port)
    self.selector = selectors.DefaultSelector()
    self.running = False
    self.listener = None
    self.logger = Message.create_logger('server')
    self.connections = {}

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
    
  # Handles listener accepting and creating new socket connections
  def accept_connection(self,sock):
    (conn, addr) = sock.accept()
    self.logger.debug(f'[CONNECTION] server established a connection with {addr}')
    conn.setblocking(False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = SimpleNamespace(conn=conn, addr=addr, type='undefined', msg_queue=queue.Queue())
    self.selector.register(conn, events, data)
    self.connections[addr] = data

  # Handles recieving a message from a client
  def handle_read(self, conn, data, mask):
    if mask & selectors.EVENT_READ:
      msg = Message.recieve_message(conn=conn)
      self.logger.debug(f'[MESSAGE] recieve message "{msg}" from {data.addr}')
      # Socket is closed if msg is empty
      if not msg:
        self.logger.debug(f'[CLOSE] closing connection to {data.addr}')
        del self.connections[data.addr]
        self.selector.unregister(conn)
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
      else:
        cmd = msg.split(" ")[0]
        # Handle messages    
        if cmd == 'shutdown':
          self.shutdown_sever()
        elif cmd == 'type':
          data.type = Message.parse_msg_arg(msg, 'type=')
        else:
          client_type = Message.parse_msg_arg(msg, 'client=')
          if client_type == '':
            client_type = 'all'
          self.create_outbound_message(msg, client_type)
  
  # Handles sending messages to a client
  def handle_write(self, conn, data, mask):
    if mask & selectors.EVENT_WRITE:
      if not data.msg_queue.empty():
        msg = data.msg_queue.get_nowait()
        Message.send_message(conn=conn,msg=msg)

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

  # Adds message to outbound queue for all clients of specified type: msg_type.
  def create_outbound_message(self, msg, client_type) -> None:
    self.logger.debug(f'[Message] sending message "{msg}" to "{client_type}" clients')
    for (key, val) in self.connections.items():
      conn_type= val.type
      msg_queue = val.msg_queue
      if conn_type != 'user' and client_type == 'all':
        msg_queue.put(msg)
      elif conn_type == client_type:
        msg_queue.put(msg)

def main():
  server = Server(host='192.168.50.36')
  server.start_server()

if __name__ == "__main__":
  main()