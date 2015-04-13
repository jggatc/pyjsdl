#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from surface import Surface
from rect import Rect
from time import Time
from color import Color
import env
import pyjsdl.event
from pyjsobj import DOM, Window, RootPanel, FocusPanel, VerticalPanel, loadImages, TextBox, TextArea, MouseWheelHandler, eventGetMouseWheelVelocityY, Event
from __pyjamas__ import JS
import base64

__docformat__ = 'restructuredtext'


class Canvas(Surface, MouseWheelHandler):

    def __init__(self, size, buffered):
        Surface.__init__(self, size)
        MouseWheelHandler.__init__(self, True)
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
        self.resize(size[0], size[1])
        self.images = {}
        self.image_list = []
        self.function = None
        self.time_wait = 0
        self.time = Time()
        self.event = pyjsdl.event
        self.addMouseListener(self)
        self.addMouseWheelListener(self)
        self.addKeyboardListener(self)
        self.sinkEvents(Event.ONMOUSEDOWN | Event.ONMOUSEUP| Event.ONMOUSEMOVE | Event.ONMOUSEOUT | Event.ONMOUSEWHEEL | Event.ONKEYDOWN | Event.ONKEYPRESS | Event.ONKEYUP)
        self.modKey = pyjsdl.event.modKey
        self.specialKey = pyjsdl.event.specialKey
        self._rect_list = []
        self._rect_list.append(Rect(0,0,0,0))
        self._rect_len = 1
        self._rect_num = 0
        self._rect_temp = Rect(0,0,0,0)
        _animationFrame = self._initAnimationFrame()
        if _animationFrame:
            self.time_hold_min = 0
        else:
            self.time_hold_min = 1
        self.time_hold = self.time_hold_min

    def _initAnimationFrame(self):
        JS("""
            $wnd['requestAnimationFrame'] = $wnd['requestAnimationFrame'] ||
                                            $wnd['mozRequestAnimationFrame'] ||
                                            $wnd['webkitRequestAnimationFrame'] ||
                                            $wnd['oRequestAnimationFrame'];
           """)
        if JS("""$wnd['requestAnimationFrame'] != undefined"""):
            _animationFrame = True
        else:
            JS("""$wnd['requestAnimationFrame'] = function(cb){cb()};""")
            _animationFrame = False
        return _animationFrame

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

    def onMouseWheel(self, sender, velocity):
        event = DOM.eventGetCurrentEvent()
        if event.type == 'mousewheel':
            #TODO: update for changes in mousewheel implementation
            if hasattr(event, 'wheelDeltaX'):
                self.onMouseWheel = self._onMouseWheel
                self._onMouseWheel(sender, velocity)
            else:
                self.onMouseWheel = self._onMouseWheelY
                DOM.eventGetMouseWheelVelocityY = eventGetMouseWheelVelocityY
                self._onMouseWheelY(sender, eventGetMouseWheelVelocityY(event))
        else:       #DOMMouseScroll
            self.onMouseWheel = self._onMouseScroll
            self._onMouseScroll(sender, velocity)

    def _onMouseWheel(self, sender, velocity):
        event = DOM.eventGetCurrentEvent()
        if not event.wheelDeltaX:
            if velocity < 0:
                button = 4
                events = velocity / -3
            else:
                button = 5
                events = velocity / 3
        else:
            if velocity < 0:
                button = 6
                events = velocity / -3
            else:
                button = 7
                events = velocity / 3
        event.btn = button
        event.pos = (self.event.mouseMove['x'], self.event.mouseMove['y'])
        for evt in range(events):
            self.event._updateQueue(event)

    def _onMouseWheelY(self, sender, velocity):
        event = DOM.eventGetCurrentEvent()
        if velocity < 0:
            button = 4
            events = velocity / -3
        else:
            button = 5
            events = velocity / 3
        event.btn = button
        event.pos = (self.event.mouseMove['x'], self.event.mouseMove['y'])
        for evt in range(events):
            self.event._updateQueue(event)

    def _onMouseScroll(self, sender, velocity):
        event = DOM.eventGetCurrentEvent()
        if velocity > 1 or velocity < -1:
            if velocity < 0:
                button = 4
            else:
                button = 5
        else:
            if velocity < 0:
                button = 6
            else:
                button = 7
        event.btn = button
        event.pos = (self.event.mouseMove['x'], self.event.mouseMove['y'])
        self.event._updateQueue(event)

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

    def set_function(self, function):
        self.function = function

    def load_images(self, images):
        if images:
            image_list = []
            for image in images:
                if isinstance(image, str):
                    image_list.append(image)
                    self.image_list.append(image)
                else:
                    name = image[0]
                    if isinstance(image[1], str):
                        data = image[1]
                    else:
                        data = base64.b64encode(image[1].getvalue())
                    if not data.startswith('data:'):
                        ext = name.strip().split('.')[-1]
                        data = "data:%s;base64,%s" %(ext, data)
                        #data:[<mediatype>][;base64],<data>
                    image_list.append(data)
                    self.image_list.append(name)
            loadImages(image_list, self)
        else:
            self.start()

    def set_timeout(self, change):
        self.time_hold += change
        if self.time_hold < self.time_hold_min:
            self.time_hold = self.time_hold_min

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

    def _get_rect(self):
        if self._rect_num < self._rect_len:
            return self._rect_list[self._rect_num]
        else:
            self._rect_list.append(Rect(0,0,0,0))
            self._rect_len += 1
            return self._rect_list[self._rect_num]

    def _run(self):
        self.function()
        JS("""$wnd['requestAnimationFrame'](@{{paint}});""")

    def rerun(self):
        if not self.time_hold:
            self.run()
        else:
            self.time.timeout(self.time_hold, self)


