
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
  QMenu,
  QFileDialog,
  QAction,
  QHBoxLayout,
  QPushButton,
  QStyle,
)
from videoplayer import VideoPlayer

class UserVideoPlayer(VideoPlayer):
  def __init__(self, data_queue=None):
    super().__init__(data_queue=data_queue)
    self._createUI()
    self.resize(640, 480)

  def _createUI(self):
    super()._createUI()
    self.setWindowTitle("Video Controller")
    self._createMenuBar()
    buttonLayout = self._createButtonLayout()
    self.vboxlayout.addLayout(buttonLayout)

  def _createMenuBar(self):
    menuBar = self.menuBar()
    openAction = QAction("&Open", self)
    exitAction = QAction("&Exit", self)
    openAction.triggered.connect(self.openFile)
    exitAction.triggered.connect(self.exit)
    fileMenu = QMenu("&File", self)
    fileMenu.addAction(openAction)
    fileMenu.addAction(exitAction)
    menuBar.addMenu(fileMenu)
    self.setMenuBar(menuBar)

  def _createButtonLayout(self):
    playButton = QPushButton()
    playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    playButton.clicked.connect(self.play)
    playButton.setFixedWidth(40)
    pauseButton = QPushButton()
    pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
    pauseButton.clicked.connect(self.pause)
    pauseButton.setFixedWidth(40)
    layout = QHBoxLayout()
    layout.setAlignment(Qt.AlignLeft)
    layout.addWidget(playButton)
    layout.addWidget(pauseButton)
    return layout

  def openFile(self):
    options = QFileDialog.Options()
    filepath, _ = QFileDialog.getOpenFileName(
        self, "Select Media", "", "All Files (*)", options=options)
    if not filepath:
      return
    super().openFile(filepath)
    self.setWindowTitle(f"Media: {filepath}")  
    self.data_queue.queue.clear()
    self.data_queue.put(f"open {filepath}")

  def exit(self):
    self.data_queue.put("exit")
    self.close()

  def close(self):
    self.data_queue.put("exit")
    super().close()

  def play(self):
    self.data_queue.put("play")
    self.timer.start()
    super().play()

  def pause(self):
    self.data_queue.put("pause")
    self.timer.stop()
    super().pause()

  def handle(self):
    if self.media_player.is_playing():
      self.data_queue.put(f"time {self.media_player.get_time()}")
    else:
      self.pause()
