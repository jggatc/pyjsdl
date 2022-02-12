#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl import env
from pyjsdl import key
from pyjsdl import constants as Const

__docformat__ = 'restructuredtext'


class Event(object):
    """
    **pyjsdl.event**
    
    * pyjsdl.event.pump
    * pyjsdl.event.get
    * pyjsdl.event.poll
    * pyjsdl.event.wait
    * pyjsdl.event.peek
    * pyjsdl.event.clear
    * pyjsdl.event.event_name
    * pyjsdl.event.set_blocked
    * pyjsdl.event.set_allowed
    * pyjsdl.event.get_blocked
    * pyjsdl.event.post
    * pyjsdl.event.Event
    """

    def __init__(self):
        """
        Maintain events received from browser.
        
        Module initialization creates pyjsdl.event instance.
        """
        self.eventQueue = [None for i in range(256)]
        self.eventNum = 0
        self.eventQueueTmp = [None for i in range(256)]
        self.eventNumTmp = 0
        self.queueLock = False
        self.queueAccess = False
        self.queue = []
        self.queueNil = []
        self.queueTmp = []
        self.mousePress = {0:False, 1:False, 2:False}
        self.mouseMove = {'x':-1, 'y':-1}
        self.mouseMovePre = {'x':0, 'y':0}
        self.mouseMoveRel = {'x':None, 'y':None}
        self.keyPress = {Const.K_ALT: False,
                         Const.K_CTRL: False,
                         Const.K_SHIFT: False}
        self.keyMod = {Const.K_ALT: {True:Const.KMOD_ALT, False:0},
                       Const.K_CTRL: {True:Const.KMOD_CTRL, False:0},
                       Const.K_SHIFT: {True:Const.KMOD_SHIFT, False:0}}
        self.eventName = {Const.MOUSEMOTION: 'MouseMotion',
                          Const.MOUSEBUTTONDOWN: 'MouseButtonDown',
                          Const.MOUSEBUTTONUP: 'MouseButtonUp',
                          Const.KEYDOWN: 'KeyDown',
                          Const.KEYUP: 'KeyUp',
                          'mousemove': 'MouseMotion',
                          'mousedown': 'MouseButtonDown',
                          'mouseup': 'MouseButtonUp',
                          'keydown': 'KeyDown',
                          'keyup': 'KeyUp'}
        self.eventType = [Const.MOUSEMOTION,
                          Const.MOUSEBUTTONDOWN, Const.MOUSEBUTTONUP,
                          Const.KEYDOWN, Const.KEYUP,
                          'mousemove', 'mousedown', 'mouseup',
                          'wheel', 'mousewheel', 'DOMMouseScroll',
                          'keydown', 'keypress', 'keyup']
        self.events = set(self.eventType)
        self.eventTypes = {Const.MOUSEMOTION: set([Const.MOUSEMOTION, 'mousemove']),
                           Const.MOUSEBUTTONDOWN: set([Const.MOUSEBUTTONDOWN,
                               'mousedown', 'wheel', 'mousewheel', 'DOMMouseScroll']),
                           Const.MOUSEBUTTONUP: set([Const.MOUSEBUTTONUP, 'mouseup']),
                           Const.KEYDOWN: set([Const.KEYDOWN, 'keydown', 'keypress']),
                           Const.KEYUP: set([ Const.KEYUP, 'keyup'])}
        self.eventObj = {'mousedown': MouseDownEvent,
                         'mouseup': MouseUpEvent,
                         'wheel': MouseWheelEvent,
                         'mousewheel': MouseWheelEvent,
                         'DOMMouseScroll': _MouseWheelEvent,
                         'mousemove': MouseMoveEvent,
                         'keydown': KeyDownEvent,
                         'keyup': KeyUpEvent}
        self.modKey = key._modKey
        self.specialKey = key._specialKey
        self.modKeyCode = key._modKeyCode
        self.specialKeyCode = key._specialKeyCode
        self.touchlistener = None
        self.keyRepeat = [0, 0]
        self.keyHeld = {}
        self.keyCode = 0
        self.keyPressCode = {}
        self.Event = UserEvent
        self._nonimplemented_methods()

    def _lock(self):
        self.queueLock = True

    def _unlock(self):
        self.queueLock = False

    def _updateQueue(self, event):
        self.queueAccess = True
        if not self.queueLock:
            if self.eventNumTmp:
                 self._appendMerge()
            self._append(event)
        else:
            self._appendTmp(event)
        self.queueAccess = False

    def _append(self, event):
        if self.eventNum < 255:
            self.eventQueue[self.eventNum] = event
            self.eventNum += 1

    def _appendTmp(self, event):
        if self.eventNumTmp < 255:
            self.eventQueueTmp[self.eventNumTmp] = event
            self.eventNumTmp += 1

    def _appendMerge(self):
        for i in range(self.eventNumTmp):
            self._append( self.eventQueueTmp[i] )
            self.eventQueueTmp[i] = None
        self.eventNumTmp = 0

    def pump(self):
        """
        Process events to reduce queue overflow, unnecessary if processing with other methods.
        """
        if self.eventNum > 250:
            self._lock()
            self._pump()
            self._unlock()
        return None

    def _pump(self):
        queue = self.eventQueue[50:self.eventNum]
        self.eventNum -= 50
        for i in range(self.eventNum):
            self.eventQueue[i] = queue[i]

    def get(self, eventType=None):
        """
        Return list of events, and queue is reset.
        Optional eventType argument of single or list of event type(s) to return.
        """
        if not self.eventNum:
            return self.queueNil
        self._lock()
        if not eventType:
            self.queue = self.eventQueue[0:self.eventNum]
            self.eventNum = 0
        else:
            self.queue = []
            if isinstance(eventType, (tuple,list)):
                for i in range(self.eventNum):
                    if self.eventQueue[i].type not in eventType:
                        self.queueTmp.append(self.eventQueue[i])
                    else:
                        self.queue.append(self.eventQueue[i])
            else:
                for i in range(self.eventNum):
                    if self.eventQueue[i].type != eventType:
                        self.queueTmp.append(self.eventQueue[i])
                    else:
                        self.queue.append(self.eventQueue[i])
            if not self.queueTmp:
                self.eventNum = 0
            else:
                self.eventNum = len(self.queueTmp)
                for i in range(self.eventNum):
                    self.eventQueue[i] = self.queueTmp[i]
                self.queueTmp[:] = []
            if self.eventNum > 250:
                self._pump()
        self._unlock()
        return self.queue

    def poll(self):
        """
        Return an event from the queue, or event type NOEVENT if none present.
        """
        self._lock()
        if self.eventNum:
            evt = self.eventQueue.pop(0)
            self.eventNum -= 1
            self.eventQueue.append(None)
            if self.eventNum > 250:
                self._pump()
        else:
            evt = self.Event(Const.NOEVENT)
        self._unlock()
        return evt

    def wait(self):     #not implemented in js
        """
        Return an event from the queue.
        """
        while True:
            if self.eventNum:
                self._lock()
                evt = self.eventQueue.pop(0)
                self.eventNum -= 1
                self.eventQueue.append(None)
                if self.eventNum > 250:
                    self._pump()
                self._unlock()
                return evt
            else:
                self._unlock()
                return None

    def peek(self, eventType=None):
        """
        Check if an event of given type is present.
        Optional eventType argument specifies event type or list, which defaults to all.
        """
        if not self.eventNum:
            return False
        elif eventType is None:
            return True
        self._lock()
        evt = [event.type for event in self.eventQueue[0:self.eventNum]]
        if self.eventNum > 250:
            self._pump()
        self._unlock()
        if isinstance(eventType, (tuple,list)):
            for evtType in eventType:
                if evtType in evt:
                    return True
        else:
            if eventType in evt:
                return True
        return False

    def clear(self, eventType=None):
        """
        Remove events of a given type from queue.
        Optional eventType argument specifies event type or list, which defaults to all.
        """
        if not self.eventNum:
            return None
        self._lock()
        if eventType is None:
            self.eventNum = 0
        else:
            if isinstance(eventType, (tuple,list)):
                for i in range(self.eventNum):
                    if self.eventQueue[i].type not in eventType:
                        self.queueTmp.append(self.eventQueue[i])
            else:
                for i in range(self.eventNum):
                    if self.eventQueue[i].type != eventType:
                        self.queueTmp.append(self.eventQueue[i])
            if not self.queueTmp:
                self.eventNum = 0
            else:
                self.eventNum = len(self.queueTmp)
                for i in range(self.eventNum):
                    self.eventQueue[i] = self.queueTmp[i]
                self.queueTmp[:] = []
            if self.eventNum > 250:
                self._pump()
        self._unlock()
        return None

    def event_name(self, eventType):
        """
        Return event name of a event type.
        """
        if eventType in self.eventName:
            return self.eventName[eventType]
        else:
            return None

    def set_blocked(self, eventType):
        """
        Block specified event type(s) from queue.
        """
        if eventType is not None:
            if isinstance(eventType, (tuple,list)):
                for evtType in eventType:
                    self.events = self.events.difference(
                                      self.eventTypes[evtType])
            else:
                self.events = self.events.difference(
                                  self.eventTypes[eventType])
        else:
            self.events = set(self.eventType)
        return None

    def set_allowed(self, eventType):
        """
        Set allowed event type(s) on queue.
        """
        if eventType is not None:
            if isinstance(eventType, (tuple,list)):
                for evtType in eventType:
                    self.events = self.events.union(
                                      self.eventTypes[evtType])
            else:
                self.events = self.events.union(
                                  self.eventTypes[eventType])
        else:
            self.events.clear()
        return None

    def get_blocked(self, eventType):
        """
        Check if specified event type is blocked from queue.
        """
        if eventType not in self.events:
            return True
        else:
            return False

    def post(self, event):
        """
        Post event to queue.
        """
        self._lock()
        if event.type in self.events:
            self._append(event)
        self._unlock()
        return None

    def _set_key_event(self):
        self.eventObj['keydown'] = _KeyDownEvent
        self.eventObj['keyup'] = _KeyUpEvent
        self.eventObj['keypress'] = _KeyPressEvent

    def _initiate_touch_listener(self, canvas):
        self.touchlistener = TouchListener(canvas)
        return None

    def _register_event(self, eventType):
        if eventType not in self.eventTypes:
            self.eventTypes[eventType] = eventType
            self.eventName[eventType] = 'UserEvent'
            self.eventType.append(eventType)
            self.events = self.events.union(set([eventType]))
            #pyjs -S set add/remove member check issue

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.set_grab = lambda *arg: None
        self.get_grab = lambda *arg: False


