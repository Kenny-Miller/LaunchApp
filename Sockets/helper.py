import re

# Prints a list of valid commands the user client can run
def print_valid_cmd_list() -> None:
  print('[HELP] help (h)')
  print('[HELP] stop (s)')
  print('[HELP] shutdown (sd)')
  print('[HELP] vlc <filename> client=[all|left|middle|right]')
  # Add new applications here

# Validates a message from user client
def validate_cmd(msg) -> bool:
  regexs = [
    'vlc \w+ client=(all|left|middle|right)'
    # insert more regexs
    # they should follow convention of: ... ...  client=(all|left|middle|right)
  ]
  temp = '(?:% s)' % '|'.join(regexs)
  return re.match(temp, msg)

# Takes a messages and maps it to an exec cmd
def map_msg_to_exe(msg, selfType) -> str: 
  msgType = msg.split("client=")[1]

  exeMode = 'standalone'
  if msgType != selfType:
    exeMode = 'shared'


  pass
