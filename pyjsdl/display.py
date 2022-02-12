#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

import base64
from pyjsdl.surface import Surface
from pyjsdl.rect import Rect
from pyjsdl.time import Time
from pyjsdl import env
from pyjsdl.pyjsobj import DOM, Window, RootPanel, SimplePanel, VerticalPanel, loadImages, TextBox, TextArea, Event, requestAnimationFrameInit

__docformat__ = 'restructuredtext'


_canvas = None
_ctx = None
_img = None
_wnd = None


class Canvas(Surface):

    def __init__(self, size, buffered):
        Surface.__init__(self, size)
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
        self.event = env.event
        self.addMouseListener(self)
        self.addKeyEventListener(self)
        self.sinkEvents(Event.ONMOUSEDOWN |
                        Event.ONMOUSEUP |
                        Event.ONMOUSEMOVE |
                        Event.ONMOUSEOUT |
                        Event.ONMOUSEWHEEL |
                        Event.ONKEYDOWN |
                        Event.ONKEYPRESS |
                        Event.ONKEYUP)
        self.onContextMenu = None
        self.preventContextMenu()
        self.evt = self.event.eventObj
        self.modKey = self.event.modKey
        self.specialKey = self.event.specialKey
        self.modKeyCode = self.event.modKeyCode
        self.specialKeyCode = self.event.specialKeyCode
        self.keyRepeat = self.event.keyRepeat
        self.keyHeld = self.event.keyHeld
        self.mouse_entered = True
        self.event._initiate_touch_listener(self)
        self._touch_callback = self.event.touchlistener.callback
        self._rect_list = []
        self._rect_len = 0
        self._rect_num = 0
        self._framerate = 0
        self._frametime = 0
        self._rendertime = self.time.time()
        self._pause = False
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
        if event.type in self.event.events:
            if not self.mouse_entered:
                self.event.mouseMovePre['x'] = self.event.mouseMove['x']
                self.event.mouseMovePre['y'] = self.event.mouseMove['y']
            else:
                self.event.mouseMovePre['x'] = x
                self.event.mouseMovePre['y'] = y
                self.mouse_entered = False
            self.event._updateQueue(self.evt[event.type](event, x, y))
        self.event.mouseMove['x'] = x
        self.event.mouseMove['y'] = y

    def onMouseDown(self, sender, x, y):
        event = DOM.eventGetCurrentEvent()
        if event.type in self.event.events:
            self.event._updateQueue(self.evt[event.type](event, x, y))
        self.event.mousePress[event.button] = True

    def onMouseUp(self, sender, x, y):
        event = DOM.eventGetCurrentEvent()
        if event.type in self.event.events:
            self.event._updateQueue(self.evt[event.type](event, x, y))
        self.event.mousePress[event.button] = False

    def onMouseEnter(self, sender):
        self.mouse_entered = True

    def onMouseLeave(self, sender):
        self.event.mousePress[0] = False
        self.event.mousePress[1] = False
        self.event.mousePress[2] = False
        self.event.mouseMove['x'] = -1
        self.event.mouseMove['y'] = -1
        self.event.mouseMoveRel['x'] = None
        self.event.mouseMoveRel['y'] = None
        for keycode in self.modKeyCode:
            if self.event.keyPress[keycode]:
                self.event.keyPress[keycode] = False

    def onMouseWheel(self, event):
        if event.type in self.event.events:
            r = self.canvas.getBoundingClientRect()
            x = event.clientX - round(r.left)
            y = event.clientY - round(r.top)
            self.event._updateQueue(self.evt[event.type](event, x, y))
        DOM.eventPreventDefault(event)

    def onKeyEvent(self, event):
        self.removeKeyEventListener(self)
        self.addKeyboardListener(self)
        DOM.currentEvent = event
        if hasattr(event, 'key') and hasattr(event, 'code'):
            self.onKeyDown(self, event.key, 0)
        else:
            self.event._set_key_event()
            self.onKeyDown = self._onKeyDown
            self.onKeyUp = self._onKeyUp
            self.onKeyPress = self._onKeyPress
            keycode = event.which or event.keyCode or 0
            self._onKeyDown(self, keycode, 0)

    def onKeyDown(self, sender, keycode, mods):
        event = DOM.eventGetCurrentEvent()
        if event.key in self.modKey:
            self.event.keyPress[self.modKey[event.key]] = True
        if event.type in self.event.events:
            if not self._isPaused(event.key):
                self.event._updateQueue(self.evt[event.type](event))
        DOM.eventPreventDefault(event)

    def onKeyUp(self, sender, keycode, mods):
        event = DOM.eventGetCurrentEvent()
        if event.key in self.modKey:
            self.event.keyPress[self.modKey[event.key]] = False
        if event.key in self.keyHeld:
            self.keyHeld[event.key]['pressed'] = False
        if event.type in self.event.events:
            self.event._updateQueue(self.evt[event.type](event))

    def _onKeyDown(self, sender, keycode, mods):
        event = DOM.eventGetCurrentEvent()
        if keycode in self.modKeyCode:
            self.event.keyPress[keycode] = True
        if event.type in self.event.events:
            if not self._isPaused(keycode):
                self.event.keyCode = keycode
                if keycode in self.specialKeyCode:
                    self.event._updateQueue(self.evt[event.type](event, keycode))
                    DOM.eventPreventDefault(event)
            else:
                DOM.eventPreventDefault(event)

    def _onKeyUp(self, sender, keycode, mods):
        event = DOM.eventGetCurrentEvent()
        if keycode in self.modKeyCode:
            self.event.keyPress[keycode] = False
        if keycode in self.keyHeld:
            self.keyHeld[keycode]['pressed'] = False
        if event.type in self.event.events:
            self.event._updateQueue(self.evt[event.type](event, keycode))

    def _onKeyPress(self, sender, keycode, mods):
        event = DOM.eventGetCurrentEvent()
        if event.type in self.event.events:
            self.event.keyPressCode[self.event.keyCode] = keycode
            self.event._updateQueue(self.evt[event.type](event, keycode))
        event.preventDefault()

    def _isPaused(self, keycode):
        if keycode not in self.keyHeld:
            self.keyHeld[keycode] = {'pressed':False, 'delay':False, 'time':0}
        key = self.keyHeld[keycode]
        if not key['pressed']:
            key['pressed'] = True
            paused = False
            if self.keyRepeat[0]:
                key['delay'] = True
                key['time'] = self.time.time()
        else:
            paused = True
            if self.keyRepeat[0]:
                time = self.time.time()
                if key['delay']:
                    if time - key['time'] > self.keyRepeat[0]:
                        key['time'] = time
                        key['delay'] = False
                        paused = False
                elif time - key['time'] > self.keyRepeat[1]:
                    key['time'] = time
                    paused = False
        return paused

    def onTouchInitiate(self, event):
        self.event.touchlistener.activate()
        for callback in self._touch_callback:
            if hasattr(callback, 'onTouchInitiate'):
                callback.onTouchInitiate(event)
        self.onTouchStart(event)

    def onTouchStart(self, event):
        for callback in self._touch_callback:
            callback.onTouchStart(event)

    def onTouchEnd(self, event):
        for callback in self._touch_callback:
            callback.onTouchEnd(event)

    def onTouchMove(self, event):
        for callback in self._touch_callback:
            callback.onTouchMove(event)

    def onTouchCancel(self, event):
        for callback in self._touch_callback:
            callback.onTouchCancel(event)

    def preventContextMenu(self, setting=True):
        """
        Control contextmenu event.
        Optional bool setting to prevent event, default to True.
        """
        if setting:
            if self.onContextMenu: return
            element = self.getElement()
            self.onContextMenu = lambda event: event.preventDefault()
            element.addEventListener('contextmenu', self.onContextMenu)
        else:
            if not self.onContextMenu: return
            element = self.getElement()
            element.removeEventListener('contextmenu', self.onContextMenu)
            self.onContextMenu = None

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

    def update(self, timestamp):
        if not self._framerate:
            self._frametime = timestamp - self._rendertime
            self.run()
        else:
            self._frametime += timestamp - self._rendertime
            if self._frametime > self._framerate:
                self.run()
                self._frametime = 0
        self._rendertime = timestamp

    def render(self):
        while self._rect_num:
            rect = self._rect_list[self._rect_num-1]
            x,y,width,height = rect.x,rect.y,rect.width,rect.height
            _ctx.drawImage(_img, x,y,width,height, x,y,width,height)
            self._rect_num -= 1

    def run(self):
        self.callback.run()