class UserEvent(object):

    __slots__ = ['type', 'attr']

    def __init__(self, eventType, *args, **kwargs):
        """
        Return user event.
        Argument includes eventType (USEREVENT+num).
        Optional attribute argument as dictionary ({str:val}) or keyword arg(s).
        """
        if args:
            attr = args[0]
        else:
            attr = kwargs
        object.__setattr__(self, "type", eventType)
        object.__setattr__(self, "attr", attr)
        if env.pyjs_mode.optimized: #__getattr__ not implemented in pyjs -O
            for attr in self.attr:
                object.__setattr__(self, attr, self.attr[attr])
        env.event._register_event(eventType)

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return self.toString()

    def __getattr__(self, attr):
        if attr in self.attr:
            return self.attr[attr]
        else:
            raise AttributeError(
                "'Event' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self.attr[attr] = value

    def toString(self):
        event_name = env.event.event_name(self.type)
        return "<Event(%s-%s %r)>" % (self.type, event_name, self.attr)


class JEvent(object):
    """
    Event object wraps browser event.

    Event object attributes:

    * type: MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN, KEYUP
    * button: mouse button pressed (1-5)
    * buttons: mouse buttons pressed (1,2,3)
    * pos: mouse position (x,y)
    * rel: mouse relative position change (x,y)
    * key: keycode of key pressed (K_a-K_z...)
    """

    __slots__ = []

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return self.toString()

    def toString(self):
        event_name = self._eventName[self.type]
        attr = {}
        for name in self.__slots__[1:-1]:
            attr[name] = getattr(self, name)
        return "<Event(%s-%s %r)>" % (self.type, event_name, repr(attr))

    def getEvent(self):
        """
        Return browser event.
        """
        return self.event


class MouseEvent(JEvent):

    _types = {'mousemove': Const.MOUSEMOTION,
              'mousedown': Const.MOUSEBUTTONDOWN,
              'mouseup': Const.MOUSEBUTTONUP,
              'wheel': Const.MOUSEBUTTONDOWN,
              'mousewheel': Const.MOUSEBUTTONDOWN,
              'DOMMouseScroll': Const.MOUSEBUTTONDOWN}
    _eventName = {Const.MOUSEMOTION: 'MouseMotion',
                  Const.MOUSEBUTTONDOWN: 'MouseButtonDown',
                  Const.MOUSEBUTTONUP: 'MouseButtonUp'}

    __slots__ = []


class MouseDownEvent(MouseEvent):

    __slots__ = ['type', 'button', 'pos', 'event']

    def __init__(self, event, x, y):
        self.event = event
        self.type = self._types[event.type]
        self.button = event.button + 1
        self.pos = (x + env.frame.scrollLeft,
                    y + env.frame.scrollTop)


class MouseUpEvent(MouseEvent):

    __slots__ = ['type', 'button', 'pos', 'event']

    def __init__(self, event, x, y):
        self.event = event
        self.type = self._types[event.type]
        self.button = event.button + 1
        self.pos = (x + env.frame.scrollLeft,
                    y + env.frame.scrollTop)


class MouseWheelEvent(MouseEvent):

    __slots__ = ['type', 'button', 'pos', 'event']

    def __init__(self, event, x, y):
        self.event = event
        self.type = self._types[event.type]
        if event.deltaY < 0:
            self.button = 4
        else:
            self.button = 5
        self.pos = (x + env.frame.scrollLeft,
                    y + env.frame.scrollTop)


class _MouseWheelEvent(MouseEvent):

    __slots__ = ['type', 'button', 'pos', 'event']

    def __init__(self, event, x, y):
        self.event = event
        self.type = self._types[event.type]
        if event.detail < 0:
            self.button = 4
        else:
            self.button = 5
        self.pos = (x + env.frame.scrollLeft,
                    y + env.frame.scrollTop)


class MouseMoveEvent(MouseEvent):

    __slots__ = ['type', 'buttons', 'pos', 'rel', 'event']

    def __init__(self, event, x, y):
        self.event = event
        self.type = self._types[event.type]
        self.buttons = ((int(event.buttons) & 1) == 1,
                        (int(event.buttons) & 4) == 4,
                        (int(event.buttons) & 2) == 2)
        self.pos = (x + env.frame.scrollLeft,
                    y + env.frame.scrollTop)
        self.rel = (x - env.event.mouseMovePre['x'],
                    y - env.event.mouseMovePre['y'])


class KeyEvent(JEvent):

    _types = {'keydown': Const.KEYDOWN,
              'keyup': Const.KEYUP,
              'keypress': Const.KEYDOWN}
    _eventName = {Const.KEYDOWN: 'KeyDown',
                  Const.KEYUP: 'KeyUp'}
    _code = key._code
    _specialKey = key._specialKey
    _specialKeyCode = key._specialKeyCode

    __slots__ = []


class KeyDownEvent(KeyEvent):

    __slots__ = ['type', 'key', 'mod', 'unicode', 'event']

    def __init__(self, event):
        self.event = event
        self.type = self._types[event.type]
        if event.key in self._specialKey:
            self.key = self._specialKey[event.key]
            if self.key in (9, 13):
                self.unicode = chr(self.key)
            else:
                self.unicode = ''
        else:
            if hasattr(event, 'code'):
                if event.code in self._code:
                    self.key = self._code[event.code]
                else:
                    self.key = event.code
            else:
                self.key = event.which or event.keyCode or 0
            self.unicode = event.key
        self.mod = ( (int(event.altKey) * Const.KMOD_ALT) |
                     (int(event.ctrlKey) * Const.KMOD_CTRL) |
                     (int(event.shiftKey) * Const.KMOD_SHIFT) )

class KeyUpEvent(KeyEvent):

    __slots__ = ['type', 'key', 'mod', 'unicode', 'event']

    def __init__(self, event):
        self.event = event
        self.type = self._types[event.type]
        if event.key in self._specialKey:
            self.key = self._specialKey[event.key]
            if self.key in (9, 13):
                self.unicode = chr(self.key)
            else:
                self.unicode = ''
        else:
            if hasattr(event, 'code'):
                if event.code in self._code:
                    self.key = self._code[event.code]
                else:
                    self.key = event.code
            else:
                self.key = event.which or event.keyCode or 0
            self.unicode = event.key
        self.mod = ( (int(event.altKey) * Const.KMOD_ALT) |
                     (int(event.ctrlKey) * Const.KMOD_CTRL) |
                     (int(event.shiftKey) * Const.KMOD_SHIFT) )


class _KeyDownEvent(KeyEvent):

    __slots__ = ['type', 'key', 'mod', 'unicode', 'event']

    def __init__(self, event, keycode):
        self.event = event
        self.type = self._types[event.type]
        self.key = self._specialKeyCode[keycode]
        if self.key in (9, 13):
            self.unicode = chr(self.key)
        else:
            self.unicode = ''
        self.mod = ( (int(event.altKey) * Const.KMOD_ALT) |
                     (int(event.ctrlKey) * Const.KMOD_CTRL) |
                     (int(event.shiftKey) * Const.KMOD_SHIFT) )


class _KeyUpEvent(KeyEvent):

    __slots__ = ['type', 'key', 'mod', 'unicode', 'event']

    def __init__(self, event, keycode):
        self.event = event
        self.type = self._types[event.type]
        if keycode in self._specialKeyCode:
            self.key = self._specialKeyCode[keycode]
            if keycode in (9, 13):
                self.unicode = chr(keycode)
            else:
                self.unicode = ''
        else:
            if keycode in env.event.keyPressCode:
                _keycode = env.event.keyPressCode[keycode]
                self.key = _keycode
                if 65 <= _keycode <= 90:
                    self.unicode = chr(_keycode+32)
                else:
                    self.unicode = chr(_keycode)
            else:
                if 65 <= keycode <= 90:
                    self.key = keycode + 32
                    self.unicode = chr(keycode+32)
                else:
                    self.key = keycode
                    self.unicode = chr(keycode)
        self.mod = ( (int(event.altKey) * Const.KMOD_ALT) |
                     (int(event.ctrlKey) * Const.KMOD_CTRL) |
                     (int(event.shiftKey) * Const.KMOD_SHIFT) )


class _KeyPressEvent(KeyEvent):

    __slots__ = ['type', 'key', 'mod', 'unicode', 'event']

    def __init__(self, event, keycode):
        self.event = event
        self.type = self._types[event.type]
        self.key = keycode
        if 65 <= keycode <= 90:
            self.unicode = chr(keycode+32)
        else:
            self.unicode = chr(keycode)
        self.mod = ( (int(event.altKey) * Const.KMOD_ALT) |
                     (int(event.ctrlKey) * Const.KMOD_CTRL) |
                     (int(event.shiftKey) * Const.KMOD_SHIFT) )


class TouchListener:
    """
    **event.touchlistener**

    * event.touchlistener.add_callback
    * event.touchlistener.is_active
    """

    def __init__(self, canvas):
        """
        Touch event listener.

        Refer to touch event api documentation:
          https://developer.mozilla.org/en-US/docs/Web/API/TouchEvent.
        Notes:
          The event.touches attribute is a list of touch objects.
          Use len(touches) for touch count and touches.item(<index>) to retrieve touch object.
          The touch attribute touch.clientX/touch.clientY provides touch position.
          Position offset checked by display getAbsoluteLeft/getAbsoluteTop/getScrollLeft/getScrollTop.
          Browser triggers delayed mousedown/mouseup event after touchstart/touchend event.
        Module initialization creates pyjsdl.event.touchlistener instance.
        """
        global _canvas
        _canvas = canvas
        self.element = canvas.getElement()
        self.element.addEventListener('touchstart', _touch_detect)
        self.active = False
        self.callback = []

    def activate(self):
        self.element.removeEventListener('touchstart', _touch_detect)
        self.element.addEventListener('touchstart', _touch_start)
        self.element.addEventListener('touchend', _touch_end)
        self.element.addEventListener('touchmove', _touch_move)
        self.element.addEventListener('touchcancel', _touch_cancel)
        self.active = True

    def add_callback(self, callback):
        """
        Add callback object to receive touch events.
        The callback should have methods onTouchStart, onTouchEnd, onTouchMove, and onTouchCancel.
        Optional callback method onTouchInitiate used to report initial touch event detection.
        Callback methods will be called with an event argument.
        """
        self.callback.append(callback)
        return None

    def is_active(self):
        """
        Check if touch event is registered.
        """
        return self.active

_canvas = None

def _touch_detect(event):
    _canvas.onTouchInitiate(event)

def _touch_start(event):
    _canvas.onTouchStart(event)

def _touch_end(event):
    _canvas.onTouchEnd(event)

def _touch_move(event):
    _canvas.onTouchMove(event)

def _touch_cancel(event):
    _canvas.onTouchCancel(event)

