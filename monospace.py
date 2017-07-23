import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Pango as pango


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='Monospace Font')

    self.set_default_size(500, 400)

    self.scrolled_win = gtk.ScrolledWindow()
    self.add(self.scrolled_win)

    # GtkTextView

    self.text_view_frame = gtk.Frame()
    self.scrolled_win.add(self.text_view_frame)
    self.text_view_scrolled_win = gtk.ScrolledWindow()
    self.text_view_frame.add(self.text_view_scrolled_win)

    self.text_view = gtk.TextView()
    self.text_view_scrolled_win.add(self.text_view)

    self.font_desc = pango.FontDescription('Monospace')
    self.text_view.modify_font(self.font_desc)


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.connect('destroy', gtk.main_quit)
  win.show_all()
  gtk.main()
