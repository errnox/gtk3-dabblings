import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='Revealer Demo')

    self.is_revealed = False

    self.hbox = gtk.HBox()
    self.add(self.hbox)
    self.hbox.set_border_width(20)

    self.revealer = gtk.Revealer()
    self.hbox.add(self.revealer)
    self.revealer.set_border_width(40)

    self.label = gtk.Label()
    self.label.set_markup(
      '<span foreground="#ffffff" background="#883322">This is a revealer demo</span>')

    self.button = gtk.Button.new_with_mnemonic('_Reveal')
    self.hbox.add(self.button)
    self.button.connect('clicked', self.on_button_clicked)

    self.revealer.add(self.label)
    self.revealer.set_transition_duration(800)
    self.revealer.set_transition_type(
      gtk.RevealerTransitionType.CROSSFADE)

  def on_button_clicked(self, widget):
    self.is_revealed = not self.is_revealed
    print(self.is_revealed)
    self.revealer.set_reveal_child(self.is_revealed)


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
