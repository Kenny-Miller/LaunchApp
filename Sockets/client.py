import socket, sys
from message import Message


# Determine which mode to run in
# User mode is a one-way connection that allows you to send commands to the server
# Auto mode is a two-way connection that waits for messages from server
def get_mode():
  mode = 'auto'
  if len(sys.argv) > 1 and sys.argv[1].lower() in ['user','u']:
    mode = 'user'
  return mode  

class Client():

  def __init__(self, server='127.0.0.1', port='5050', mode='auto') -> None:
    self.server = server
    self.port = port
    self.running = False
    self.conn = None
    self.mode = mode

  def start_client(self) -> None:
    print('[STARTUP] starting client')
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.conn.connect((self.server, self.port))

    print(f'[Connection] client connected to {self.server}:{self.port}')
    try:
      while self.running:
        if self.mode == 'user':
          msg = input("[USER] Enter command: ")
          if msg.lower() in ['quit', 'q', 'exit']:
            self.running = False
          elif msg.lower() == 'shutdown':
            self.running = False
            Message.send_message(self.conn,'shutdown')
        else:
          msg = Message.recieve_message()
    except KeyboardInterrupt:
      pass
    print('[CONNECTION] Terminating connection bewteen client and server')
    self.conn.close()

client = Client(mode=get_mode())
client.start_client()
