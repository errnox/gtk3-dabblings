#
# DISCLAIMER: THIS IS NOT FUNCTIONAL!
#

import gi


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Pango as pango

import webkit


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='Monospace Font')

    self.set_default_size(500, 400)

    self.scrolled_win = gtk.ScrolledWindow()
    self.add(self.scrolled_win)

    self.web_view = webkit.WebView()
    self.scrolled_win.add(self.web_view)
    self.web_view.connect(
      'load-committed', self.on_web_view_load_committed)

    self.web_view.load_string('Hello there!')

  def on_web_view_load_committed(self, widget, frame):
    pass


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.connect('destroy', gtk.main_quit)
  win.show_all()
  gtk.main()
