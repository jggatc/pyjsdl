#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
from surface import Surface
from rect import Rect
from time import Time
import env
import pyjsdl.event
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.FocusPanel import FocusPanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.Canvas import Color
from pyjamas.Canvas.ImageLoader import loadImages
from pyjamas import Window
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui import Event
from pyjamas import DOM
import locals as Const

__docformat__ = 'restructuredtext'


class Canvas(Surface):

    def __init__(self, size, buffered):
        Surface.__init__(self, size)
        Surface.resize(self, size[0], size[1])
        if isinstance(buffered, bool):
            self._bufferedimage = buffered
        else:
            self._bufferedimage = True
        try:
            if self.impl.canvasContext:
                self._isCanvas = True
        except:
            self._isCanvas = False
            self._bufferedimage = False
        if self._bufferedimage:
            self.surface = Surface(size)
        else:
            self.surface = self
        self.images = {}
        self.image_list = None
        self.loop = None
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
        for keycode in self.modKey:
            if self.event.keyPress[keycode]:
                self.event.keyPress[keycode] = False

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

    def resize(self, width, height):
        Surface.resize(self, width, height)
        self.surface.resize(width, height)
        try:
            self.surface._display.textbox.resize()
        except (TypeError, AttributeError):     #pyjs-O:TypeError/-S:AttributeError
            pass
        try:
            self.surface._display.textarea.resize()
        except (TypeError, AttributeError):     #pyjs-O:TypeError/-S:AttributeError
            pass

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
        self.run = self._run
        self.time.timeout(self.time_hold, self)

    def stop(self):
        self.time_wait = 0
        self.run = lambda: None

    def onImagesLoaded(self, images):
        for i, image in enumerate(self.image_list):
            self.images[image] = images[i]
        self.start()

    def set_timeWait(self, time):
        if time:
            self.time_wait = time
            self.run = lambda: None
        else:
            if self.time_wait:
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
    * pyjsdl.display.setup
    * pyjsdl.display.textbox_init
    * pyjsdl.display.is_canvas
    * pyjsdl.display.get_surface
    * pyjsdl.display.get_canvas
    * pyjsdl.display.get_panel
    * pyjsdl.display.get_vpanel
    * pyjsdl.display.quit
    * pyjsdl.display.get_init
    * pyjsdl.display.get_active
    * pyjsdl.display.set_caption
    * pyjsdl.display.get_caption
    * pyjsdl.display.clear
    * pyjsdl.display.flip
    * pyjsdl.display.update_rect
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
            self.id = ''
            self.icon = None
            self._nonimplemented_methods()
            self._initialized = True

    def set_mode(self, size, buffered=True, *args, **kwargs):
        """
        Setup the display Surface.
        Argument include size (x,y) of surface and optional buffered surface.
        Return a reference to the display Surface.
        """
        self.canvas = Canvas(size, buffered)
        env.canvas = self.canvas
        env.frame = Window.getDocumentRoot()
        panel = FocusPanel(Widget=self.canvas)
        RootPanel().add(panel)
        self.panel = panel
        self.vpanel = None
        self.textbox = None
        self.textarea = None
        self.Textbox = Textbox
        self.Textarea = Textarea
        self.surface = self.canvas.surface
        self.surface._display = self
        if not self.canvas._bufferedimage:
            self.flip = lambda: None
            self.update = lambda *arg: None
            self.update_rect = lambda *arg: None
        return self.surface

    def setup(self, loop, images=None):
        """
        Initialize Canvas for script execution.
        Argument include loop function to run and optional images list to preload.
        """
        self.canvas.set_loop(loop)
        self.canvas.load_images(images)

    def textbox_init(self):
        """
        Initiate textbox functionality and creates instances of pyjsdl.display.textbox and pyjsdl.display.textarea that are subclasses of Pyjs TextBox/TextArea, placed in lower VerticalPanel.
        """
        if not self.textbox:
            self.textbox = Textbox()
            self.textarea = Textarea()

    def is_canvas(self):
        """
        Check whether browser has HTML5 Canvas.
        """
        return self.canvas._isCanvas

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

    def get_vpanel(self):
        """
        Return VerticalPanel positioned under Panel holding Canvas.
        """
        if not self.vpanel:
            self.vpanel = VerticalPanel()
            RootPanel().add(self.vpanel)
        return self.vpanel

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

    def get_active(self):
        """
        Check if display is visible.
        """
        if hasattr(self, 'canvas'):
            return True
        else:
            return False

    def set_caption(self, text):
        """
        Set Canvas element id.
        Argument is the id text.
        """
        self.id = text
        try:
            self.canvas.setID(self.id)
        except (TypeError, AttributeError):
            pass
        return None

    def get_caption(self):
        """
        Get Canvas element id.
        """
        try:
            return self.canvas.getID()
        except (TypeError, AttributeError):
            return self.id

    def clear(self):
        """
        Clear display surface.
        """
        self.surface.beginPath()
        self.surface.setFillStyle(Color.Color(0,0,0))
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
        self.canvas.drawImage(self.canvas.surface.canvas, 0, 0)
