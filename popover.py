import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='GtkPopover Demo')

    self.set_default_size(500, 400)

    self.scrolled_win = gtk.ScrolledWindow()
    self.add(self.scrolled_win)

    self.vbox = gtk.VBox()
    self.scrolled_win.add(self.vbox)

    self.choose_action_btn = gtk.Button.new_with_mnemonic(
      'Choose _action')
    self.vbox.pack_end(self.choose_action_btn, False, False, 0)
    self.choose_action_btn.connect(
      'clicked', self.on_choose_action_btn_clicked)
    self.choose_action_btn.set_tooltip_text(
      'Choose an action from a popup')

    self.choose_action_popover = gtk.Popover()
    self.choose_action_popover.set_border_width(5)
    self.choose_action_popover.set_relative_to(
      self.choose_action_btn)
    self.choose_action_popover_box = gtk.VBox()
    self.choose_action_popover_box.set_spacing(10)
    self.choose_action_popover.add(self.choose_action_popover_box)

    # Info Button
    self.info_btn = gtk.Button.new_with_mnemonic('_Info')
    self.info_btn.connect('clicked', self.on_info_btn_clicked)
    self.choose_action_popover_box.pack_end(
      self.info_btn, False, False, 0)
    # Warning Button
    self.warning_btn = gtk.Button.new_with_mnemonic('_Warning')
    self.warning_btn.connect('clicked', self.on_info_btn_clicked)
    self.choose_action_popover_box.pack_end(
      self.warning_btn, False, False, 0)
    # Error Button
    self.Error_btn = gtk.Button.new_with_mnemonic('_Error')
    self.Error_btn.connect('clicked', self.on_info_btn_clicked)
    self.choose_action_popover_box.pack_end(
      self.Error_btn, False, False, 0)

  def on_choose_action_btn_clicked(self, widget):
    self.choose_action_popover.show_all()

  def on_info_btn_clicked(self, widget):
    self.choose_action_popover.hide()

    dialog = gtk.MessageDialog(
      self, gtk.DialogFlags.MODAL, gtk.MessageType.INFO,
      gtk.ButtonsType.OK, 'Here is some info.')
    dialog.set_border_width(20)
    dialog.run()
    dialog.destroy()


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
