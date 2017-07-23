import random

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class FlowBoxChildWithData(gtk.FlowBoxChild):
  def __init__(self, data, child):
    super(gtk.FlowBoxChild, self).__init__()
    self.data = data
    self.add(child)


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='GtkFlowBox Demo')

    self.icon_names = [
      'network-error',
      'network-idle',
      'network-offline',
      'network-receive',
      'network-transmit',
      'network-transmit-receive'
    ]

    self.set_default_size(500, 400)
    self.set_border_width(10)

    self.vbox = gtk.VBox()
    self.add(self.vbox)
    self.vbox.set_spacing(10)

    # GtkEntry

    self.flowbox_filter_entry = gtk.Entry()
    self.vbox.pack_start(self.flowbox_filter_entry, False, False, 0)
    self.flowbox_filter_entry_buffer = self.flowbox_filter_entry.get_buffer()
    self.flowbox_filter_entry_buffer.connect(
      'inserted-text', self.on_flowbox_filter_entry_inserted_text)
    self.flowbox_filter_entry_buffer.connect(
      'deleted-text', self.on_flowbox_filter_entry_deleted_text)

    # GtkEntryCompletion

    self.flowbox_filter_entry_model = gtk.ListStore(str)
    for name in self.icon_names:
      self.flowbox_filter_entry_model.append([name])

    self.flowbox_filter_entry_completion = gtk.EntryCompletion()
    self.flowbox_filter_entry_completion.set_model(
      self.flowbox_filter_entry_model)
    self.flowbox_filter_entry_completion.set_text_column(0)
    self.flowbox_filter_entry_completion.set_popup_completion(True)
    self.flowbox_filter_entry_completion.set_inline_completion(False)
    self.flowbox_filter_entry_completion.set_minimum_key_length(0)
    self.flowbox_filter_entry_completion.set_match_func(
      self.flowbox_filter_entry_completion_match_func, 0)

    self.flowbox_filter_entry.set_completion(
      self.flowbox_filter_entry_completion)

    # GtkFlowBox

    self.scrolled_win = gtk.ScrolledWindow()
    self.vbox.pack_start(self.scrolled_win, True, True, 0)

    self.flowbox = gtk.FlowBox()
    self.scrolled_win.add(self.flowbox)
    self.flowbox.set_filter_func(self.filter_flowbox_children)

    for i in range(20):
      name = random.sample(self.icon_names, 1)[0]
      data = {'type': name}

      vbox = gtk.VBox()
      child = FlowBoxChildWithData(data, vbox)
      child.set_size_request(80, 150)
      child.set_valign(gtk.Align.START)
      self.flowbox.add(child)
      child.set_hexpand(False)
      child.set_vexpand(False)
      # Image
      image = gtk.Image.new_from_icon_name(
        name, gtk.IconSize.DIALOG)
      vbox.pack_start(image, True, False, 0)
      # Button
      button = gtk.Button('Machine #{}'.format(i + 1))
      vbox.pack_end(button, False, False, 0)

  def compare_input_with_type(self, user_input, type):
    return (type.find(user_input) >= 0) or (user_input.strip() == '')

  def filter_flowbox_children(self, child):
    type = child.data['type']
    user_input = self.flowbox_filter_entry.get_text()
    return self.compare_input_with_type(user_input, type)

  def on_flowbox_filter_entry_inserted_text(
      self, buffer, position, chars, n_chars):
    self.update_flowbox_filter()

  def on_flowbox_filter_entry_deleted_text(
      self, buffer, position, n_chars):
    self.update_flowbox_filter()

  def update_flowbox_filter(self):
    self.flowbox.invalidate_filter()

  def flowbox_filter_entry_completion_match_func(self, completion, key,
                                                 iter, column):
    user_input = completion.get_entry().get_text()
    model = completion.get_model()
    text = model.get_value(iter, column)
    return self.compare_input_with_type(user_input, text)


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