#        self.canvas.drawImage(self.canvas.surface, 0, 0) #pyjs0.8 *.canvas

    def update_rect(self, rect_list):
        """
        Repaint display.
        Argument rect_list specifies a list of Rect to repaint.
        """
        for rect in rect_list:
            try:
                self.canvas.drawImage(self.canvas.surface.canvas, rect.x,rect.y,rect.width,rect.height, rect.x,rect.y,rect.width,rect.height)
            except IndexSizeError:
                rx = self.canvas.surface.get_rect().clip(rect)
                if rx.width and rx.height:
                    self.canvas.drawImage(self.canvas.surface.canvas, rx.x,rx.y,rx.width,rx.height, rx.x,rx.y,rx.width,rx.height)
        return None

    def update(self, rect_list=None):
        """
        Repaint display.
        An optional rect_list to specify regions to repaint.
        """
        if not isinstance(rect_list, list):
            if not rect_list:
                self.canvas.drawImage(self.canvas.surface.canvas, 0, 0)
#                self.canvas.drawImage(self.canvas.surface, 0, 0) #pyjs0.8 *.canvas
                return None
            else:
                rect_list = [rect_list]
        for rect in rect_list:
            try:
                x, y, w, h = rect[0], rect[1], rect[2], rect[3]
                #pyjs -O no attribute checking of Rect obj
                try:
                    self.canvas.drawImage(self.canvas.surface.canvas, x,y,w,h, x,y,w,h)
#                    self.canvas.drawImage(self.canvas.surface, x,y,w,h, x,y,w,h) #pyjs0.8 *.canvas
                except IndexSizeError:
                    if isinstance(rect, Rect):
                        rx = self.canvas.surface.get_rect().clip(rect)
                    else:
                        rx = self.canvas.surface.get_rect().clip(Rect(x,y,w,h))
                    if rx.width and rx.height:
                        self.canvas.drawImage(self.canvas.surface.canvas, rx.x,rx.y,rx.width,rx.height, rx.x,rx.y,rx.width,rx.height)    #pyjs0.8 *.canvas
            except (TypeError, AttributeError):     #pyjs -O TypeError -S AttributeError
                continue    #rect is None
        return None


class Textbox(TextBox):
    """
    TextBox object for text input, subclass of Pyjs TextBox class.
    Optional attribute size (x,y) specifying textbox dimensions and panel to hold element, default size derived from Canvas size placed in lower VerticalPanel.
    Module initialization provides pyjsdl.display.textbox instance.
    """

    def __init__(self, size=None, panel=None):
        TextBox.__init__(self)
        if not size:
            self.width, self.height = env.canvas.surface.width-5, 20
        else:
            self.width, self.height = int(size[0]), int(size[1])
        self.setSize(str(self.width)+'px', str(self.height)+'px')
        self.setVisible(False)
        if panel:
            panel.add(self)
        else:
            try:
                env.canvas.surface._display.vpanel.add(self)
            except (TypeError, AttributeError):
                env.canvas.surface._display.vpanel = VerticalPanel()
                RootPanel().add(env.canvas.surface._display.vpanel)
                env.canvas.surface._display.vpanel.add(self)

    def resize(self, width=None, height=None):
        if not (width or height):
            self.width, self.height = env.canvas.surface.width-5, 20
        else:
            if width:
                self.width = int(width)
            if height:
                self.height = int(height)
        self.setSize(str(self.width)+'px', str(self.height)+'px')

    def toggle(self, visible=None):
        if visible:
            self.setVisible(visible)
        else:
            self.setVisible(not self.getVisible())


class Textarea(TextArea):
    """
    TextArea object for text input/output, subclass of Pyjs TextArea class.
    Optional attribute size (x,y) specifying textarea dimensions and panel to hold element, default size derived from Canvas size placed in lower VerticalPanel.
    Module initialization provides pyjsdl.display.textarea instance.
    """

    def __init__(self, size=None, panel=None):
        TextArea.__init__(self)
        if not size:
            self.width, self.height = env.canvas.surface.width-5, int(env.canvas.surface.height/5)-5
        else:
            self.width, self.height = int(size[0]), int(size[1])
        self.setSize(str(self.width)+'px', str(self.height)+'px')
        self.setStyleAttribute({'resize':'vertical'})
        self.setVisible(False)
        if panel:
            panel.add(self)
        else:
            try:
                env.canvas.surface._display.vpanel.add(self)
            except (TypeError, AttributeError):
                env.canvas.surface._display.vpanel = VerticalPanel()
                RootPanel().add(env.canvas.surface._display.vpanel)
                env.canvas.surface._display.vpanel.add(self)

    def resize(self, width=None, height=None):
        if not (width or height):
            self.width, self.height = env.canvas.surface.width-5, int(env.canvas.surface.height/5)-5
        else:
            if width:
                self.width = int(width)
            if height:
                self.height = int(height)
        self.setSize(str(self.width)+'px', str(self.height)+'px')

    def toggle(self, visible=None):
        if visible:
            self.setVisible(visible)
        else:
            self.setVisible(not self.getVisible())


class IndexSizeError(Exception):
    pass

