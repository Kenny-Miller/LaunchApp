import socket, threading

HOST = '127.0.0.1'  
PORT = 5050        
HEADER = 64

def handle_conn(conn, addr):
  print(f'[CONNECTION] server accepted connected with {addr}')
  connected = True

  # Handles recieving messages from a client
  # Client will send 2 messages: one with message length and one with the actual message
  def recieve_message():
    msg = ''
    msg_length = conn.recv(HEADER).decode('utf-8')
    if msg_length:
      msg_length = int(msg_length)
      msg = conn.recv(msg_length).decode('utf-8')
      print(f'[MESSAGE] server recieved {msg} from {addr}')
    return msg
  
  # Sends a message to a client
  # Will always send two messages to the client: one stating the message length and one containg the message
  def send_message(msg):
    message = msg.encode('utf-8')
    msg_length = len(message)
    send_length = str(msg_length).encode('utf-8')
    send_length += b' ' * (HEADER - len(send_length))
    print(f'[MESSAGE] sending message {message} to client')
    conn.send(send_length)
    conn.send(message)

  # Handles what to do with a message sent from a client
  def handle_message(msg):
    if msg == 'test':
      print('made it')

  # Wait and handle sending and recieveing messages to the client
  while connected:
      msg = recieve_message()
      if msg == '!QUIT!':
        connected = False
      else:
        handle_message(msg)

  print(f'[CONNECTION] server is disconnecting from {addr}')
  print(f'[INFO] current number of connections is {threading.active_count() -1}')
  conn.close()

def start_server():
  # Create listening socket on server
  print('[STARTUP] starting server')
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener: 
    listener.bind((HOST, PORT))
    listener.listen(5)
    print(f'[STARTUP] server is now listening on: {HOST}:{PORT}')

    # Loop forever
    try:
      while True:
        # Create a new thread that handles a connection to the server
        (conn, addr) = listener.accept()
        thread = threading.Thread(target=handle_conn, args=(conn,addr))
        thread.start()
        print(f'[INFO] current number of connections is {threading.active_count() -1}')
    except KeyboardInterrupt:
      print('interupt')
      return 

start_server()
