import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
# from gi.repository import Gdk as gdk


class MainWin(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='Test Application')

    # self.set_resizable(False)
    # self.set_border_width(10)
    # self.set_default_size(800, 500)

    self.main_box = gtk.VBox()
    self.add(self.main_box)

    self.header_bar = gtk.HeaderBar(title='Test Application')
    self.header_bar.set_decoration_layout(':close')
    self.set_titlebar(self.header_bar)
    self.header_bar.set_show_close_button(True)

    self.vbox = gtk.VBox(spacing=20, border_width=10)
    self.main_box.add(self.vbox)

    self.close_btn = gtk.Button.new_with_mnemonic('_Close')
    # self.close_btn.set_style()
    #
    # self.close_btn.override_color(
    #   gtk.StateFlags.NORMAL, gdk.RGBA(1.0, 0.0, 0.0, 1.0))
    #
    # self.close_btn.modify_fg(gtk.StateFlags.NORMAL, gdk.color_parse('blue'))
    #
    self.header_bar.pack_end(self.close_btn)
    self.close_btn.connect('clicked', gtk.main_quit)

    self.link_btn = gtk.LinkButton.new_with_label(
      'file:////usr/share/doc/debian/FAQ/index.html', 'Documentation')
    self.header_bar.pack_end(self.link_btn)

    self.spin_btn = gtk.SpinButton.new_with_range(0, 100, 10)
    self.header_bar.pack_start(self.spin_btn)
    self.spin_btn.set_value(20)

    self.color_btn = gtk.ColorButton()
    self.color_btn.set_title('Favorite Color')
    self.header_bar.pack_start(self.color_btn)

    # Switch

    self.switch = gtk.Switch()
    self.vbox.add(self.switch)

    # Entry

    self.text_entry = gtk.Entry()
    self.text_entry.set_text('something')
    self.vbox.add(self.text_entry)
    self.text_entry.connect(
      'move-cursor', lambda a, b, c, d: self.text_entry.progress_pulse())
    self.text_entry.connect('activate', self.munge_user_input)

    # Grid

    self.grid = gtk.Grid()
    self.vbox.add(self.grid)

    self.btn1 = gtk.CheckButton.new_with_mnemonic('B_utton 1')
    self.btn1.connect('clicked', self.toggle_feature)
    self.btn2 = gtk.Button('Button 2')
    self.btn3 = gtk.Button('Button 3')
    self.btn4 = gtk.Button('Button 4')
    self.btn5 = gtk.Button('Button 5')
    self.btn6 = gtk.Button('Button 6')
    self.btn7 = gtk.Button('Button 7')

    self.grid.attach(self.btn1, 0, 0, 1, 1)
    self.grid.attach(self.btn2, 1, 0, 1, 1)
    self.grid.attach(self.btn3, 2, 0, 1, 1)
    self.grid.attach(self.btn4, 0, 1, 2, 1)
    self.grid.attach(self.btn5, 2, 1, 1, 1)

    # ListBox

    self.list_box_container = gtk.Box()
    self.vbox.add(self.list_box_container)
    self.list_box = gtk.ListBox()
    self.list_box_container.add(self.list_box)
    self.list_box.set_selection_mode(gtk.SelectionMode.NONE)

    self.list_box_row = gtk.ListBoxRow(expand=True)
    self.list_box.add(self.list_box_row)
    self.color_label = gtk.Label('Color')
    self.color_row = gtk.HBox()
    self.list_box.add(self.color_row)
    self.color_row.add(self.color_label)
    self.color_selector = gtk.ColorButton()
    self.color_row.add(self.color_selector)

    # ComboBox

    self.fruit_combo_box = gtk.ComboBoxText()
    self.vbox.add(self.fruit_combo_box)
    for i, fruit in enumerate(
        ['Apple', 'Banana', 'Cherry', 'Strawberry']):
      self.fruit_combo_box.insert(i, fruit, fruit)
    self.fruit_combo_box.set_active(0)
    self.fruit_combo_box.connect('changed', self.select_fruit)
    self.fruit_popup_btn = gtk.Button('Popup Fruit')
    self.vbox.add(self.fruit_popup_btn)
    self.fruit_popup_btn.connect(
      'clicked', lambda x: self.fruit_combo_box.popup())

    # Stack

    self.vbox.add(gtk.Separator())

    self.stack = gtk.Stack()
    self.stack_check_btn = gtk.CheckButton('Checkbox')
    self.stack.add_titled(self.stack_check_btn, 'check', 'Checkbox')
    self.stack.set_transition_type(
      gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

    self.stack_label = gtk.Label()
    self.stack_label.set_markup('<big>This is a label.</big>')
    self.stack.add_titled(self.stack_label, 'label', 'Label')

    self.stack_level_bar_box = gtk.VBox()
    self.stack.add_titled(self.stack_level_bar_box, 'level', 'Level')
    self.stack_level_bar = gtk.LevelBar()
    self.stack_level_bar_box.add(self.stack_level_bar)
    self.stack_level_bar.set_value(0.3)
    # Button 1
    self.stack_level_bar_btn_1 = gtk.Button('10%')
    self.stack_level_bar_btn_1.connect(
      'clicked', lambda x: self.stack_level_bar.set_value(0.1))
    self.stack_level_bar_box.add(self.stack_level_bar_btn_1)
    # Button 2
    self.stack_level_bar_btn_2 = gtk.Button('50%')
    self.stack_level_bar_btn_2.connect(
      'clicked', lambda x: self.stack_level_bar.set_value(0.5))
    self.stack_level_bar_box.add(self.stack_level_bar_btn_2)
    # Button 3
    self.stack_level_bar_btn_3 = gtk.Button('80%')
    self.stack_level_bar_btn_3.connect(
      'clicked', lambda x: self.stack_level_bar.set_value(0.8))
    self.stack_level_bar_box.add(self.stack_level_bar_btn_3)
    # Button 4
    self.stack_level_bar_btn_4 = gtk.Button('100%')
    self.stack_level_bar_btn_4.connect(
      'clicked', lambda x: self.stack_level_bar.set_value(1.0))
    self.stack_level_bar_box.add(self.stack_level_bar_btn_4)
    ## Scale
    self.stack_level_bar_scale = gtk.Scale.new_with_range(
      gtk.Orientation.HORIZONTAL, 0.0, 1.0, 0.1)
    self.stack_level_bar_box.add(self.stack_level_bar_scale)
    self.stack_level_bar_scale.connect(
      'change-value',
      lambda x, y, z: self.stack_level_bar.set_value(x.get_value()))

    self.stack_switcher = gtk.StackSwitcher()
    self.stack_switcher.set_stack(self.stack)

    self.vbox.add(self.stack_switcher)
    self.vbox.add(self.stack)

    gtk.MessageDialog()

  def toggle_feature(self, widget):
    print(widget.get_active())

  def munge_user_input(self, widget):
    print(widget.get_text())

  def select_fruit(self, widget):
    fruit = widget.get_active_id()
    print(fruit)
    self.header_bar.set_title(fruit)
    

if __name__ == '__main__':
  win = MainWin()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
