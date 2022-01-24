from abc import abstractmethod
from vlc import Instance
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
  QWidget,
  QVBoxLayout,
  QFrame,
  QMainWindow
)

class VideoPlayer(QMainWindow):
  def __init__(self, parent=None, data_queue=None):
    super().__init__(parent)
    self.data_queue=data_queue
    self.instance = Instance()
    self.media_player = self.instance.media_player_new()
    self.media = None
    self.timer = QTimer(self)
    self.timer.setInterval(25)
    self.timer.timeout.connect(self.handle)

  def _createUI(self):
    self.widget = QWidget(self)
    self.setCentralWidget(self.widget)
    self.videoframe = QFrame()
    self.vboxlayout = QVBoxLayout()
    self.vboxlayout.addWidget(self.videoframe)
    self.widget.setLayout(self.vboxlayout)

  def openFile(self, filepath):
    self.media = self.instance.media_new(filepath)
    self.media_player.set_media(self.media)
    self.media.parse()
    self.media_player.set_hwnd(int(self.videoframe.winId()))

  def play(self):  
    self.media_player.play()

  def pause(self):
    self.media_player.pause()

  def setTime(self, time):
    self.media_player.set_time(time)
  
  @abstractmethod
  def handle(self):
    raise NotImplementedError()

