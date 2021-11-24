import sys
from client import Client
from message import Message
from videoplayer import VideoPlayer

class SimpleClient(Client):
  def __init__(self, server='127.0.0.1', port='5050', type='middle') -> None:
    """
    Constructor for the SimpleClient
    """
    super().__init__(server=server,port=port,type=type)
    self.videoplayer = None

  def handle(self) -> None:
    """
    Handles messages recieved from server
    """
    self.establish_connection()
    while self.running:
      msg = Message.recieve_message(conn=self.conn)
      self.logger.debug(f'[Message] client recieved message {msg} from server')
      if not msg:
        self.logger.info('[Connection] server has closed client connection')
        self.running = False
      msg_header = msg.split(" ")[0]
      if msg_header == 'vlc':
        self.handle_vlc_message(msg)
      else:
        self.logger.debug('[Message] client recieved an invalid message from server')
      
    self.close_connection()

  # Handles messages pertaining to vlc
  # In format of 'vlc action=<> client=<> [filename=<>]
  def handle_vlc_message(self, msg) -> None:
    action = Message.parse_msg_arg(msg,'action=')
    if action == 'init':
      self.videoplayer = VideoPlayer()
    elif self.videoplayer is None:
      self.logger.debug('[Warning] videoplayer is null, command cannot be executed')
    elif action == 'play':
      self.videoplayer.play_media()
    elif action == 'pause':
      self.videoplayer.pause_media()
    elif action == 'load':
      filename = Message.parse_msg_arg(msg, 'filename=')
      self.videoplayer.load_media(filename)
    elif action == 'exit':
      self.videoplayer.exit_player()
      self.videoplayer = None

# Determine which type to run in
# User type is a one-way connection that allows you to send commands to the server
# Auto type is a two-way connection that waits for messages from server
def get_type():
  type = 'middle'
  if len(sys.argv) > 1:
    arg = sys.argv[1].lower()
    print(arg)
    if arg in ['left','l']:
      type = 'left'
    elif arg in ['right','r']:
      type = 'right'
  return type  

def main():
  client = SimpleClient(server='192.168.50.36',type=get_type())
  client.handle()

if __name__ == "__main__":
  main()