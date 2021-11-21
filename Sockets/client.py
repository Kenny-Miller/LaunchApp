import socket, sys, logging
import helper
from message import Message
from videoplayer import VideoPlayer

class Client():
  def __init__(self, server='127.0.0.1', port='5050', type='user') -> None:
    self.server = server
    self.port = int(port)
    self.running = False
    self.conn = None
    self.videoplayer = None
    self.type = type
    self.logger = logging.getLogger('client')
    self.config_logger()

  def config_logger(self) -> None:
    self.logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    self.logger.addHandler(ch)

  def start_client(self) -> None:
    self.logger.debug('[STARTUP] starting client')
    self.running = True
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.conn.connect((self.server, self.port))
    self.logger.info(f'[Connection] client connected to {self.server}:{self.port}')

    # Tell server what type of client this is
    self.logger.info(f'[Connection] telling server client is type: {self.type}')
    Message.send_message(self.conn,self.type)

    if self.type == 'user':
      self.handle_command()
    else:
      self.handle_message()
    self.logger.info('[Shutdown] shutting down client connection')
    self.conn.shutdown(socket.SHUT_RDWR)
    self.conn.close()

  # Handles commands from the user clients
  def handle_command(self) -> None:
    try:
      while self.running:
        cmd = input("Please enter command: ")
        # disconnect user client from server
        # server and other clients will not be affected
        if cmd.lower() in ['stop', 's']:
          self.running = False
        # shut server down
        # server will close conections with all other clients
        elif cmd.lower() in ['shutdown', 'sd']:
          self.running = False
          Message.send_message(self.conn,'shutdown')
        # prints all current command uses
        elif cmd.lower() in ['help', 'h']:
          helper.print_valid_cmd_list()
        # non-special command
        elif cmd.lower() == 'vlc':
          self.handle_vlc_commands()
        else:
          print('[COMMAND] invalid command')
          print('[COMMAND] type help or h for a full list of commands')   
    except KeyboardInterrupt:
      self.logger.debug('[User] user has stopped client')
    except Exception as e:
      self.logger.error(f'[Error] an error has occured, {e}\n') 

  # Handles messages recieved from the server
  def handle_message(self) -> None:
    try:
      while self.running:
        msg = Message.recieve_message(self.conn)
        self.logger.debug(f'[Message] client recieved message {msg} from server')
        if not msg:
          self.logger.info('[Connection] server has closed client connection')
          self.running = False
        else:
          exe = msg.split(" ")
          if exe[0] == 'vlc':
            self.handle_vlc_messages()
          else:
            self.logger.debug('[Message] client recieved an invalid message from server')
    except KeyboardInterrupt:
      self.logger.debug('[User] user has stopped client')
    except Exception as e:
      self.logger.error(f'[Error] an error has occured, {e}\n')    

  def handle_vlc_commands(self) -> None:
    print('[Mode] running in vlc mode')
    clients = input("Please enter which clients you would like to run media on [all|left|middle|right]\nClients: ")
    if clients.lower() in ['all', 'left', 'middle', 'right']:
      Message.send_message(self.conn, f"vlc client={clients}")
      runVlc = True
      while runVlc:
        cmd = input("Enter vlc command: ").lower()
        if cmd in ['play','pause','load','exit']:
          Message.send_message(self.conn, f'{cmd} client={clients}')
          if cmd == 'exit':
            runVlc = False
          elif cmd == 'load':
            filename = input("Enter media file: ").lower()
            Message.send_message(self.conn, f'{filename} client={clients}')
        else:
          print('[Error] invalid vlc input')
    else:
      print('[Error] invalid client input')
    print('[Mode] exiting vlc mode')

  def handle_vlc_messages(self) -> None:
    print('[Mode] running in vlc mode')
    mediaplayer = VideoPlayer()
    runVlc = True
    while runVlc:
      msg = Message.recieve_message(self.conn)
      cmd = msg.split(" ")[0]

      if cmd == 'play':
        mediaplayer.play_media()
      elif cmd == 'pause':
        mediaplayer.pause_media()
      elif cmd == 'load':
        filemsg = Message.recieve_message(self.conn)
        filename = filemsg.split(" ")[0]
        mediaplayer.load_media(filename)
      elif cmd == 'exit':
        runVlc = False
        mediaplayer.exit_player()
    print('[Mode] exiting vlc mode') 

# Determine which type to run in
# User type is a one-way connection that allows you to send commands to the server
# Auto type is a two-way connection that waits for messages from server
def get_type():
  type = 'user'
  if len(sys.argv) > 1:
    if sys.argv[1].lower() in ['left','l']:
      type = 'left'
    elif sys.argv[1].lower() in ['middle','m']:
      type = 'middle'
    elif sys.argv[1].lower() in ['right','r']:
      type = 'right'
  return type  

def main():
  client = Client(type=get_type())
  client.start_client()

if __name__ == "__main__":
  main()