def run(timestamp):
    _wnd.requestAnimationFrame(run)
    _canvas.update(timestamp)
    _canvas.render()


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
    * pyjsdl.display.getAbsoluteLeft
    * pyjsdl.display.getAbsoluteTop
    * pyjsdl.display.getScrollLeft
    * pyjsdl.display.getScrollTop
    * pyjsdl.display.quit
    * pyjsdl.display.get_init
    * pyjsdl.display.get_active
    * pyjsdl.display.set_caption
    * pyjsdl.display.get_caption
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
        env.set_env('canvas', self.canvas)
        self.frame = Window.getDocumentRoot()
        env.set_env('frame', self.frame)
        panel = SimplePanel(Widget=self.canvas)
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

    def getAbsoluteLeft(self):
        """
        Return canvas left-offset position.
        """
        return self.canvas.getAbsoluteLeft()

    def getAbsoluteTop(self):
        """
        Return canvas top-offset position.
        """
        return self.canvas.getAbsoluteTop()

    def getScrollLeft(self):
        """
        Return page horizontal scroll offset.
        """
        return self.frame.scrollLeft

    def getScrollTop(self):
        """
        Return page vertical scroll offset.
        """
        return self.frame.scrollTop

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
            self.width = env.canvas.surface.width - 5
            self.height = 20
        else:
            self.width = int(size[0])
            self.height = int(size[1])
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
            self.width = env.canvas.surface.width - 5
            self.height = 20
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
            self.width = env.canvas.surface.width - 5
            self.height = int(env.canvas.surface.height/5) - 5
        else:
            self.width = int(size[0])
            self.height = int(size[1])
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
            self.width = env.canvas.surface.width - 5
            self.height = int(env.canvas.surface.height/5) - 5
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

