import vlc

class VideoPlayer():
  def __init__(self) -> None:
    self.media_player = vlc.MediaPlayer()
    self.media = None
    self.media_player.set_fullscreen(True)

  def load_media(self, file):    
    self.media = vlc.Media(file)
    self.media_player.set_media(self.media)

  def play_media(self):
    self.media_player.play()

  def pause_media(self):
    self.media_player.pause()

  def exit_player(self):
    self.running = False
    self.media_player.stop()

  def resize_player(self):
    self.media_player.toggle_fullscreen()

  # Start video player to run with command line input
  def start_player(self):
    running = True
    while running:
      command = input("Input command: ")
      if command == 'play':
        self.play_media()
      elif command == 'pause':
        self.pause_media()
      elif command == 'load':
        file = input("Please specify file location: ")
        file = "sample.mp4"
        self.load_media(file)
      elif command == 'resize':
        self.resize_player()
      elif command == 'exit':
        self.exit_player()
  
def main():
  player = VideoPlayer()
  player.start_player()

if __name__ == "__main__":
  main()