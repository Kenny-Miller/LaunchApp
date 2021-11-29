from client import Client
import helper
from message import Message

class UserClient(Client):
  """
  UserClient is a tcp client implementation that allows user input

  Connects to a specified server and creates terminal for the user to send commands to other
  clients connected to the server
  """

  def __init__(self, server='127.0.0.1', port='5050') -> None:
    """
    Constructor for the UserClient
    """
    super().__init__(server=server,port=port,type='user')

  def handle(self) -> None:
    """
    Starts the client.

    Runs in terminal mode accepting commands from the user that will then be sent to the server and broadcasted to clients.
    """
    self.establish_connection()
    while self.running:
      cmd = input("Please enter command: ").lower()
      if cmd in ['stop', 's']:
        # Closes client connection, but server still runs
        self.running = False
      elif cmd in ['shutdown', 'sd']:
        # Terminates server and all client connections
        self.running = False
        Message.send_message(conn=self.conn, msg='shutdown')
      elif cmd.lower() == 'vlc':
        # Puts user client in vlc mode
        self.handle_vlc_commands()
      elif cmd.lower() == 'test':
        # Sends a test message to echo on all connected clients
        Message.send_message(conn=self.conn, msg='test')
      else:
        print('[COMMAND] invalid command')

    self.close_connection()

  def handle_vlc_commands(self) -> None:
    """
    Handles sending vlc commands to server

    Uses seperate commands from handle() commands. 
    """
    self.logger.info('[Mode] running in vlc mode')
    runVlc = True
    clients = input("Please enter which clients you would like to run media on [all|left|middle|right]\nClients: ").lower()
    while runVlc:
      # valid actions: play, pause, exit, load, init
      cmd = input("Enter vlc command: ").lower()
      extra_arg = ""
      if cmd == 'load':
        extra_arg = 'filename=' + input("Please enter media filename: ")
      elif cmd == 'exit':
        runVlc = False
      msg = f'vlc action={cmd} client={clients} {extra_arg}'
      Message.send_message(conn=self.conn, msg=msg) 
    self.logger.info('[Mode] exiting vlc mode')

def main():
  client = UserClient(server='192.168.50.36')
  client.handle()

if __name__ == "__main__":
  main()