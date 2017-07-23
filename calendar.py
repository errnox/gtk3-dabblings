import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
# from gi.repository import Gio as gio
# from gi.repository import Gdk as gdk


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title="Calendar")

    self.year = 2016

    self.set_default_size(800, 700)

    self.paned = gtk.Paned()
    self.add(self.paned)
    self.paned.set_position(8000)

    # Edit pane

    self.is_edit_pane_visible = False

    self.edit_pane = gtk.ScrolledWindow()
    self.edit_box = gtk.VBox()
    self.edit_pane.add(self.edit_box)
    self.paned.pack2(self.edit_pane)

    self.edit_label = gtk.Label('This is the edit pane.')
    self.edit_box.add(self.edit_label)

    # Calendar pane

    self.scrolled_win = gtk.ScrolledWindow()
    self.paned.pack1(self.scrolled_win, True, True)

    self.vbox = gtk.VBox()
    self.scrolled_win.add(self.vbox)

    self.flowbox = gtk.FlowBox()
    self.vbox.add(self.flowbox)
    self.flowbox.set_selection_mode(gtk.SelectionMode.NONE)
    self.flowbox.set_max_children_per_line(3)

    self.calendars = []

    for i in range(12):
      calendar = gtk.Calendar()
      calendar.set_property('no-month-change', True)
      calendar.select_month(i, self.year)
      calendar.select_day(0)
      calendar.connect('focus-in-event', self.on_calendar_focus_in_event)
      calendar.connect('day-selected', self.on_calendar_day_selected)
      calendar.connect(
        'day-selected-double-click',
        self.on_calendar_day_selected_double_click)
      calendar.mark_day(13)
      self.flowbox.add(calendar)
      self.calendars.append(calendar)

    # Popover

    self.calendar_popover = gtk.Popover()
    self.calendar_popover.set_modal(False)

    self.calendar_popover_box = gtk.VBox()
    self.calendar_popover.add(self.calendar_popover_box)
    self.calendar_popover_box.set_border_width(5)
    self.calendar_popover_box.set_spacing(5)

    self.popover_hide_btn = gtk.Button.new_with_mnemonic("_Hide")
    self.popover_hide_btn.set_property('relief', gtk.ReliefStyle.NONE)
    self.popover_hide_btn.connect(
      'clicked', self.on_popover_hide_btn_clicked)
    self.calendar_popover_box.add(self.popover_hide_btn)

    self.popover_label = gtk.Label('This is a popover.')
    self.calendar_popover_box.add(self.popover_label)

#   # Theme
#
#     self.info_btn = gtk.Button('Information')
#     self.vbox.pack_start(self.info_btn, False, False, 0)
#     self.info_btn.set_name('infobutton')
#     self.calendars[0].set_name('infobutton')
#
#     self.css_provider = gtk.CssProvider()
#     # self.css_provider.load_from_file(
#     #   gio.File.new_for_path('./calendar.css'))
#     print(self.css_provider.to_string())
#     self.css = """
# #infobutton {
#   background-color: #FF0000;
#   color: #333333;
#   border: 3px solid #FF0000;
#   box-shadow: 0 0 0 #FFFFFF inset;
#   border-radius: 10px;
# }
# """
#     self.css_provider.load_from_data(self.css)
#
#     gtk.StyleContext.add_provider_for_screen(
#       gdk.Screen.get_default(), self.css_provider,
#       gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

  def on_calendar_focus_in_event(self, widget, event):
    for calendar in self.calendars:
      if calendar != widget:
        try:
          calendar.select_day(0)
        except:
          pass

  def on_calendar_day_selected(self, widget):
    for calendar in self.calendars:
      if calendar != widget:
        try:
          date = widget.get_date()
          print(date)
          self.popover_label.set_text(
            '{}/{}/{}'.format(date[0], date[1], date[2]))
          self.calendar_popover.set_relative_to(widget)
          self.calendar_popover.show_all()

          self.edit_label.set_text(
            '{}/{}/{}'.format(date[0], date[1], date[2]))
          break
        except:
          pass

  def on_calendar_day_selected_double_click(self, widget):
    if not self.is_edit_pane_visible:
      self.is_edit_pane_visible = True
      self.paned.set_position(250)

  def on_popover_hide_btn_clicked(self, widget):
    self.calendar_popover.hide()


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