def paint(ts):
    ctx = env.canvas.impl.canvasContext
    img = env.canvas.surface.canvas
    i = 0
    while i < env.canvas._rect_num:
        rect = env.canvas._rect_list[i]
        ctx.drawImage(img, rect.x,rect.y,rect.width,rect.height, rect.x,rect.y,rect.width,rect.height)
        i += 1
    env.canvas._rect_num = 0
    env.canvas.rerun()


class Display(object):
    """
    **pyjsdl.display**

    * pyjsdl.display.init
    * pyjsdl.display.set_mode
    * pyjsdl.display.setup
    * pyjsdl.display.setup_images
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
            self._image_list = []
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
        self._surface_rect = self.surface.get_rect()
        if not self.canvas._bufferedimage:
            self.flip = lambda: None
            self.update = lambda *arg: None
            self.update_rect = lambda *arg: None
        return self.surface

    def setup(self, function, images=None):
        """
        Initialize Canvas for script execution.
        Argument include callback function to run and optional images list to preload.
        The images can be image URL, or file-like object or base64 data in format (name.ext,data).
        """
        self.canvas.set_function(function)
        image_list = []
        if self._image_list:
            image_list.extend(self._image_list)
            self._image_list[:] = []
        if images:
            image_list.extend(images)
        self.canvas.load_images(image_list)

    def setup_images(self, images):
        """
        Add images to image preload list.
        The argument is an image or list of images representing an image URL, or file-like object or base64 data in format (name.ext,data).
        Image preloading occurs at display.setup call.
        """
        if isinstance(images, str):
            images = [images]
        self._image_list.extend(images)

    def textbox_init(self):
        """
        Initiate textbox functionality and creates instances of pyjsdl.display.textbox and pyjsdl.display.textarea placed in lower VerticalPanel.
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
        self.surface.setFillStyle(Color(0,0,0))
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
        self.canvas._rect_list[0].x = 0
        self.canvas._rect_list[0].y = 0
        self.canvas._rect_list[0].width = self._surface_rect.width
        self.canvas._rect_list[0].height = self._surface_rect.height
        self.canvas._rect_num = 1
        return None

    def update(self, rect_list=None):
        """
        Repaint display.
        An optional rect_list to specify regions to repaint.
        """
        if hasattr(rect_list, 'append'):
            _update(self.canvas, rect_list)
        else:
            if rect_list:
                _update(self.canvas, [rect_list])
            else:
                self.flip()
        return None


def _update(canvas, rect_list):
    for r in rect_list:
        if hasattr(r, 'width'):
            rect = r
        else:
            if r:
                rect = canvas._rect_temp
                rect.set(r)
            else:
                continue
        repaint_rect = canvas._get_rect()
        if rect.x >= 0:
            repaint_rect.x = rect.x
        else:
            repaint_rect.x = 0
            repaint_rect.width = rect.width + rect.x
        if rect.y >= 0:
            repaint_rect.y = rect.y
        else:
            repaint_rect.y = 0
            repaint_rect.height = rect.height + rect.y
        if rect.x+rect.width <= canvas.surface.width:
            repaint_rect.width = rect.width
        else:
            repaint_rect.width = canvas.surface.width - repaint_rect.x
            if repaint_rect.width < 1:
                continue
        if rect.y+rect.height <= canvas.surface.height:
            repaint_rect.height = rect.height
        else:
            repaint_rect.height = canvas.surface.height - repaint_rect.y
            if repaint_rect.height < 1:
                continue
        canvas._rect_num += 1
    return None


class Textbox(TextBox):
    """
    TextBox object for text input.
    Optional argument size (x,y) of textbox and panel to hold element.
    Default size derived from Canvas size placed in lower VerticalPanel.
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
    TextArea object for text input/output.
    Optional argument size (x,y) of textarea and panel to hold element.
    Default size derived from Canvas size placed in lower VerticalPanel.
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

