import sys
from client import Client
from queue import Queue
from videoplayer_wall import WallVideoPlayer
from PyQt5.QtWidgets import (
  QApplication, 
)

class WallClient(Client):
  def __init__(self, server='127.0.0.1', port='5050',type='m', data_queue=None) -> None:
    super().__init__(server=server,port=port,type=type, data_queue=data_queue)

  def handle(self) -> None:
    self.establish_connection()
    while self.running:
      msg = self.conn.recv(1024).decode('utf-8')
      self.logger.info(f"[Message] Received msg: {msg}") 
      if not msg:
        self.running = False
      self.data_queue.put(msg)
    self.close_connection()

if __name__ == "__main__":
  if len(sys.argv) <= 3:
    print("Use $ server.py <addr> <port> <type>")
    
  server =  '127.0.0.1' if len(sys.argv) <= 3 else sys.argv[1]
  port = 5050 if len(sys.argv) <= 3 else sys.argv[2]
  type = 'm' if len(sys.argv) <=3 else sys.argv[3]
  data_queue = Queue()
  app = QApplication([])
  player = WallVideoPlayer(type=type, data_queue=data_queue)
  _ = WallClient(server=server, port=port, type=type, data_queue=data_queue)
  player.show()
  sys.exit(app.exec())