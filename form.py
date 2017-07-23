import random

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class ListBoxRowWithData(gtk.ListBoxRow):
  def __init__(self, child, data):
    gtk.ListBoxRow.__init__(self)
    self.data = data
    self.add(child)

class CustomerEditDialog(gtk.Dialog):
  def __init__(self, parent, data):
    gtk.Dialog.__init__(self)

    self.set_transient_for(parent)

    self.set_default_size(500, 300)

    self.data = data

    self.box = self.get_content_area()
    self.box.set_border_width(10)

    self.action_box = self.get_action_area()
    self.action_box.set_border_width(10)

    self.vvbox = gtk.VBox()
    self.vvbox.set_spacing(10)
    self.box.add(self.vvbox)

    # First Name
    self.first_name_entry = gtk.Entry()
    self.first_name_entry.connect('activate', self.on_save)
    self.first_name_entry.set_text(self.data['first_name'])
    self.vvbox.add(gtk.Label('Fist Name', xalign=0))
    self.vvbox.add(self.first_name_entry)
    # Last Name
    self.last_name_entry = gtk.Entry()
    self.last_name_entry.connect('activate', self.on_save)
    self.last_name_entry.set_text(self.data['last_name'])
    self.vvbox.add(gtk.Label('Last Name', xalign=0))
    self.vvbox.add(self.last_name_entry)
    # Phone number
    self.phone_entry = gtk.Entry()
    self.phone_entry.connect('activate', self.on_save)
    self.phone_entry.set_text(str(self.data['phone']))
    self.vvbox.add(gtk.Label('Phone', xalign=0))
    self.vvbox.add(self.phone_entry)

    self.button_box = gtk.HBox()
    self.button_box.set_spacing(10)
    self.vvbox.add(self.button_box)
    # `Save' Buttons
    self.cancel_button = gtk.Button.new_with_mnemonic('_Cancel')
    self.cancel_button.connect('clicked', self.on_cancel)
    self.button_box.add(self.cancel_button)
    # `Cancel' Button
    self.save_button = gtk.Button.new_with_mnemonic('_Save')
    self.save_button.connect('clicked', self.on_save)
    self.button_box.add(self.save_button)

    self.show_all()

  def on_cancel(self, widget):
    self.response(gtk.ResponseType.CANCEL)
    self.destroy()

  def on_save(self, widget):
    self.response(gtk.ResponseType.APPLY)
    self.data['first_name'] = self.first_name_entry.get_text()
    self.data['last_name'] = self.last_name_entry.get_text()
    self.data['phone'] = int(self.phone_entry.get_text())
    self.destroy()

