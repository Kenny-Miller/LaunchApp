from client import Client
import helper
from message import Message

class UserClient(Client):

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
        # disconnect user client from server
        # server and other clients will not be affected
        if cmd.lower() in ['stop', 's']:
          self.running = False
        # shut server down
        # server will close conections with all other clients
        elif cmd.lower() in ['shutdown', 'sd']:
          self.running = False
          Message.send_message(conn=self.conn, msg='shutdown')
        # prints all current command uses
        elif cmd.lower() in ['help', 'h']:
          helper.print_valid_cmd_list()
        # non-special command
        elif cmd.lower() == 'vlc':
          self.handle_vlc_commands()
        # sends a test message
        elif cmd.lower() == 'test':
          self.conn.send('test'.encode('utf-8'))
        else:
          print('[COMMAND] invalid command')
          print('[COMMAND] type help or h for a full list of commands')
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