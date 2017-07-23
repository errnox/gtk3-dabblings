import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class MainWin(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='Test Application')

    self.vbox = gtk.VBox(True, 2, spacing=10)

    self.label = gtk.Label('Hello there!', halign=gtk.Align.END)
    self.vbox.add(self.label)

    self.spin_btn = gtk.Button(label='Spin')
    self.spin_btn.connect('clicked', self.spin_label)
    self.vbox.pack_start(self.spin_btn, expand=True, fill=True,
                         padding=0)

    self.button = gtk.Button(label='Click me!')
    self.button.connect('clicked', self.on_button_clicked)
    self.vbox.add(self.button)

    self.add(self.vbox)

    self.btn_counter = 0
    self.spin_angle = 0

  def on_button_clicked(self, widget):
    print('Hello there!')
    gtk.main_quit()
    # self.btn_counter += 1
    # new_button = gtk.Button(label='Button #{}'.format(self.btn_counter))
    # new_button.connect('clicked', self.on_button_clicked)
    # self.vbox.add(new_button)

  def spin_label(self, widget):
    if self.spin_angle < 360:
      self.spin_angle += 10
    else:
      self.spin_angle = 0
    self.label.props.angle = self.spin_angle

if __name__ == '__main__':
  win = MainWin()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
