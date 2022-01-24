import math
from PyQt5.QtCore import Qt
from videoplayer import VideoPlayer

class WallVideoPlayer(VideoPlayer):
  def __init__(self, type='m', data_queue=None):
    super().__init__(data_queue=data_queue)
    self._createUI()
    self.vboxlayout.setContentsMargins(0, 0, 0, 0)
    #self.setWindowFlag(Qt.FramelessWindowHint)
    self.type = type
    self.timer.start()

  def play(self):
    (width, height) = self.media_player.video_get_size()
    slice = math.floor(width/3)
    geometry = ''
    match self.type:
      case 'l': geometry = f"{slice}x{height}+{0}+{0}"
      case 'm': geometry = f"{2*slice}x{height}+{slice}+{0}"
      case 'r': geometry = f"{3*slice}x{height}+{2*slice}+{0}"
      case  _ : geometry = f"{width}x{height}+{0}+{0}" 
    self.media_player.video_set_crop_geometry(geometry)
    self.resize(slice,height)
    super().play()

  def handle(self):
    if not self.data_queue.empty():
      msg = self.data_queue.get_nowait()
      msg_header = msg.split(" ")[0]
      match msg_header:
        case 'open': self.openFile(msg.split(" ")[1])
        case 'play': self.play()
        case 'pause': self.pause()
        case '': self.close()
        #case 'set': self.setTime(int(msg.split(" ")[1]))

  def open(self):
    super().open()
    