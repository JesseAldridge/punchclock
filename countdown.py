
import time
from threading import Thread
from datetime import datetime, timedelta
from os.path import join

from PySide.QtGui import *
from PySide.QtCore import *

from jca.qtwrap import app

def countdown(window, minutes, and_then=lambda: None, count_session=False):

  # One label for time, one for number of countdowns transpired.

  session_label, time_label = window.session_label, window.time_label
  if count_session:
    session_label.count += 1
    session_str = unicode(session_label.count)
    session_label.setText(session_str)
  def tick(text):
    time_label.setText(text)
    app.g.app.processEvents()

  # Run the countdown in separate thread.  Ding when time is up.
  def on_done():
    if session_label.count == 6:  bell_path = 'hibell.wav'
    else:  bell_path = 'bell.wav'
    QSound.play(bell_path)
    and_then()
  t = Thread(target=lambda: countdown_(minutes, tick, on_done))
  t.start()

def countdown_(minutes, tick, on_done):

  # Loop until time is up

  start_time = datetime.now()
  while not is_closed():
    so_far = datetime.now() - start_time
    remaining = timedelta(minutes=minutes) - so_far
    if remaining <= timedelta(seconds=0):
      app.post_function(on_done)
      break
    seconds = unicode(remaining.seconds % 60)
    if len(seconds) == 1:  seconds = '0' + seconds
    text = ':'.join([unicode(remaining.seconds / 60), seconds])
    app.post_function(lambda: tick(text))
    time.sleep(1)

def is_closed():
  return app.g.app.is_closed

if __name__ == '__main__':
  app.start_if_havent()
  window = QWidget()
  layout = QVBoxLayout()
  window.setLayout(layout)
  window.time_label = time_label = QLabel()
  window.session_label = session_label = QLabel()
  session_label.count = 5
  for label in [time_label, session_label]: layout.addWidget(label)
  window.show()
  countdown(window, minutes=.02, count_session=True)
  app.launch_if_havent()