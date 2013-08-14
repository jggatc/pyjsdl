#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
from surface import Surface
from time import Time
import env
import pyjsdl.event
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.FocusPanel import FocusPanel
try:    ###0.15
    from pyjamas.Canvas.HTML5Canvas import HTML5Canvas      ###>IE9
except ImportError:
    from pyjamas.Canvas.GWTCanvas import GWTCanvas as HTML5Canvas
from pyjamas.Canvas import Color
from pyjamas.Canvas.ImageLoader import loadImages
from pyjamas.ui import Event
from pyjamas import DOM
import locals as Const

__docformat__ = 'restructuredtext'


class Canvas(HTML5Canvas):    ###0.15

    def __init__(self, size):
        HTML5Canvas.__init__(self, size[0], size[1])      ###0.15
        self.width = size[0]
        self.height = size[1]
        self.surface = Surface(size)
        self.resize(self.width, self.height)
        self.images = {}
        self.image_list = None
        self.loop = None
        self.run = self._run
        self.time_hold = 1
        self.time_wait = 0
        self.time = Time()
        self.event = pyjsdl.event
        self.addMouseListener(self)
        self.addKeyboardListener(self)
        self.sinkEvents(Event.ONMOUSEDOWN | Event.ONMOUSEUP| Event.ONMOUSEMOVE | Event.ONMOUSEOUT | Event.ONKEYDOWN | Event.ONKEYPRESS | Event.ONKEYUP)
        self.modKey = pyjsdl.event.modKey
        self.specialKey = pyjsdl.event.specialKey

    def onMouseMove(self, sender, x, y):
        event = DOM.eventGetCurrentEvent()
        event.pos = (x, y)
        self.event.mouseMove['x'], self.event.mouseMove['y'] = x, y
        self.event._updateQueue(event)
      	
    def onMouseDown(self, sender, x, y):
        event = DOM.eventGetCurrentEvent()
        event.pos = (x, y)
        self.event.mousePress[event.button] = True
        self.event._updateQueue(event)
      	
    def onMouseUp(self, sender, x, y):
        event = DOM.eventGetCurrentEvent()
        event.pos = (x, y)
        self.event.mousePress[event.button] = False
        self.event._updateQueue(event)

    def onMouseLeave(self, sender):
        self.event.mousePress[0], self.event.mousePress[1], self.event.mousePress[2] = False, False, False
        self.event.mouseMove['x'], self.event.mouseMove['y'] = -1, -1
        self.event.mouseMoveRel['x'], self.event.mouseMoveRel['y'] = None, None
        self.event.keyPress['a'], self.event.keyPress['c'], self.event.keyPress['s'] = False, False, False

    def onKeyDown(self, sender, keycode, modifiers):
        if keycode in self.modKey:
            event = DOM.eventGetCurrentEvent()
            self.event.keyPress[keycode] = True
            self.event._updateQueue(event)
            DOM.eventPreventDefault(event)
        elif keycode in self.specialKey:
            event = DOM.eventGetCurrentEvent()
            self.event._updateQueue(event)
            DOM.eventPreventDefault(event)

    def onKeyPress(self, sender, keycode, modifiers):
        event = DOM.eventGetCurrentEvent()
        if not (event.keyCode and event.keyCode in self.specialKey):
            self.event._updateQueue(event)
        DOM.eventPreventDefault(event)

    def onKeyUp(self, sender, keycode, modifiers):
        event = DOM.eventGetCurrentEvent()
        if keycode in self.modKey:
            self.event.keyPress[keycode] = False
        self.event._updateQueue(event)

    def set_loop(self, loop):
        self.loop = loop

    def load_images(self, images):
        if images:
            self.image_list = images
            loadImages(images, self)
        else:
            self.start()

    def set_timeout(self, change):
        self.time_hold += change
        if self.time_hold < 1:
            self.time_hold = 1

    def start(self):
        self.time.timeout(self.time_hold, self)

    def onImagesLoaded(self, images):
        for i, image in enumerate(self.image_list):
            self.images[image] = images[i]
        self.start()

    def set_timeWait(self, time):
        if time:
            self.time_wait = time
            self.run = lambda: None
        else:
            self.time_wait = 0
            self.run = self._run
            self.run()

    def _run(self):
        self.loop()
        self.time.timeout(self.time_hold, self)


