class Message():
  HEADER = 64

  # Handles recieving messages. Assumes two messages will be sent.
  # One message with message length and one message with message content.
  @classmethod
  def recieve_message(cls, conn) -> str:
    msg = ''
    msg_length = conn.recv(cls.HEADER).decode('utf-8')
    if msg_length:
      msg_length = int(msg_length)
      msg = conn.recv(msg_length).decode('utf-8')
    return msg

  # Handles sending messages. Sends two messages at a time
  # One message wtih message length and one message with message content.
  @classmethod
  def send_message(cls, conn, msg) -> None:
    message = msg.encode('utf-8')
    msg_length = len(message)
    send_length = str(msg_length).encode('utf-8')
    send_length += b' ' * (cls.HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


