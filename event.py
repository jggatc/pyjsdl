#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
import env
import time
import locals as Const

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
        Maintain events received from JVM.
        
        Module initialization creates pyjsdl.event instance.
        """
        self.eventQueue = [None for i in range(256)]      #max 256: Error: Event queue full
#        self.eventQueue = [None] * 256      #pyjs -O TypeError
        self.eventNum = 0
        self.eventQueueTmp = [None for i in range(256)]   #used when main queue is locked
#        self.eventQueueTmp = [None] * 256   #pyjs -O TypeError
        self.eventNumTmp = 0
        self.eventAllowed = []
        self.eventBlocked = []
        self.queueLock = False
        self.queueAccess = False
        self.queue = []
        self.mousePress = {0:False, 1:False, 2:False}
        self.mouseMove = {'x':-1, 'y':-1}
        self.mouseMoveRel = {'x':None, 'y':None}
        self.keyPress = {Const.K_ALT:False, Const.K_CTRL:False, Const.K_SHIFT:False}
        self.keyMod = {Const.K_ALT:{True:Const.KMOD_ALT,False:0}, Const.K_CTRL:{True:Const.KMOD_CTRL,False:0}, Const.K_SHIFT:{True:Const.KMOD_SHIFT,False:0}}
        self.mouseCursor = True
        self.timer = time.Clock()
        self.eventName = {'mousemove':'MouseMotion', 'mousedown':'MouseButtonDown', 'mouseup':'MouseButtonUp', 'keydown':'KeyDown', 'keyup':'KeyUp'}
        self.eventType = ['mousemove', 'mousedown', 'mouseup', 'keydown', 'keypress', 'keyup']
        self.events = ['mousemove', 'mousedown', 'mouseup', 'keydown', 'keypress', 'keyup']
        self.eventTypes = {Const.MOUSEMOTION:['mousemove'], Const.MOUSEBUTTONDOWN:['mousedown'], Const.MOUSEBUTTONUP:['mouseup'], Const.KEYDOWN:['keydown','keypress'], Const.KEYUP:['keyup']}
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
        try:
            self.eventQueue[self.eventNum] = event
            self.eventNum += 1
        except IndexError:
            pass

    def _appendTmp(self, event):
        try:
            self.eventQueueTmp[self.eventNumTmp] = event
            self.eventNumTmp += 1
        except IndexError:
            pass

    def _appendMerge(self):
        for i in range(self.eventNumTmp):
            self._append( self.eventQueueTmp[i] )
            self.eventQueueTmp[i] = None
        self.eventNumTmp = 0

    def pump(self):
        """
        Reset event queue.
        """
        self._lock()
        self.eventNum = 0
        self._unlock()
        return None

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
                eventType = [eventType]
            eventType = [et for t in eventType for et in self.eventTypes[t]]
            queue = []
            self.queue = []
            for i in range(self.eventNum):
                if self.eventQueue[i].type not in eventType:
                    queue.append(self.eventQueue[i])
                else:
                    self.queue.append( JEvent(self.eventQueue[i]) )
            if len(queue) != self.eventNum:
                self.eventNum = len(queue)
                for i in range(self.eventNum):
                    self.eventQueue[i] = queue[i]
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
            eventType = [eventType]
        eventType = [et for t in eventType for et in self.eventTypes[t]]
        self._lock()
        evt = [event.type for event in self.eventQueue[0:self.eventNum]]
        self._unlock()
        for evtType in eventType:
            if evtType in evt:
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
                eventType = [eventType]
            eventType = [et for t in eventType for et in self.eventTypes[t]]
            queue = []
            for i in range(self.eventNum):
                if self.eventQueue[i].type not in eventType:
                    queue.append(self.eventQueue[i])
            if len(queue) != self.eventNum:
                self.eventNum = len(queue)
                for i in range(self.eventNum):
                    self.eventQueue[i] = queue[i]
        self._unlock()
        return None

    def event_name(self, eventType):
        """
        Return event name of a event type.
        """
        try:
            return self.eventName[self.eventTypes[eventType][0]]
        except KeyError:
            return None

    def set_blocked(self, eventType):
        """
        Block specified event type(s) from queue.
        """
        if eventType is not None:
            if not isinstance(eventType, (tuple,list)):
                eventType = [eventType]
            eventType = [et for t in eventType for et in self.eventTypes[t]]
            for evtType in eventType:
                try:
                    self.events.remove(evtType)
                except ValueError:
                    pass
        else:
            self.events = self.eventType[:]
        return None

    def set_allowed(self, eventType):
        """
        Set allowed event type(s) on queue. 
        """
        if eventType is not None:
            if not isinstance(eventType, (tuple,list)):
                eventType = [eventType]
            eventType = [et for t in eventType for et in self.eventTypes[t]]
            for evtType in eventType:
                if evtType not in self.events:
                    self.events.append(evtType)
        else:
            self.events = []
        return None

    def get_blocked(self, eventType):
        """
        Check if specified event type is blocked from queue.
        """
        eventType = [et for et in self.eventTypes[eventType]][0]
        if eventType not in self.events:
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
            self.events.append(event.type)
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

    def __setattr__(self, attr, value):
        raise AttributeError, ("'Event' object has no attribute '%s'" % attr)


class JEvent(object):

    _mouse_pos = (0, 0)
    _types = {'mousemove':Const.MOUSEMOTION, 'mousedown':Const.MOUSEBUTTONDOWN, 'mouseup':Const.MOUSEBUTTONUP, 'keydown':Const.KEYDOWN, 'keypress':Const.KEYDOWN, 'keyup':Const.KEYUP}
    _charCode = {33:Const.K_EXCLAIM, 34:Const.K_QUOTEDBL, 35:Const.K_HASH, 36:Const.K_DOLLAR, 38:Const.K_AMPERSAND, 39:Const.K_QUOTE, 40:Const.K_LEFTPAREN, 41:Const.K_RIGHTPAREN, 42:Const.K_ASTERISK, 43:Const.K_PLUS, 44:Const.K_COMMA, 45:Const.K_MINUS, 46:Const.K_PERIOD, 97:Const.K_a, 98:Const.K_b, 99:Const.K_c, 100:Const.K_d, 101:Const.K_e, 102:Const.K_f, 103:Const.K_g, 104:Const.K_h, 105:Const.K_i, 106:Const.K_j, 107:Const.K_k, 108:Const.K_l, 109:Const.K_m, 110:Const.K_n, 111:Const.K_o, 112:Const.K_p, 113:Const.K_q, 114:Const.K_r, 115:Const.K_s, 116:Const.K_t, 117:Const.K_u, 118:Const.K_v, 119:Const.K_w, 120:Const.K_x, 121:Const.K_y, 122:Const.K_z}

    def __init__(self, event):
        """
        Event object wraps JavaScript event, created when retrieving events from queue.
        
        Event object attributes:
        
        * type: MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN, KEYUP
        * button: mouse button pressed (1/2/3)
        * pos: mouse position (x,y)
        * rel: mouse relative position change (x,y)
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
        elif event.type in ('keydown', 'keyup'):
            self.type = self.__class__._types[event.type]
            self.key = event.keyCode
        elif event.type == 'keypress':
            self.type = self.__class__._types[event.type]
            if event.keyCode:
                code = event.keyCode
            else:
                code = event.which
            try:
                self.key = self.__class__._charCode[code]
            except KeyError:
                self.key = code
        else:
            self.type = event.type
            for attr in event.attr:
                object.__setattr__(self, attr, event.attr[attr])

    def __repr__(self):
        """
        Return string representation of Event object.
        """
        try:
            return "%s(%s)" % (self.__class__, self.event.toString())
        except AttributeError:      #User Event
            return self.event.__repr__()

    def getEvent(self):
        """
        Return JavaScript event.
        """
        return self.event

