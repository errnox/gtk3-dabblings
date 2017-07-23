import datetime

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='Buttons Demo')

    self.set_default_size(900, 600)

    self.scrolled_win = gtk.ScrolledWindow()
    self.add(self.scrolled_win)

    self.vbox = gtk.VBox()
    self.scrolled_win.add(self.vbox)
    self.vbox.set_spacing(20)
    self.vbox.set_border_width(20)
    self.vbox.set_homogeneous(False)

    # self.new_customer_rows = []

    self.customer_rows_box = gtk.VBox()
    self.customer_rows_box.set_spacing(20)
    self.vbox.pack_start(self.customer_rows_box, False, False, 0)

    for i in range(3):
      self.customer_rows_box.pack_start(
        self.create_new_customer_row(), False, False, 0)

    self.create_new_customer_row_btn_box = gtk.HBox()
    self.create_new_customer_row_btn_box.set_border_width(40)
    self.create_new_customer_row_btn = gtk.Button.new_with_mnemonic(
      '_Add row')
    self.create_new_customer_row_btn_box.pack_start(
      self.create_new_customer_row_btn, True, True, 0)
    self.vbox.pack_start(
    self.create_new_customer_row_btn_box, False, False, 0)
    self.create_new_customer_row_btn.connect(
      'clicked', self.on_create_new_customer_row_btn_clicked)

  def create_new_customer_row(self):
    hbox = gtk.HBox()
    hbox.set_spacing(10)

    # The following code could be used to replace the `HBox' to
    # account for smaller window sizes. However, doing so will mess
    # with the nice focus chain ("tabbing through") thta the `HBox'
    # solution provides.
    #
    # hbox = gtk.FlowBox()
    # hbox.set_max_children_per_line(10)
    # hbox.set_selection_mode(gtk.SelectionMode.NONE)

    first_name_label = gtk.Label('First Name: ')
    first_name_label.set_property('xalign', 0.0)
    hbox.add(first_name_label)
    first_name_entry = gtk.Entry()
    first_name_entry.set_property('placeholder-text', 'John')
    hbox.add(first_name_entry)

    hbox.add(gtk.Separator(orientation=gtk.Orientation.VERTICAL))
    last_name_label = gtk.Label('Last Name: ')
    last_name_label.set_property('xalign', 0.0)
    hbox.add(last_name_label)
    last_name_entry = gtk.Entry()
    last_name_entry.set_property('placeholder-text', 'Doe')
    hbox.add(last_name_entry)

    hbox.add(gtk.Separator(orientation=gtk.Orientation.VERTICAL))
    timestamp_label = gtk.Label('Timestamp: ')
    timestamp_label.set_property('xalign', 0.0)
    hbox.add(timestamp_label)
    timestamp_entry = gtk.Entry()
    timestamp_entry.set_property('xalign', 0.5)
    timestamp_entry.set_property('editable', False)
    timestamp_entry.set_property('has-frame', False)
    timestamp_entry.set_property('secondary-icon-name', 'info')
    timestamp_entry.set_property('secondary-icon-activatable', False)
    timestamp_entry.set_property('secondary-icon-sensitive', False)
    timestamp_entry.set_property(
      'secondary-icon-tooltip-text', 'This field is not editable')
    timestamp_entry.set_text(datetime.datetime.now().strftime(
      '%H:%M:%S'))
    hbox.add(timestamp_entry)

    hbox.add(gtk.Separator(orientation=gtk.Orientation.VERTICAL))
    remove_btn = gtk.Button.new_from_icon_name(
      'window-close', gtk.IconSize.BUTTON)
    remove_btn.set_property('relief', gtk.ReliefStyle.NONE)
    remove_btn.set_tooltip_text('Remove this row')
    remove_btn.connect(
      'clicked', self.on_new_customer_row_remove_btn_clicked, hbox)
    hbox.add(remove_btn)

    # DO NOT REMOVE THIS COMMENT!
    #
    # Demo: Iterate through the row containers.
    #
    # (This is not perfect, but it can be a startig point. There may
    # be a off-by-one-error; fix it yourself, if needed.)
    #
    # children = self.customer_rows_box.get_children()
    # for child in children:
    #   child_children = child.get_children()
    #   for child_child in child_children:
    #     if type(child_child) == gi.repository.Gtk.Entry:
    #       child_child.set_text('foo')
    #       print(child_child.get_text())

    return hbox

  def on_create_new_customer_row_btn_clicked(self, widget):
    self.customer_rows_box.pack_start(
      self.create_new_customer_row(), False, False, 0)
    self.customer_rows_box.show_all()

  def on_new_customer_row_remove_btn_clicked(self, widget, container):
    container.destroy()


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.connect('destroy', gtk.main_quit)
  win.show_all()
  gtk.main()
