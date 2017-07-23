import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk


class Block(object):
  def __init__(self, x=0, y=0, w=0, h=0, type='normal'):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.type = type

  def draw(self, cr):
    if self.type == 'highlighted':
      color = (0.0, 0.3, 0.8, 0.8)
    else:
      color = (0.0, 0.5, 0.0, 0.4)

    cr.set_source_rgba(*color)
    cr.rectangle(self.x, self.y, self.w, self.h)
    cr.fill()

class Field(object):
  def __init__(self, w=10, h=10, block_w=30, block_h=30, padding=5):
    self.w = w
    self.h = h

    self.block_w=block_w
    self.block_h=block_h

    self.items = []
    self.padding = padding

    self.insert_items()

  def update(self):
    # self.items = []
    # self.insert_items()
    pass

  def insert_items(self):
    for x in range(self.w):
      for y in range(self.h):
        self.items.append(Block(
          x=x*(self.block_w+self.padding),
          y=y*(self.block_h+self.padding),
          w=self.block_w, h=self.block_h))

  def draw(self, cr):
    for item in self.items:
      item.draw(cr)

    # for x in range(self.w):
    #   for y in range(self.h):
    #     item = self.items[x*self.w+y]
    #     if item.type == 'highlighted':
    #       self.items[(x-1)*self.w+y].type = 'highlighted'
    #     item.draw(cr)

  def highlight_block(self, x, y):
    try:
      item = self.items[x*self.w+y]
      if item.type == 'normal':
        item.type = 'highlighted'
      else:
        item.type = 'normal'
    except:
      pass


class MainWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title='Blocks')

    self.field = Field(w=30, h=30, block_w=10, block_h=10)
    self.zoom_level = 1

    self.set_default_size(700, 600)

    self.scrolled_win = gtk.ScrolledWindow()
    self.add(self.scrolled_win)

    self.vbox = gtk.VBox()
    self.scrolled_win.add(self.vbox)

    self.buttons_box = gtk.HBox()
    self.buttons_box.set_border_width(10)
    self.buttons_box.set_spacing(10)
    self.vbox.pack_end(self.buttons_box, False, False, 0)

    # Buttons

    self.width_btn = gtk.SpinButton()
    self.width_btn.set_adjustment(gtk.Adjustment(5, 1, 1000, 1, 1, 1))
    self.height_btn = gtk.SpinButton()
    self.height_btn.set_adjustment(gtk.Adjustment(5, 1, 1000, 1, 1, 1))
    self.buttons_box.add(self.width_btn)
    self.buttons_box.add(self.height_btn)
    self.width_btn.connect(
      'value-changed', self.on_width_btn_value_changed)
    self.height_btn.connect(
      'value-changed', self.on_height_btn_value_changed)

    # Drawing area

    self.drawing_area_box = gtk.ScrolledWindow()
    self.drawing_area = gtk.DrawingArea()
    self.drawing_area_box.add(self.drawing_area)
    self.vbox.pack_start(self.drawing_area_box, True, True, 0)

    self.drawing_area.set_events(
      self.drawing_area.get_events() | gdk.EventMask.ALL_EVENTS_MASK)
    self.drawing_area.connect(
      'draw', self.on_drawing_area_draw)
    self.drawing_area.connect(
      'button-press-event', self.on_drawing_area_button_press_event)
    self.drawing_area.connect(
      'motion-notify-event', self.on_drawing_area_motion_notify_event)
    self.drawing_area.connect(
      'scroll-event', self.on_drawing_area_scroll_event)

  def on_drawing_area_draw(self, drawing_area, cr):
    w = drawing_area.get_allocated_width()
    h = drawing_area.get_allocated_height()

    cr.scale(self.zoom_level, self.zoom_level)

    # Background

    cr.set_source_rgb(1.0, 1.0, 1.0)
    cr.rectangle(0, 0, w, h)
    cr.fill()

    cr.set_source_rgb(1.0, 0.0, 0.0)
    cr.rectangle(20, 40, 40, 40)
    cr.fill()

    # Field

    # block_w = 10
    # block_h = 10
    # padding = 5
    # self.field.block_w = block_w
    # self.field.block_h = block_h
    # self.field.padding = padding
    # self.field.w = w/(block_w+padding)
    # self.field.h = h/(block_h+padding)

    self.field.update()
    self.field.draw(cr)

  def on_drawing_area_button_press_event(self, widget, event):
    x = event.x/self.zoom_level
    y = event.y/self.zoom_level
    xx = int(x/(self.field.block_w+self.field.padding))
    yy = int(y/(self.field.block_h+self.field.padding))
    self.field.highlight_block(xx, yy)

    w = self.drawing_area.get_allocated_width()
    h = self.drawing_area.get_allocated_height()
    self.drawing_area.queue_draw_area(0, 0, w, h)

  def on_drawing_area_motion_notify_event(self, drawing_area, event):
    # x = int(event.x)
    # y = int(event.y)
    # xx = int(x/(self.field.block_w+self.field.padding))
    # yy = int(y/(self.field.block_h+self.field.padding))
    # self.field.highlight_block(xx, yy)
    #
    # w = self.drawing_area.get_allocated_width()
    # h = self.drawing_area.get_allocated_height()
    # self.drawing_area.queue_draw_area(0, 0, w, h)
    #
    pass

  def on_drawing_area_scroll_event(self, drawing_area, event):
    direction = event.direction
    dx = event.delta_x
    dy = event.delta_y
    if direction == gdk.ScrollDirection.SMOOTH:
      if dy >= 1.0:
        self.zoom_level -= 0.1
      if dy <= -1.0:
        self.zoom_level += 0.1

    w = self.drawing_area.get_allocated_width()
    h = self.drawing_area.get_allocated_height()
    self.drawing_area.queue_draw_area(0, 0, w, h)

  def on_width_btn_value_changed(self, btn):
    value = btn.get_value_as_int()
    self.field.w = value

    w = self.drawing_area.get_allocated_width()
    h = self.drawing_area.get_allocated_height()
    self.drawing_area.queue_draw_area(0, 0, w, h)

  def on_height_btn_value_changed(self, btn):
    value = btn.get_value_as_int()
    self.field.h = value
    w = self.drawing_area.get_allocated_height()
    h = self.drawing_area.get_allocated_height()
    self.drawing_area.queue_draw_area(0, 0, w, h)



if __name__ == '__main__':
  win = MainWindow()
  win.connect('delete-event', gtk.main_quit)
  win.connect('destroy', gtk.main_quit)
  win.show_all()
  gtk.main()
