import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='GtkFilechooserButton Demo')

    self.set_default_size(200, 150)

    self.scrolled_win = gtk.ScrolledWindow()
    self.add(self.scrolled_win)

    self.vbox = gtk.VBox()
    self.scrolled_win.add(self.vbox)
    self.vbox.set_border_width(20)
    self.vbox.set_spacing(20)

    self.file_chooser_btn = gtk.FileChooserButton(
      'Choose some file', gtk.FileChooserAction.OPEN)
    self.vbox.add(self.file_chooser_btn)
    self.file_chooser_btn.connect(
      'file-set', self.on_file_chooser_btn_file_set)

    self.info_btn = gtk.Button.new_with_mnemonic('_Info')
    self.vbox.add(self.info_btn)
    self.info_btn.connect('clicked', self.on_info_btn_clicked)


  def on_info_btn_clicked(self, widget):
    self.show_selected_file_info()

  def on_file_chooser_btn_file_set(self, widget):
    self.show_selected_file_info()

  def show_selected_file_info(self):
    message = self.file_chooser_btn.get_filename()
    if (message == None) or (message.strip() == ''):
      message = 'There is no file selected yet.'
    dialog = gtk.MessageDialog(
      self, gtk.DialogFlags.MODAL, gtk.MessageType.INFO,
      gtk.ButtonsType.OK, 'Selected File')
    dialog.format_secondary_text(message)
    dialog.set_border_width(20)
    dialog.run()
    dialog.destroy()


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
