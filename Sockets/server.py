import socket, threading
from message import Message

class Server():
  def __init__(self, host='127.0.0.1', port='5050') -> None:
      self.host = host 
      self.port = int(port)
      self.running = False
      self.listener = None
      self.connections = []

  # Setsup server listener to accept new connections and begin listening for sockets
  def start_server(self) -> None:
    print('[STARTUP] starting server')
    self.running = True
    self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.listener.bind((self.host, self.port))
    self.listener.listen()

    # Loop until we want to stop server
    print(f'[STARTUP] server is now listening on: {self.host}:{self.port}')
    try:
      while self.running:
        # Accept connection and handle on seperate thread
        (conn, addr) = self.listener.accept()
        self.connections.append((conn,addr))
        thread = threading.Thread(target=self.handle_connection, args=(conn, addr))
        thread.start()
    # Shutting down listener socket seems to throw an error. This is a workaround
    except Exception as e:
      print('[SHUTDOWN] shutdown was called or errored occured in server listener')
    
  # Handles a connection between client and server.
  def handle_connection(self, conn, addr) -> None:
    print(f'[CONNECTION] server established a connection with {addr}')
    connected = True
  
    # Loop until connection is broken
    while connected:
      msg = Message.recieve_message(conn)
      print(f'[MESSAGE] recieve message "{msg}" from {addr}')

      # Socket has been closed
      if not msg:
        print(f'[CLOSE] closing connection to {addr}')
        self.connections.remove((conn,addr))
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        connected = False
      # Shutdown message has been recieved
      elif msg == 'shutdown':
        self.shutdown_sever()
        connected = False
      # Normal message has been recieved
      else:
        pass
     
  # Closes all connections and stops listening for new connections
  def shutdown_sever(self) -> None:
    print(f'[SHUTDOWN] shutting down server')
    for (conn, addr) in self.connections:
      conn.shutdown(socket.SHUT_RDWR)
      conn.close()
      self.running = False
    self.listener.close()

  # Sends a message to all clients. ignr is a list of (conn,addr) you don't want to send to
  def broadcast_message(msg, ignr=None) -> None:
    pass

server = Server()
server.start_server()
  