class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='Form App')

    self.first_name = 'John'
    self.last_name = 'Doe'
    self.selected_contacts_row_idx = None

    # Contacts
    self.contacts = []
    for i in range(20):
      id = i
      first_name = 'Firstname{}'.format(i)
      last_name = 'Lastname{}'.format(i)
      phone = random.randrange(132832, 947372)
      self.contacts.append({'id': id, 'first_name': first_name,
                            'last_name': last_name, 'phone': phone})

    self.set_default_size(700, 600)

    self.header_bar = gtk.HeaderBar(title='Form App')
    self.header_bar.set_show_close_button(True)
    self.set_titlebar(self.header_bar)

    # Notebook

    self.notebook = gtk.Notebook()
    self.add(self.notebook)
    self.notebook.set_scrollable(True)
    # Create notebook pages
    self.create_notebook_page_personal_data()
    self.create_notebook_page_info()
    self.create_notebook_page_website()
    self.create_notebook_page_employees()
    self.create_notebook_page_contacts()

    # Notebook settings
    #
    # self.notebook.set_tab_pos(gtk.PositionType.LEFT)
    # self.notebook.set_tab_detachable(self.page_website, True)
    # self.notebook.set_tab_reorderable(self.info_page, True)

  def create_notebook_page_personal_data(self):
    self.scrolled_win = gtk.ScrolledWindow()
    self.scrolled_win.set_border_width(20)
    self.notebook.append_page(
      self.scrolled_win, gtk.Label.new_with_mnemonic('_Personal Data'))

    self.grid = gtk.Grid()
    self.grid.set_row_spacing(30)
    self.grid.set_column_spacing(20)
    self.scrolled_win.add(self.grid)

    # First name
    self.first_name_label = gtk.Label()
    self.grid.attach(self.first_name_label, 0, 0, 3, 3)
    self.first_name_label.set_halign(gtk.Align.START)
    self.first_name_label.set_markup('<b>{}</b>'.format('First Name'))
    self.first_name_entry = gtk.Entry()
    self.first_name_entry.set_width_chars(40)
    self.grid.attach(self.first_name_entry, 0, 1, 3, 3)

    # Last name
    self.last_name_label = gtk.Label()
    self.grid.attach(self.last_name_label, 0, 2, 3, 3)
    self.last_name_label.set_halign(gtk.Align.START)
    self.last_name_label.set_markup('<b>{}</b>'.format('Last Name'))
    self.last_name_entry = gtk.Entry()
    self.last_name_entry.set_width_chars(40)
    self.grid.attach(self.last_name_entry, 0, 3, 3, 3)

    # "Set data" button
    self.set_personal_data_btn = gtk.Button('Set data')
    self.grid.attach(self.set_personal_data_btn, 0, 15, 1, 1)
    self.set_personal_data_btn.connect('clicked', self.set_personal_data)

  def create_notebook_page_info(self):
    self.info_page = gtk.ScrolledWindow()
    self.info_page.set_border_width(20)
    # self.info_page.add(gtk.Label('This is some info. More to come.')

    self.info_page_grid = gtk.Grid()
    self.info_page.add(self.info_page_grid)
    self.info_page_grid.set_row_spacing(40)
    self.info_page_grid.set_column_spacing(20)

    # First Name Info
    self.info_page_first_name_text_label = gtk.Label('First Name:')
    self.info_page_grid.attach(self.info_page_first_name_text_label,
                               0, 0, 2, 1)
    self.info_page_first_name_text = gtk.Label(self.first_name)
    self.info_page_first_name_text.set_selectable(True)
    self.info_page_first_name_text.select_region(0, 0)
    self.info_page_grid.attach(self.info_page_first_name_text,
                               3, 0, 4, 1)

    # Last Name Info
    self.info_page_last_name_text_label = gtk.Label('Last Name:')
    self.info_page_grid.attach(self.info_page_last_name_text_label,
                               0, 1, 2, 1)
    self.info_page_last_name_text = gtk.Label(self.last_name)
    self.info_page_last_name_text.set_selectable(True)
    self.info_page_last_name_text.select_region(0, 0)
    self.info_page_grid.attach(self.info_page_last_name_text,
                               3, 1, 4, 1)

    self.notebook.append_page(
      self.info_page, gtk.Label.new_with_mnemonic('_Info'))

  def create_notebook_page_website(self):
    #   GtkScrolledWindow -> GtkGrid -> GtkVBox -> <content>

    self.page_website = gtk.ScrolledWindow()
    self.page_website.set_border_width(20)

    self.page_website_grid = gtk.Grid()
    self.notebook.append_page(
      self.page_website, gtk.Label.new_with_mnemonic('_Website'))
    self.page_website.add(self.page_website_grid)

    self.page_website_vbox = gtk.VBox()
    self.page_website_vbox.set_spacing(10)
    self.page_website_grid.attach(self.page_website_vbox, 0, 0, 8, 8)

    self.website_data = {
      'name': '', 'url': '', 'description': '', 'company': ''
    }
    self.website_data_entries = {}

    for data_point in sorted(self.website_data.keys()):
      label = gtk.Label(data_point.capitalize())
      label.set_halign(gtk.Align.START)
      self.page_website_vbox.add(label)

      variable = self.website_data[data_point]
      entry = gtk.Entry()
      entry.set_width_chars(40)
      entry.connect('activate', self.set_website_data)
      self.page_website_vbox.add(entry)
      self.website_data_entries[data_point] = entry

    self.page_website_vbox.add(gtk.Label(''))
    button = gtk.Button('Set data')
    self.page_website_vbox.add(button)
    button.connect('clicked', self.set_website_data)

    self.website_data_label_box = gtk.VBox()
    self.website_data_label_box.set_border_width(40)
    self.website_data_label_box.set_spacing(10)
    self.website_data_label = gtk.Label('Website Data')
    self.page_website_grid.attach(
      self.website_data_label_box, 11, 0, 4, 1)
    self.website_data_label_box.add(self.website_data_label)

    self.website_data_label_box.add(gtk.HSeparator())

    self.do_show_website_data_dialog = False
    self.show_website_data_dialog_toggle = gtk.CheckButton('Show dialog')
    self.website_data_label_box.add(self.show_website_data_dialog_toggle)
    self.show_website_data_dialog_toggle.connect(
      'clicked', self.toggle_show_website_data_dialog) 
    self.show_website_data_dialog_toggle.set_active(
      not self.do_show_website_data_dialog)

  def create_notebook_page_employees(self):
    # GtkScrolledWindow -> GtkGrid -> GtkVBox

    self.page_employees = gtk.ScrolledWindow()
    self.notebook.append_page(
      self.page_employees, gtk.Label.new_with_mnemonic('_Employees'))

    self.page_employees_grid = gtk.Grid()
    self.page_employees.add(self.page_employees_grid)

    self.page_employees_vbox = gtk.VBox()
    self.page_employees_grid.attach(self.page_employees_vbox, 0, 0, 1, 8)

    self.employees_list_store = gtk.ListStore(str, str, int)
    for i in range(200):
      self.employees_list_store.append(
        ['John{}'.format(i), 'Doe{}'.format(i),
         random.randrange(23, 64)])

    self.page_employees_tree_view = gtk.TreeView(
      model=self.employees_list_store)
    self.page_employees_vbox.add(self.page_employees_tree_view)

    # First name & last name fields
    for i, title in enumerate(['First Name', 'Last Name', 'Age']):
      renderer = gtk.CellRendererText()
      renderer.set_property('editable', True)
      renderer.column = i
      renderer.connect('edited', self.on_edited_employee_field)
      col = gtk.TreeViewColumn(title, renderer, text=i)
      self.page_employees_tree_view.append_column(col)

  def create_notebook_page_contacts(self):
    self.page_contacts = gtk.ScrolledWindow()
    self.notebook.append_page(
      self.page_contacts, gtk.Label.new_with_mnemonic('C_ontacts'))

    self.page_contacts_vbox = gtk.VBox()
    self.page_contacts.add(self.page_contacts_vbox)
    self.page_contacts_vbox.set_border_width(20)

    self.page_contacts_lbox = gtk.ListBox()
    self.page_contacts_lbox.connect(
      'row-selected', self.on_contacts_row_selected)
    self.page_contacts_vbox.add(self.page_contacts_lbox)
    self.page_contacts_lbox.connect(
      'row-activated', self.on_page_contacts_lbox_row_activated)

    self.insert_contacts_lbox_rows()

  def on_contacts_row_selected(self, widget, row):
    try:
      self.selected_contacts_row_idx = row.data['index']
    except:
      pass

  def insert_contacts_lbox_rows(self):
    for i, contact in enumerate(self.contacts):
      id = contact['id']
      first_name = contact['first_name']
      last_name = contact['last_name']
      phone = contact['phone']

      label_first_name = gtk.Label(first_name, xalign=0)
      label_last_name = gtk.Label(last_name, xalign=0)
      label_phone = gtk.Label(phone, xalign=0)
      button = gtk.Button('Info')
      button.set_tooltip_text('Show info for this contact')
      button.set_margin_end(20)

      hbox = gtk.HBox()
      hbox.set_homogeneous(True)
      hbox.set_border_width(5)
      hbox.add(label_first_name)
      hbox.add(label_last_name)
      hbox.add(label_phone)
      hbox.pack_start(button, False, False, 0)
      data = {'index': i, 'id': id, 'first_name': first_name,
              'last_name': last_name, 'phone': phone}
      self.page_contacts_lbox.add(ListBoxRowWithData(hbox, data))

  def set_personal_data(self, widget):
    self.first_name = self.first_name_entry.get_text()
    self.last_name = self.last_name_entry.get_text()

    self.info_page_first_name_text.set_text(self.first_name)
    self.info_page_last_name_text.set_text(self.last_name)

    self.notebook.next_page()

  def set_website_data(self, widget):
    s = '<big>Website Data</big>\n\n'
    for data_point in sorted(self.website_data.keys()):
      data = self.website_data_entries[data_point].get_text()
      s += '{}: <b>{}</b>\n'.format(data_point.capitalize(), data)
    self.website_data_label.set_markup(s)

    if self.do_show_website_data_dialog:
      dialog = gtk.MessageDialog(
        self, gtk.DialogFlags.MODAL, gtk.MessageType.INFO,
        gtk.ButtonsType.OK)
      dialog.set_markup(s)
      dialog.run()
      dialog.destroy()

  def toggle_show_website_data_dialog(self, widget):
    t = self.do_show_website_data_dialog
    self.do_show_website_data_dialog = not t

  def rebuild_contacts_lbox(self):
    children = self.page_contacts_lbox.get_children()
    for child in children:
      child.destroy()
    self.insert_contacts_lbox_rows()
    self.page_contacts_lbox.show_all()
    self.page_contacts_lbox.select_row(
      self.page_contacts_lbox.get_row_at_index(
        self.selected_contacts_row_idx))

  def on_edited_employee_field(self, widget, path, new_text):
    col = widget.column
    if col == 2:
      new_text = int(new_text) 
    self.employees_list_store[path][col] = new_text

  def on_edited_employee_age(self, widget, path, new_value):
    self.employees_list_store[path][widget.column] = new_value

  def on_page_contacts_lbox_row_activated(self, widget, row):
    dialog = CustomerEditDialog(self, row.data)
    response = dialog.run()
    dialog.destroy()

    if response == gtk.ResponseType.APPLY:
      print(dialog.data)
      print('Save')
      for i, contact in enumerate(self.contacts):
        if contact['id'] == dialog.data['id']:
          self.contacts[i] = dialog.data
      self.rebuild_contacts_lbox()

if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
