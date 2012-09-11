
from PySide.QtGui import *
from PySide.QtCore import *

from jca.qtwrap import app

import countdown

def timer_gui(work_mins=25, rest_mins=5):

    # Create gui.  Clicking the button will call work, then rest, and so on.

    class Phase:
        def __init__(self, r,g,b, mins, count_session):
            self.rgb, self.mins, self.count_session = (
              (r,g,b), mins, count_session)

        def go(self):
          if countdown.is_closed():
            return
          set_color(window, *self.rgb)
          countdown.countdown(
            window, self.mins, count_session=self.count_session,
            and_then=self.and_then)

    rest = Phase(200,200,255, rest_mins, count_session=False)
    work = Phase(200,255,200, work_mins, count_session=True)
    rest.and_then, work.and_then = work.go, rest.go
    window = timer_window(work.go)
    return window

# Use post function because timer's running in another thread.

def click(window):  app.post_function(window.go_button.click)
def set_color(window, r,g,b):
  css_str = '* { background-color: rgb(%i,%i,%i) }' % (r,g,b)
  app.post_function(lambda: window.setStyleSheet(css_str))

def timer_window(go):

  # Setup layouts.

  window = QWidget()
  main_layout, top_row = QVBoxLayout(), QHBoxLayout()
  time_layout = QVBoxLayout()
  main_layout.addLayout(top_row)
  window.setLayout(main_layout)
  top_row.addLayout(time_layout)

  # Add the time and session labels.  Add go button.

  window.time_label = time_label = QLabel('-:--')
  window.session_label = session_label = QLabel('0')
  session_label.count = 0
  time_layout.addWidget(time_label)
  time_layout.addWidget(session_label)

  window.go_button = go_button = QToolButton()
  go_button.setText('Go')
  go_button.connect(go_button, SIGNAL('clicked()'), go)
  go_button.setMaximumSize(35,25)
  top_row.addWidget(go_button)
  window.show()
  return window

# Launch.

app.start_if_havent()
work_mins, rest_mins = 25, 5
# work_mins, rest_mins = .1, .1
win = timer_gui(work_mins=work_mins, rest_mins=rest_mins)
win.show()
app.launch_if_havent()
