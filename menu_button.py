import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='GtkMenuButton Demo')

    self.set_default_size(400, 300)
    self.set_border_width(20)

    self.scrolled_win = gtk.ScrolledWindow()
    self.add(self.scrolled_win)

    self.vbox = gtk.VBox()
    self.scrolled_win.add(self.vbox)

    self.info_label = gtk.Label('Please select an action')
    self.vbox.pack_end(self.info_label, True, True, 0)

    self.menu_btn = gtk.MenuButton()
    self.menu_btn.set_halign(gtk.Align.CENTER)
    self.menu_btn.set_valign(gtk.Align.CENTER)

    self.menu = gtk.Menu()
    self.menu_btn.set_popup(self.menu)

    for i in range(10):
      menu_item = gtk.MenuItem.new_with_label(
        'Do something {}'.format(i + 1))
      menu_item.connect('activate', self.on_menu_item_acitvate)
      self.menu.append(menu_item)

    self.menu.show_all()
    self.vbox.pack_start(self.menu_btn, False, False, 0)

  def on_menu_item_acitvate(self, widget):
    activity = widget.get_label()
    self.info_label.set_label(activity)


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
