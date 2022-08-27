import pynput.keyboard as Keyboard
import logging
import time

log_dir = r"C:/Users/John Kim/Desktop/ai/passWords/"
logging.basicConfig(filename = (log_dir + "keyLog.txt"), level=logging.DEBUG, format = '')#, format='%(asctime)s: %(message)s')
open('keyLog.txt', 'w').close()

ended = False

def on_press(key):
  if str(key) == 'Key.enter':
    return False
  logging.info(f'{time.time()} {str(key)} Pressed')

def on_release(key):
  logging.info(f'{time.time()} {str(key)} Released')

def runKlog():
  with Keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

if __name__ == '__main__':
  runKlog()