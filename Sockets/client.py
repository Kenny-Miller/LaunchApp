import socket, sys, re
from message import Message


# Determine which mode to run in
# User mode is a one-way connection that allows you to send commands to the server
# Auto mode is a two-way connection that waits for messages from server
def get_mode():
  mode = 'user'
  if len(sys.argv) > 1:
    if sys.argv[1].lower() in ['left','l']:
      mode = 'left'
    elif sys.argv[1].lower() in ['middle','m']:
      mode = 'middle'
    elif sys.argv[1].lower() in ['right','r']:
      mode = 'right'
  return mode  

class Client():
  def __init__(self, server='127.0.0.1', port='5050', mode='user') -> None:
    self.server = server
    self.port = int(port)
    self.running = False
    self.conn = None
    self.mode = mode

  def start_client(self) -> None:
    print('[STARTUP] starting client')
    self.running = True
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.conn.connect((self.server, self.port))
    print(f'[Connection] client connected to {self.server}:{self.port}')

    # Tell server what type of client this is
    Message.send_message(self.conn,self.mode)

    try:
      while self.running:
        # User mode will only be able to launch commands
        if self.mode == 'user':
          cmd = input("[USER] enter command: ")
          self.handle_command(cmd)
        # Other modes will recieve commands from server
        else:
          msg = Message.recieve_message(self.conn)
          if not msg:
            print(f'[CLOSE] server closed connection')
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn.close()
            self.running = False
          else:
            self.handle_message(msg)
    except KeyboardInterrupt:
      pass
    print('[CONNECTION] terminating connection bewteen client and server')
    self.conn.close()

  def handle_command(self, cmd):
    # disconnect user client from server
    if cmd.lower() in ['stop', 's']:
      self.running = False
    # shut server down
    elif cmd.lower() in ['shutdown', 'sd']:
      self.running = False
      Message.send_message(self.conn,'shutdown')
    # launch app on clients
    elif 'launch' in cmd.lower():
      if self.validate_command(cmd):
        Message.send_message(self.conn,cmd)
      else:
        print('[COMMAND] comand must match format')
        print('[COMMAND] launch appname [client=all|left|middle|right]')
    else:
      print('[COMMAND] invalid command')
  
  def validate_command(self,cmd) -> bool:
    regex = 'launch [a-z]+( client=(all|left|middle|right)){0,1}'
    return re.match(regex,cmd)

  def handle_message(self, msg):
    print(msg)
    pass

client = Client(mode=get_mode())
client.start_client()
