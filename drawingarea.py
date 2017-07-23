import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
import cairo

class Confetti(object):
  def __init__(self, length=5):
    self.length = length
    self.queue = []

  def push(self, item):
    self.queue.append(item)
    if len(self.queue) > self.length:
      self.pop()

  def pop(self):
      self.queue = self.queue[1:]

  def draw(self, cr):
    for i, item in enumerate(self.queue):
      item.draw(cr)

      try:
        cr.set_source_rgba(0.0, 0.0, 0.0, 1.0)
        cr.move_to(item.x, item.y)
        cr.line_to(self.queue[i+1].x, self.queue[i+1].y)
        cr.stroke()
      except:
        pass


class Rectangle(object):
  def __init__(self, x=0, y=0, width=20, height=20):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  def draw(self, cr):
    cr.set_source_rgb(1.0, 0.0, 0.0)
    cr.rectangle(
      self.x-(self.width/2), self.y-self.height/2,
      self.width, self.height)
    cr.set_font_size(9.0)
    cr.fill()

    cr.set_source_rgb(0.4, 0.0, 0.0)
    cr.move_to(self.x+20, self.y+20)
    cr.show_text('{}:{}'.format(int(self.x), int(self.y)))
    cr.fill()


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='GtkDrawingArea Demo')

    self.is_showing_red_rectangle = False
    self.mx = 0
    self.my = 0
    self.confetti = Confetti(length=5)

    self.set_default_size(500, 400)
    # self.set_position(gtk.WindowPosition.CENTER)

    self.scrolled_win = gtk.ScrolledWindow()
    self.add(self.scrolled_win)

    self.drawing_area = gtk.DrawingArea()
    self.scrolled_win.add(self.drawing_area)

    self.drawing_area.connect(
      'configure-event', self.on_drawing_area_configure_event)
    self.drawing_area.connect('draw', self.on_drawing_area_draw)
    self.drawing_area.connect(
      'button-press-event', self.on_drawing_area_button_press_event)
    self.drawing_area.set_events(
      self.drawing_area.get_events() | gdk.EventMask.BUTTON_PRESS_MASK |
      gdk.EventMask.POINTER_MOTION_MASK)

    self.surface = None

  def on_drawing_area_draw(self, drawing_area, cr):
    # cr.translate(150, 150)
    # cr.scale(2.5, 2.5)

    self.cr = cr

    w = drawing_area.get_allocated_width()
    h = drawing_area.get_allocated_height()

    # Background
    cr.set_source_rgb(1.0, 1.0, 1.0)
    cr.rectangle(0, 0, w, h)
    cr.fill()

    cr.set_source_rgb(1.0, 0, 0)
    cr.set_line_width(3.0)
    cr.rectangle(20, 40, 100, 120)
    cr.stroke()

    cr.set_source_rgb(0.0, 0.5, 1.0)
    cr.move_to(20, 30)
    cr.line_to(120, 150)
    cr.move_to(150, 120)
    cr.line_to(30, 20)
    cr.set_line_width(1.0)
    cr.stroke()

    for x in range(5):
      for y in range(5):
        cr.set_source_rgba(0.2, 0.8, 0.4, 0.6)
        cr.rectangle(x*25+20, y*25+20, 20, 20)
        cr.fill()

        cr.set_source_rgba(1.0, 1.0, 1.0, 0.8)
        cr.move_to(x*25+20, y*25+20+12)
        cr.set_font_size(12.0)
        cr.show_text('{},{}'.format(x, y))

    cr.set_source_rgb(0.3, 0.3, 0.0)
    cr.move_to(100, 100)
    cr.set_font_size(24.0)
    cr.show_text('Hello')

    if self.is_showing_red_rectangle:
      cr.set_source_rgb(1.0, 0.0, 0.0)
      cr.rectangle(self.mx, self.my, 50, 50)
      cr.fill()

    self.confetti.draw(cr)

  def on_drawing_area_button_press_event(self, widget, event):
    # try:
    #   # self.cr.set_source_surface(self.surface, 0, 0)
    #   # self.cr.set_source_rgb(1.0, 0.0, 0.0)
    #   # self.cr.rectangle(100, 100, 40, 40)
    #   # self.cr.fill()

    #   cr = cairo.Context(self.surface)
    #   cr.set_source_rgb(1.0, 0.0, 0.0)
    #   cr.rectangle(100, 100, 40, 40)
    #   cr.fill()

    #   widget.queue_draw_area(0, 0, 300, 300)
    # except:
    #   pass

    width = widget.get_allocated_width()
    height = widget.get_allocated_height()
    self.drawing_area.queue_draw_area(0, 0, width, height)
    # self.is_showing_red_rectangle = not self.is_showing_red_rectangle
    # self.mx = event.x
    # self.my = event.y

    self.confetti.push(Rectangle(x=event.x, y=event.y))

  def on_drawing_area_configure_event(self, widget, event):
    # window = widget.get_window()
    # width = widget.get_allocated_width()
    # height = widget.get_allocated_height()
    # self.surface = window.create_similar_surface(
    #   cairo.CONTENT_COLOR, width, height)
    pass


if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.connect('destroy', gtk.main_quit)
  win.show_all()
  gtk.main()
