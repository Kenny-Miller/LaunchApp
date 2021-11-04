import socket, sys

SERVER = '127.0.0.1'  # The server's hostname or IP address
PORT = 5050        # The port used by the server
HEADER = 64

# Determine which mode to run in
# User mode is a one-way connection that allows you to send commands to the server
# Auto mode is a two-way connection that waits for messages from server
def get_mode():
  mode = 'auto'
  if len(sys.argv) > 1 and sys.argv[1].lower() in ['user','u']:
    mode = 'user'
  return mode  

# Starts up the client 
def start_client(mode):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
    
    # Handles recieving messages from the server
    # Server will send 2 messages: one with message length and one with the actual message
    def recieve_message():
      msg = ''
      msg_length = conn.recv(HEADER).decode('utf-8')
      if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode('utf-8')
        print(f'[MESSAGE] client recieved {msg} from server')
      return msg

    # Handles what to do with a message sent from the server
    def handle_message(msg):
      pass

    # Sends a message to the server
    # Will always send two messages to the server: one stating the message length and one containg the message
    def send_message(msg):
      message = msg.encode('utf-8')
      msg_length = len(message)
      send_length = str(msg_length).encode('utf-8')
      send_length += b' ' * (HEADER - len(send_length))
      print(f'[MESSAGE] sending message {message} to server')
      conn.send(send_length)
      conn.send(message)
    
    # Sends a message to the server saying that the client is closing the connection
    def close_connection():
      send_message("!QUIT!")
      conn.close()

    conn.connect((SERVER, PORT))
    print(f'[Connection] client connected to {SERVER}:{PORT}')
    try:
      running = True
      while running:
        if mode == 'user':
          msg = input("[USER] Enter command: ")
          if msg.lower() in ['quit', 'q', 'exit']:
            running = False
          else :
            send_message(msg)
        else:
          msg = recieve_message()
          handle_message(msg) 

    except Exception as e:
      print('An exception occurred: {}'.format(e))
    except KeyboardInterrupt:
      pass
    print('[CONNECTION] Terminating connection bewteen client and server')
    close_connection()

mode = get_mode()
start_client(mode) 

      
    
    