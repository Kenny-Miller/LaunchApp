import sys
from queue import Queue
from client import Client
from videoplayer_user import UserVideoPlayer

from PyQt5.QtWidgets import (
  QApplication, 
)

class UserClient(Client):
  def __init__(self, server='127.0.0.1', port='5050', data_queue=None) -> None:    
    super().__init__(server=server,port=port,type='u', data_queue=data_queue)

  def handle(self) -> None:
    self.establish_connection()
    while self.running:
      if not self.data_queue.empty():
        msg = self.data_queue.get_nowait()
        self.conn.send(msg.encode('utf-8'))
    self.close_connection()

if __name__ == "__main__":
  if len(sys.argv) <= 2:
    print("Use $ server.py <addr> <port>")

  server =  '127.0.0.1' if len(sys.argv) <= 2 else sys.argv[1]
  port = 5050 if len(sys.argv) <= 2 else sys.argv[2]
  data_queue = Queue()
  app = QApplication([])
  player = UserVideoPlayer(data_queue=data_queue)
  _ = UserClient(server=server, port=port,data_queue=data_queue)
  player.show()
  sys.exit(app.exec())