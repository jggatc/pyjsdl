#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from pyjsdl import env
from pyjsdl import locals as Const

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
        self.eventQueue = [None for i in range(256)]      #max 256: Error: Event queue full
#        self.eventQueue = [None] * 256      #pyjs -O TypeError
        self.eventNum = 0
        self.eventQueueTmp = [None for i in range(256)]   #used when main queue is locked
#        self.eventQueueTmp = [None] * 256   #pyjs -O TypeError
        self.eventNumTmp = 0
        self.queueLock = False
        self.queueAccess = False
        self.queue = []
        self.mousePress = {0:False, 1:False, 2:False}
        self.mouseMove = {'x':-1, 'y':-1}
        self.mouseMoveRel = {'x':None, 'y':None}
        self.keyPress = {Const.K_ALT:False, Const.K_CTRL:False, Const.K_SHIFT:False}
        self.keyMod = {Const.K_ALT:{True:Const.KMOD_ALT,False:0}, Const.K_CTRL:{True:Const.KMOD_CTRL,False:0}, Const.K_SHIFT:{True:Const.KMOD_SHIFT,False:0}}
        self.eventName = {'mousemove':'MouseMotion', 'mousedown':'MouseButtonDown', 'mouseup':'MouseButtonUp', 'keydown':'KeyDown', 'keyup':'KeyUp'}
        self.eventType = ['mousemove', 'mousedown', 'mouseup', 'wheel', 'mousewheel', 'DOMMouseScroll', 'keydown', 'keypress', 'keyup']
        self.events = set(self.eventType)
        self.eventTypes = {Const.MOUSEMOTION:['mousemove'], Const.MOUSEBUTTONDOWN:['mousedown','wheel','mousewheel', 'DOMMouseScroll'], Const.MOUSEBUTTONUP:['mouseup'], Const.KEYDOWN:['keydown','keypress'], Const.KEYUP:['keyup']}
        if env.pyjs_mode.optimized:
            self.modKey = set([Const.K_ALT, Const.K_CTRL, Const.K_SHIFT])
            self.specialKey = set([Const.K_UP, Const.K_DOWN, Const.K_LEFT, Const.K_RIGHT, Const.K_HOME, Const.K_END, Const.K_PAGEDOWN, Const.K_PAGEUP, Const.K_BACKSPACE, Const.K_DELETE, Const.K_INSERT, Const.K_RETURN, Const.K_TAB, Const.K_ESCAPE])
        else:   #pyjs-S onKeyDown keycode 'mod' not in set, due to js/pyjs numeric diff
            self.modKey = set([keycode.valueOf() for keycode in (Const.K_ALT, Const.K_CTRL, Const.K_SHIFT)])
            self.specialKey = set([keycode.valueOf() for keycode in (Const.K_UP, Const.K_DOWN, Const.K_LEFT, Const.K_RIGHT, Const.K_HOME, Const.K_END, Const.K_PAGEDOWN, Const.K_PAGEUP, Const.K_BACKSPACE, Const.K_DELETE, Const.K_INSERT, Const.K_RETURN, Const.K_TAB, Const.K_ESCAPE)])
