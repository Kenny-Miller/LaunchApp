import socket, types, queue, selectors, sys
from types import SimpleNamespace

from logger import Logger

class Server():
  def __init__(self, host='127.0.0.1', port='5050') -> None:
    self.host = host 
    self.port = int(port)
    self.logger = Logger.create_logger('server')
    self.selector = selectors.DefaultSelector()
    self.running = False
    self.listener = None
    self.connections = {}

  def start_server(self) -> None:
    data = types.SimpleNamespace(type='listener')
    self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.listener.bind((self.host, self.port))
    self.listener.setblocking(False)
    self.listener.listen()
    self.logger.info(f"[Message] Now listening on {self.host}:{self.port}")
    self.selector.register(self.listener, selectors.EVENT_READ, data=data)

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
    conn.setblocking(False)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    data = SimpleNamespace(conn=conn, addr=addr, type='undefined', msg_queue=queue.Queue())
    self.selector.register(conn, events, data)
    self.connections[addr] = data
    self.logger.info(f"[Message] Accepted connection from {addr}")

  def handle_read(self, conn, data, mask):
    if mask & selectors.EVENT_READ:
      msg = conn.recv(1024).decode('utf-8')  
      self.logger.info(f"[Message] Received msg: {msg} from {data.addr}") 
      if not msg:
        del self.connections[data.addr]
        self.selector.unregister(conn)
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
      else:
        msg_header = msg.split(" ")[0]
        match msg_header:
          case 'exit': self.shutdown_sever()
          case 'type': data.type = msg.split(" ")[1]
          case _: self.create_outbound_message(msg)
  
  def handle_write(self, conn, data, mask):
    if mask & selectors.EVENT_WRITE:
      if not data.msg_queue.empty():
        msg = data.msg_queue.get_nowait()
        conn.send(msg.encode('utf-8'))

  def shutdown_sever(self) -> None:
    self.listener.close()
    self.selector.unregister(self.listener)
    self.running = False    
    for (key, val) in self.connections.items():
      conn = val.conn
      conn.shutdown(socket.SHUT_RDWR)
      conn.close()
      self.selector.unregister(conn)
    self.connections = {}  

  def create_outbound_message(self, msg) -> None:
    for (key, val) in self.connections.items():
      conn_type= val.type
      msg_queue = val.msg_queue
      if conn_type != 'u':
        msg_queue.put(msg)

def main():
  if len(sys.argv) <= 2:
    # print("Invalid Command:")
    print("Use $ server.py <addr> port=<>")
    # exit(0)

  host =  '127.0.0.1' if len(sys.argv) <= 2 else sys.argv[1]
  port = 5050 if len(sys.argv) <= 2 else sys.argv[2]

  server = Server(host=host, port=port)
  server.start_server()

if __name__ == "__main__":
  main()