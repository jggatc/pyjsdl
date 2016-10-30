#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

import base64
from pyjsdl.surface import Surface
from pyjsdl.rect import Rect
from pyjsdl.time import Time
from pyjsdl.color import Color
from pyjsdl import env
import pyjsdl.event
from pyjsdl.pyjsobj import DOM, Window, RootPanel, FocusPanel, VerticalPanel, loadImages, TextBox, TextArea, MouseWheelHandler, eventGetMouseWheelVelocityY, Event, requestAnimationFrameInit
from __pyjamas__ import JS

__docformat__ = 'restructuredtext'


_canvas = None
_ctx = None
_img = None
_wnd = None


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
        self.images = {}
        self.image_list = []
        self.callback = None
        self.time = Time()
        self.event = pyjsdl.event
        self.addMouseListener(self)
        self.addMouseWheelListener(self)
        self.addKeyboardListener(self)
        self.sinkEvents(Event.ONMOUSEDOWN | Event.ONMOUSEUP| Event.ONMOUSEMOVE | Event.ONMOUSEOUT | Event.ONMOUSEWHEEL | Event.ONKEYDOWN | Event.ONKEYPRESS | Event.ONKEYUP)
        self.modKey = pyjsdl.event.modKey
        self.specialKey = pyjsdl.event.specialKey
        self._repaint = False
        self._rect_list = []
        self._rect_len = 0
        self._rect_num = 0
        self._framerate = 0
        self._frametime = 0
        self._canvas_init()
        self.initialized = False

    def _canvas_init(self):
        global _canvas, _ctx, _img, _wnd
        _canvas = self
        _ctx = self.impl.canvasContext
        _img = self.surface.canvas
        _wnd = requestAnimationFrameInit()

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
        if self._bufferedimage:
            self.surface.resize(width, height)
        self.surface._display._surface_rect = self.surface.get_rect()

    def set_callback(self, cb):
        if not hasattr(cb, 'run'):
            self.callback = Callback(cb)
        else:
            self.callback = cb

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

    def onImagesLoaded(self, images):
        for i, image in enumerate(self.image_list):
            self.images[image] = images[i].getElement()
        self.start()

    def start(self):
        if not self.initialized:
            self.initialized = True
            _wnd.requestAnimationFrame(run)
            self.time.timeout(0, self)

    def stop(self):
        global run
        run = lambda ts: None
        self.run = lambda: None

    def _get_rect(self):
        if self._rect_num < self._rect_len:
            return self._rect_list[self._rect_num]
        else:
            self._rect_list.append(Rect(0,0,0,0))
            self._rect_len += 1
            return self._rect_list[self._rect_num]

    def run(self):
        if not self._repaint:
            self.callback.run()
            self._repaint = True
        self.time.timeout(0, self)


def run(timestamp):
    _wnd.requestAnimationFrame(run)
    if _canvas._repaint:
        if (timestamp-_canvas._frametime) >= _canvas._framerate:
            _canvas._frametime = timestamp
            while _canvas._rect_num:
                rect = _canvas._rect_list[_canvas._rect_num-1]
                _ctx.drawImage(_img, rect.x,rect.y,rect.width,rect.height,
                                     rect.x,rect.y,rect.width,rect.height)
                _canvas._rect_num -= 1
            _canvas._repaint = False


class Callback(object):

    __slots__ = ['run']

    def __init__(self, cb):
        self.run = cb


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
        return self.surface

    def setup(self, callback, images=None):
        """
        Initialize Canvas for script execution.
        Argument include callback function to run and optional images list to preload.
        Callback function can also be an object with a run method to call.
        The images can be image URL, or file-like object or base64 data in format (name.ext,data).
        """
        self.canvas.set_callback(callback)
        image_list = []
        if self._image_list:
            image_list.extend(self._image_list)
            self._image_list[:] = []
        if images:
            image_list.extend(images)
        self.canvas.load_images(image_list)

    def set_callback(self, callback):
        """
        Set Canvas callback function.
        Argument callback function to run.
        Callback function can also be an object with a run method to call.
        """
        if self.canvas.initialized:
            self.canvas.set_callback(callback)
        else:
            self.setup(callback)

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
        self.canvas.impl.canvasContext.drawImage(self.surface.canvas, 0, 0)
        return None

    def update(self, rect_list=None):
        """
        Repaint display.
        Optional rect or rect list to specify regions to repaint.
        """
        if hasattr(rect_list, 'append'):
            _update(self.canvas, rect_list)
        elif rect_list:
            _update(self.canvas, [rect_list])
        else:
            self.flip()
        return None


def _update(canvas, rect_list):
    for rect in rect_list:
        if hasattr(rect, 'width'):
            if (rect.width > 0) and (rect.height > 0):
                repaint_rect = canvas._get_rect()
                repaint_rect.x = rect.x
                repaint_rect.y = rect.y
                repaint_rect.width = rect.width
                repaint_rect.height = rect.height
                canvas._rect_num += 1
        elif rect:
            if (rect[2] > 0) and (rect[3] > 0):
                repaint_rect = canvas._get_rect()
                repaint_rect.x = rect[0]
                repaint_rect.y = rect[1]
                repaint_rect.width = rect[2]
                repaint_rect.height = rect[3]
                canvas._rect_num += 1


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

