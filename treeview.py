import csv
import random

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Pango as pango


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='GtkTreeView Demo')

    self.set_default_size(500, 400)

    # Data

    self.data = []
    self.data_limit = 20
    self.data_offset = 0
    self.tree_view_titles = [
      'Title',
      'URL',
      'Length',
      'Viewed',
      'Bookmark',
      'Tags',
      'Added'
    ]

    # Layout boxes

    self.vbox = gtk.VBox()
    self.scrolled_win = gtk.ScrolledWindow()
    self.vbox.pack_end(self.scrolled_win, True, True, 0)
    self.add(self.vbox)

    # Next/previous page controls

    self.tree_view_nav_box = gtk.HBox()
    self.vbox.pack_start(self.tree_view_nav_box, False, False, 0)
    self.tree_view_nav_box.set_border_width(10)

    self.tree_view_nav_box.pack_start(
      gtk.Label('Page: '), False, False, 0)

    self.tree_view_nav_spin_btn = gtk.SpinButton()
    self.tree_view_nav_box.pack_start(
      self.tree_view_nav_spin_btn, False, False, 0)
    self.tree_view_nav_spin_btn.set_adjustment(
      gtk.Adjustment(
        self.data_offset + 1.0, 1.0, 99999.0, 1.0, 1.0, 1.0))
    self.tree_view_nav_spin_btn.connect(
      'value-changed', self.on_tree_view_nav_spin_btn_value_changed)

    # GtkTreeView

    self.list_store = gtk.ListStore(int, str, str, str, bool, str, str, int)

    csv_reader = csv.reader(
      open('data.csv', 'r'), delimiter=',', quotechar='"')
    for i,row in enumerate(csv_reader):
      if i > 0:
        self.data.append([i] + row)
    for i, row in enumerate(self.data[self.data_offset:self.data_limit]):
      if i > 0:
        if row[4] == '0':
          viewed = False
        else:
          viewed = True
        self.list_store.append([
          row[0],
          row[1],
          row[2],
          row[3],
          viewed,
          row[5],
          row[6],
          int(row[7])
        ])

    self.tree_view = gtk.TreeView()
    self.tree_view.set_model(self.list_store)

    for i, title in enumerate(self.tree_view_titles):
      if i == 3:
        renderer = gtk.CellRendererToggle()
        # renderer.connect('toggled', self.on_toggle_renderer_toggled)
      else:
        renderer = gtk.CellRendererText()
        renderer.set_property('ellipsize', pango.EllipsizeMode.END)
      if (i == 0):
        renderer.set_property('width-chars', 60)
      column = gtk.TreeViewColumn(title, renderer, text=i+1)
      column.set_resizable(True)
      column.set_min_width(80)
      column.set_reorderable(True)
      column.set_sort_column_id(i+1)
      column.set_clickable(True)
      if i == 3:
        column.add_attribute(renderer, 'active', 4)
      self.tree_view.append_column(column)

    self.tree_view.connect(
      'row-activated', self.on_tree_view_row_activated)

    self.scrolled_win.add(self.tree_view)

  # def on_toggle_renderer_toggled(self, widget, path):
  #   self.list_store[path][3] = not self.list_store[path][3]

  def on_tree_view_nav_spin_btn_value_changed(self, widget):
    offset = int(widget.get_value())
    offset -= 1
    lower = offset * self.data_limit
    upper = (offset + 1) * self.data_limit
    if upper > len(self.data):
      upper = len(self.data)
    if lower < len(self.data):
      self.data_offset = offset
      self.list_store.clear()
      for row in self.data[lower:upper]:
        if row[4] == '0':
          viewed = False
        else:
          viewed = True
        self.list_store.append([
          row[0],
          row[1],
          row[2],
          row[3],
          viewed,
          row[5],
          row[6],
          int(row[7])
        ])
    else:
      widget.set_value(offset)

  def on_tree_view_row_activated(self, widget, path, column):
    print(self.list_store[path][:])


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