class Display(object):
    """
    **pyjsdl.display**

    * pyjsdl.display.init
    * pyjsdl.display.set_mode
    * pyjsdl.display.get_surface
    * pyjsdl.display.get_canvas
    * pyjsdl.display.get_panel
    * pyjsdl.display.quit
    * pyjsdl.display.get_init
    * pyjsdl.display.set_caption
    * pyjsdl.display.clear
    * pyjsdl.display.flip
    * pyjsdl.display.update
    """

    def __init__(self):
        """
        Initialize Display module.

        Module initialization creates pyjsdl.display instance.        
        """
        self._initialized = False
        self.init()

    def init(self):
        """
        Initialize display.
        """
        if not self._initialized:
            self.caption = ''
            self.icon = None
            self._nonimplemented_methods()
            self._initialized = True

    def set_mode(self, size):
        """
        Return a display Surface.
        Argument: size (x,y) of surface.
        """
        self.canvas = Canvas(size)
        env.canvas = self.canvas
        panel = FocusPanel(Widget=self.canvas)
        RootPanel().add(panel)
        self.panel = panel
        self.surface = self.canvas.surface
        self.surface._display = self
        return self.surface

    def setup(self, loop, images=None):
        """
        Initialize Canvas for script execution.
        Argument include loop function to run and optional images list to preload.
        """
        self.canvas.set_loop(loop)
        self.canvas.load_images(images)

    def get_surface(self):
        """
        Return display Surface.
        """
        return self.surface

    def get_canvas(self):
        """
        Return Canvas.
        """
        return self.canvas

    def get_panel(self):
        """
        Return Panel.
        """
        return self.panel

    def quit(self):
        """
        Uninitialize display.
        """
        self._initialized = False
        return None

    def get_init(self):
        """
        Check that display module is initialized.
        """
        return self._initialized

    def set_caption(self, caption):
        """
        Set Display.caption.
        Argument: caption text.
        """
        self.caption = caption
        return None

    def clear(self):
        """
        Clear display surface.
        """
        self.surface.beginPath()
        self.surface.setFillStyle(Color.Color(0,0,0))   ###0.15
        self.surface.fillRect(0, 0, self.surface.width, self.surface.height)

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.set_icon = lambda *arg: None

    def flip(self):
        """
        Repaint display.
        """
        self.canvas.drawImage(self.canvas.surface.canvas, 0, 0)   ###pyjs0.8 problem
#        self.canvas.drawImage(self.canvas.surface, 0, 0)

    def update_rect(self, rect_list):       ###0.16
        """
        Repaint display.
        Argument rect_list specifies a list of Rect to repaint.
        """
        for rect in rect_list:
            self.canvas.drawImage(self.canvas.surface.canvas, rect.x,rect.y,rect.width,rect.height, rect.x,rect.y,rect.width,rect.height)
        return None

    def update(self, rect_list=None):
        """
        Repaint display.
        An optional rect_list to specify regions to repaint.
        """
        if not isinstance(rect_list, list):     ###0.16
            if not rect_list:
                self.canvas.drawImage(self.canvas.surface.canvas, 0, 0)
#                self.canvas.drawImage(self.canvas.surface, 0, 0) ##pyjs0.8 *.canvas
                return None
            else:
                rect_list = [rect_list]
        for rect in rect_list:
            try:
                x, y, w, h = rect[0], rect[1], rect[2], rect[3]
                #pyjs -O no attribute checking of Rect obj
                self.canvas.drawImage(self.canvas.surface.canvas, x,y,w,h, x,y,w,h)
#                self.canvas.drawImage(self.canvas.surface, x,y,w,h, x,y,w,h) ###pyjs0.8 *.canvas
            except (TypeError, AttributeError): ###pyjs -O TypeError -S AttributeError
                continue    #rect is None
        return None