#Const.K_F1, Const.K_F2, Const.K_F3, Const.K_F4, Const.K_F5, Const.K_F6, Const.K_F7, Const.K_F8, Const.K_F9, Const.K_F10, Const.K_F11, Const.K_F12, Const.K_F13, Const.K_F14, Const.K_F15   #IE keypress keycode: id same as alpha keys
        self.Event = UserEvent
        self._nonimplemented_methods()

    def _lock(self):
        self.queueLock = True

    def _unlock(self):
        self.queueLock = False

    def _updateQueue(self, event):
        if event.type not in self.events:
            return
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
        self._lock()
        if not eventType:
            self.queue = [ JEvent(event) for event in self.eventQueue[0:self.eventNum] ]
            self.eventNum = 0
        else:
            if not isinstance(eventType, (tuple,list)):
                evtType = [et for et in self.eventTypes[eventType]]
            else:
                evtType = [et for t in eventType for et in self.eventTypes[t]]
            queue = []
            self.queue = []
            for i in range(self.eventNum):
                if self.eventQueue[i].type not in evtType:
                    queue.append(self.eventQueue[i])
                else:
                    self.queue.append( JEvent(self.eventQueue[i]) )
            if len(queue) != self.eventNum:
                self.eventNum = len(queue)
                for i in range(self.eventNum):
                    self.eventQueue[i] = queue[i]
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
            evt = JEvent( self.eventQueue.pop(0) )
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
                evt = JEvent( self.eventQueue.pop(0) )
                self.eventNum -= 1
                self.eventQueue.append(None)
                if self.eventNum > 250:
                    self._pump()
                self._unlock()
                return evt
            else:
                self._unlock()
                return None

    def peek(self, eventType):
        """
        Check if an event of given type is present.
        The eventType argument can be a single event type or a list.
        """
        if not self.eventNum:
            return False
        if not isinstance(eventType, (tuple,list)):
            evtType = [et for et in self.eventTypes[eventType]]
        else:
            evtType = [et for t in eventType for et in self.eventTypes[t]]
        self._lock()
        evt = [event.type for event in self.eventQueue[0:self.eventNum]]
        if self.eventNum > 250:
            self._pump()
        self._unlock()
        for et in evtType:
            if et in evt:
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
            if not isinstance(eventType, (tuple,list)):
                evtType = [et for et in self.eventTypes[eventType]]
            else:
                evtType = [et for t in eventType for et in self.eventTypes[t]]
            queue = []
            for i in range(self.eventNum):
                if self.eventQueue[i].type not in evtType:
                    queue.append(self.eventQueue[i])
            if len(queue) != self.eventNum:
                self.eventNum = len(queue)
                for i in range(self.eventNum):
                    self.eventQueue[i] = queue[i]
            if self.eventNum > 250:
                self._pump()
        self._unlock()
        return None

    def event_name(self, eventType):
        """
        Return event name of a event type.
        """
        evtType = self.eventTypes[eventType][0]
        if evtType in self.eventName:
            return self.eventName[evtType]
        else:
            return None

    def set_blocked(self, eventType):
        """
        Block specified event type(s) from queue.
        """
        if eventType is not None:
            if not isinstance(eventType, (tuple,list)):
                evtType = [et for et in self.eventTypes[eventType]]
            else:
                evtType = [et for t in eventType for et in self.eventTypes[t]]
            for et in evtType:
                if et in self.events:
                    self.events.remove(et)
        else:
            for event in self.eventType:
                self.events.add(event)
        return None

    def set_allowed(self, eventType):
        """
        Set allowed event type(s) on queue. 
        """
        if eventType is not None:
            if not isinstance(eventType, (tuple,list)):
                evtType = [et for et in self.eventTypes[eventType]]
            else:
                evtType = [et for t in eventType for et in self.eventTypes[t]]
            for et in evtType:
                self.events.add(et)
        else:
            self.events.clear()
        return None

    def get_blocked(self, eventType):
        """
        Check if specified event type is blocked from queue.
        """
        evtType = [et for et in self.eventTypes[eventType]][0]
        if evtType not in self.events:
            return True
        else:
            return False

    def post(self, event):
        """
        Post event to queue.
        """
        self._lock()
        self._append(event)
        if event.type not in self.events:
            self.eventTypes[event.type] = [event.type]
        self._unlock()
        return None

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

    def __repr__(self):
        """
        Return string representation of Event object.
        """
        return "%s(%s-UserEvent %r)" % (self.__class__, self.type, self.attr)

    def __getattr__(self, attr):
        if attr in self.attr:
            return self.attr[attr]
        else:
            raise AttributeError("'Event' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        raise AttributeError("'Event' object has no attribute '%s'" % attr)


class JEvent(object):

    _mouse_pos = (0, 0)
    _types = {'mousemove':Const.MOUSEMOTION, 'mousedown':Const.MOUSEBUTTONDOWN, 'mouseup':Const.MOUSEBUTTONUP, 'wheel':Const.MOUSEBUTTONDOWN, 'mousewheel':Const.MOUSEBUTTONDOWN, 'DOMMouseScroll':Const.MOUSEBUTTONDOWN, 'keydown':Const.KEYDOWN, 'keypress':Const.KEYDOWN, 'keyup':Const.KEYUP}
    _charCode = {33:Const.K_EXCLAIM, 34:Const.K_QUOTEDBL, 35:Const.K_HASH, 36:Const.K_DOLLAR, 38:Const.K_AMPERSAND, 39:Const.K_QUOTE, 40:Const.K_LEFTPAREN, 41:Const.K_RIGHTPAREN, 42:Const.K_ASTERISK, 43:Const.K_PLUS, 44:Const.K_COMMA, 45:Const.K_MINUS, 46:Const.K_PERIOD, 97:Const.K_a, 98:Const.K_b, 99:Const.K_c, 100:Const.K_d, 101:Const.K_e, 102:Const.K_f, 103:Const.K_g, 104:Const.K_h, 105:Const.K_i, 106:Const.K_j, 107:Const.K_k, 108:Const.K_l, 109:Const.K_m, 110:Const.K_n, 111:Const.K_o, 112:Const.K_p, 113:Const.K_q, 114:Const.K_r, 115:Const.K_s, 116:Const.K_t, 117:Const.K_u, 118:Const.K_v, 119:Const.K_w, 120:Const.K_x, 121:Const.K_y, 122:Const.K_z}

    def __init__(self, event):
        """
        Event object wraps browser event.
        
        Event object attributes:
        
        * type: MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN, KEYUP
        * button: mouse button pressed (1-3, 4-5 V-scroll, and 6-7 H-scroll some browsers)
        * pos: mouse position (x,y)
        * rel: mouse relative position change (x,y)
        * key: keycode of key pressed (K_a-K_z...)
        """
        self.event = event      #__getattr__ not implemented in pyjs -O
        if event.type in ('mousedown', 'mouseup'):
            self.type = self.__class__._types[event.type]
            self.button = event.button + 1
            self.pos = event.pos[0]+env.frame.scrollLeft, event.pos[1]+env.frame.scrollTop
        elif event.type == 'mousemove':
            self.type = self.__class__._types[event.type]
            self.button = event.button + 1
            self.pos = event.pos[0]+env.frame.scrollLeft, event.pos[1]+env.frame.scrollTop
            self.rel = (self.pos[0]-self.__class__._mouse_pos[0], self.pos[1]-self.__class__._mouse_pos[1])
            self.__class__._mouse_pos = self.pos
        elif event.type in ('wheel', 'mousewheel', 'DOMMouseScroll'):
            self.type = self.__class__._types[event.type]
            self.button = event.btn
            self.pos = event.pos[0]+env.frame.scrollLeft, event.pos[1]+env.frame.scrollTop
        elif event.type in ('keydown', 'keyup'):
            self.type = self.__class__._types[event.type]
            self.key = event.keyCode
        elif event.type == 'keypress':
            self.type = self.__class__._types[event.type]
            if event.keyCode:
                code = event.keyCode
            else:
                code = event.which
            if code in self.__class__._charCode:
                self.key = self.__class__._charCode[code]
            else:
                self.key = code
        else:
            self.type = event.type
            for attr in event.attr:
                object.__setattr__(self, attr, event.attr[attr])

    def __repr__(self):
        """
        Return string representation of Event object.
        """
        if hasattr(self.event, 'toString'):
            return "%s(%s)" % (self.__class__, self.event.toString())
        else:      #User Event
            return self.event.__repr__()

    def getEvent(self):
        """
        Return browser event.
        """
        return self.event

