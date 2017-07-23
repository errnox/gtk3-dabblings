import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='Assistant Demo')

    self.set_default_size(400, 300)

    self.scrolled_win = gtk.ScrolledWindow()
    self.add(self.scrolled_win)

    self.vbox = gtk.VBox()
    self.scrolled_win.add(self.vbox)

    self.show_assistant_btn = gtk.Button.new_with_mnemonic(
      '_Show assistant')
    self.vbox.pack_start(self.show_assistant_btn, False, False, 0)
    self.show_assistant_btn.connect(
      'clicked', self.on_show_assistant_btn_clicked)

    self.gather_data()

  def gather_data(self):
    self.input_text = ''
    self.chunks = []
    with open('./assistant.py', 'r') as file:
      for line in file:
        self.input_text += line

    for line in self.input_text.split('\n\n'):
      self.chunks.append(line)

  def on_show_assistant_btn_clicked(self, widget):
    self.assistant = gtk.Assistant()
    self.assistant.connect('cancel', self.on_assistant_cancel)
    self.assistant.connect('close', self.on_assistant_close)

    intro_box = gtk.ScrolledWindow()
    self.assistant.append_page(intro_box)
    self.assistant.set_page_type(intro_box, gtk.AssistantPageType.INTRO)
    intro_label = gtk.Label('This is an assistant.')
    intro_label.set_line_wrap(True)
    intro_box.add(intro_label)
    self.assistant.set_page_title(intro_box, 'Intro')
    self.assistant.set_page_complete(intro_box, True)

    # for i, chunk in enumerate(self.chunks):
    #   box = gtk.ScrolledWindow()
    #   label = gtk.Label(chunk)
    #   label.set_line_wrap(True)
    #   box.add(label)

    #   self.assistant.append_page(box)
    #   self.assistant.set_page_type(box, gtk.AssistantPageType.CONTENT)
    #   self.assistant.set_page_title(box, 'Page {}'.format(i))
    #   self.assistant.set_page_complete(box, True)

    content_box = gtk.ScrolledWindow()
    self.assistant.append_page(content_box)
    self.assistant.set_page_type(
      content_box, gtk.AssistantPageType.CONTENT)
    content_label = gtk.Label('This is a content page.')
    content_label.set_line_wrap(True)
    content_box.add(content_label)
    self.assistant.set_page_title(content_box, 'Content')
    self.assistant.set_page_complete(content_box, True)

    summary_box = gtk.ScrolledWindow()
    self.assistant.append_page(summary_box)
    self.assistant.set_page_type(
      summary_box, gtk.AssistantPageType.SUMMARY)
    summary_label = gtk.Label('This was an assistant in action.')
    summary_label.set_line_wrap(True)
    summary_box.add(summary_label)
    self.assistant.set_page_title(summary_box, 'Summary')
    self.assistant.set_page_complete(summary_box, True)

    self.assistant.show_all()

  def on_assistant_cancel(self, widget):
    self.assistant.destroy()

  def on_assistant_close(self, widget):
    self.assistant.destroy()


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.show_all()
  gtk.main()
