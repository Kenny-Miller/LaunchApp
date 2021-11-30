import socket, types, queue, selectors, sys
from types import SimpleNamespace

from message import Message

class Server():
  """
  Class for server tcp implementation

  Creates a server that is able to handle connections from multiple clients. Server is 'dumb' and
  only recieves a message and then sends it to the correct client from them to handle.
  """

  def __init__(self, host='127.0.0.1', port='5050') -> None:
    """
    Constructor for the Server

    host: what address server is running on
    port: what port server is running on
    """
    self.host = host 
    self.port = int(port)
    self.selector = selectors.DefaultSelector()
    self.running = False
    self.listener = None
    self.logger = Message.create_logger('server')
    self.connections = {}

  # Sets up server listener to accept new connections and begin running for sockets
  def start_server(self) -> None:
    """
    Sets up the server listener to accept new connections and handles messages to and from sockets
    """
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
    """
    Handles listener accepting and creating new socket connections
    """
    (conn, addr) = sock.accept()
    self.logger.debug(f'[CONNECTION] server established a connection with {addr}')
    conn.setblocking(False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = SimpleNamespace(conn=conn, addr=addr, type='undefined', msg_queue=queue.Queue())
    self.selector.register(conn, events, data)
    self.connections[addr] = data

  def handle_read(self, conn, data, mask):
    """
    Recieves a message from a client and handles it
    """
    if mask & selectors.EVENT_READ:
      msg = Message.recieve_message(conn=conn)
      self.logger.debug(f'[MESSAGE] recieve message "{msg}" from {data.addr}')      
      if not msg:
        # Socket is closed if msg is empty
        self.logger.debug(f'[CLOSE] closing connection to {data.addr}')
        del self.connections[data.addr]
        self.selector.unregister(conn)
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
      else:
        cmd = msg.split(" ")[0]
        if cmd == 'shutdown':
          self.shutdown_sever()
        elif cmd == 'type':
          # Sets the each client connetion's type
          data.type = Message.parse_msg_arg(msg, 'type=')
        else:
          # Determine which clients to broadcast message to
          client_type = Message.parse_msg_arg(msg, 'client=')
          if client_type == '':
            client_type = 'all'
          self.create_outbound_message(msg, client_type)
  
  def handle_write(self, conn, data, mask):
    """
    Handles sending messages to a client
    """
    if mask & selectors.EVENT_WRITE:
      if not data.msg_queue.empty():
        msg = data.msg_queue.get_nowait()
        Message.send_message(conn=conn,msg=msg)

  def shutdown_sever(self) -> None:
    """
    Closes all connections and stops running for new connections
    """
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

  def create_outbound_message(self, msg, client_type) -> None:
    """
    Adds message to outbound queue for all clients of specified type: msg_type.
    """
    self.logger.debug(f'[Message] sending message "{msg}" to "{client_type}" clients')
    for (key, val) in self.connections.items():
      conn_type= val.type
      msg_queue = val.msg_queue
      if conn_type != 'user' and client_type == 'all':
        msg_queue.put(msg)
      elif conn_type == client_type:
        msg_queue.put(msg)

def main():
  if len(sys.argv) <= 2:
    print("Invalid Command:")
    print("Use $ server.py <addr> port=<>")
    exit(0)

  server = Server(host=sys.argv[1], port=sys.argv[2])
  server.start_server()

if __name__ == "__main__":
  main()