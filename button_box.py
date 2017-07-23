import datetime

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='Revealer Demo')

    self.set_default_size(600, 400)

    self.is_revealed = False

    self.grid = gtk.Grid()
    self.add(self.grid)

    self.scrolled_win = gtk.ScrolledWindow()
    self.grid.attach(self.scrolled_win, 0, 1,  1, 1)
    self.scrolled_win.set_vexpand(True)
    self.scrolled_win.set_hexpand(True)

    self.vbox = gtk.VBox()
    self.scrolled_win.add(self.vbox)
    self.vbox.set_spacing(20)
    self.vbox.set_border_width(20)

    self.button_box_style_mappings = {
      'spread': gtk.ButtonBoxStyle.SPREAD,
      'edge': gtk.ButtonBoxStyle.EDGE,
      'start': gtk.ButtonBoxStyle.START,
      'end': gtk.ButtonBoxStyle.END,
      'center': gtk.ButtonBoxStyle.CENTER,
      'expand': gtk.ButtonBoxStyle.EXPAND
    }

    self.style_selector_cbox_label = gtk.Label(
      'Set the "GtkButtonBox" layout:')
    self.style_selector_cbox_label.set_property('xalign', 0)
    self.vbox.add(self.style_selector_cbox_label)

    self.style_selector_cbox = gtk.ComboBoxText()
    self.vbox.pack_start(self.style_selector_cbox, False, False, 0)
    self.style_selector_cbox.append('spread', 'SPREAD')
    self.style_selector_cbox.append('edge', 'EDGE')
    self.style_selector_cbox.append('start', 'START')
    self.style_selector_cbox.append('end', 'END')
    self.style_selector_cbox.append('center', 'CENTER')
    self.style_selector_cbox.append('expand', 'EXPAND')
    self.style_selector_cbox.connect(
      'changed', self.on_style_selector_cbox_changed)

    self.button_box = gtk.ButtonBox(gtk.Orientation.VERTICAL)
    self.button_box.set_layout(gtk.ButtonBoxStyle.END)
    self.style_selector_cbox.set_active_id('end')
    self.btn_cancel = gtk.Button.new_with_mnemonic('_Cancel')
    self.button_box.add(self.btn_cancel)
    self.btn_edit = gtk.Button.new_with_mnemonic('_Edit')
    self.button_box.add(self.btn_edit)
    self.btn_save = gtk.Button.new_with_mnemonic('_Save')
    self.button_box.add(self.btn_save)
    self.btn_help = gtk.Button.new_with_mnemonic('_Help')
    self.btn_help.connect('clicked', self.on_btn_help_clicked)
    self.button_box.add(self.btn_help)
    self.button_box.set_child_secondary(self.btn_help, True)
    self.vbox.add(self.button_box)

    self.separator = gtk.Separator()
    self.vbox.add(self.separator)

    # GtkExpander

    self.expander = gtk.Expander.new_with_mnemonic('_More Info')
    self.vbox.add(self.expander)

    self.expander_box = gtk.VBox()
    self.expander.add(self.expander_box)

    self.more_info_label = gtk.Label(
      'This application demonstrates how different "GtkButtonBox"'
      + ' layouts look like in a window.')
    self.expander_box.add(self.more_info_label)

    self.unexpand_btn_box = gtk.ButtonBox()
    self.expander_box.add(self.unexpand_btn_box)

    self.unexpand_btn = gtk.Button.new_with_mnemonic('_Got it')
    self.unexpand_btn_box.add(self.unexpand_btn)

    self.unexpand_btn.connect('clicked', self.on_unexpand_btn_clicked)

  def show_info_bar(self, message):
    self.info_bar = gtk.InfoBar()
    self.grid.attach(self.info_bar, 0, 0, 1, 1)
    self.info_bar.connect('response', self.on_info_bar_response)
    self.info_bar.set_show_close_button(True)
    self.info_bar.set_message_type(gtk.MessageType.INFO)

    self.info_bar_label = gtk.Label(message)
    self.info_bar_content_area = self.info_bar.get_content_area()
    self.info_bar_content_area.set_border_width(20)
    self.info_bar_content_area.add(self.info_bar_label)

    self.info_bar_more_info_button = gtk.Button.new_with_mnemonic(
      '_More info')
    self.info_bar_action_area = self.info_bar.get_action_area()
    self.info_bar_action_area.add(self.info_bar_more_info_button)
    self.info_bar_more_info_button.connect(
      'clicked', self.on_info_bar_more_info_button_clicked)

    self.info_bar.show_all()

  def on_btn_help_clicked(self, widget):
    try:
      self.info_bar
    except:
      time = datetime.datetime.now().strftime("%H:%M:%S")
      self.show_info_bar(
        '{}  -  This is a demo app.'.format(time))
    self.info_bar.show()

  def on_style_selector_cbox_changed(self, widget):
    id = self.style_selector_cbox.get_active_id()
    self.button_box.set_layout(self.button_box_style_mappings[id])

  def on_unexpand_btn_clicked(self, widget):
    self.expander.set_expanded(False)

  def on_info_bar_response(self, widget, data):
    self.info_bar.hide()

  def on_info_bar_more_info_button_clicked(self, widget):
    self.expander.set_expanded(True)

if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
