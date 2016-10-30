#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

import pyjsdl.event
from pyjsdl import env
from __pyjamas__ import JS

__docformat__ = 'restructuredtext'


class Clock(object):
    """
    **pyjsdl.time.Clock**
    
    * Clock.get_time
    * Clock.tick
    * Clock.tick_busy_loop
    * Clock.get_fps
    """

    def __init__(self):
        """
        Return Clock.
        """
        self._time = self.time()
        self._time_init = self._time
        self._time_diff = [33 for i in range(10)]
        self._pos = 0
        self._framerate = 0

    def get_time(self):
        """
        Return time (in ms) between last two calls to tick().
        """
        return self._time_diff[self._pos]

    def tick(self, framerate=0):
        """
        Call once per program cycle, returns ms since last call.
        An optional framerate will add pause to limit rate.
        """
        if self._pos:
            self._pos -= 1
        else:
            self._pos = 9
            if self._framerate != framerate:
                self._framerate = framerate
                env.canvas._framerate = 1000/framerate
        self._time = self.time()
        self._time_diff[self._pos] = self._time-self._time_init
        self._time_init = self._time
        return self._time_diff[self._pos]

    def tick_busy_loop(self, framerate=0):
        """
        Calls tick() with optional framerate.
        Returns ms since last call.
        """
        return self.tick(framerate)

    def get_fps(self):
        """
        Return fps.
        """
        return 1000/(sum(self._time_diff)/10)

    def time(self):
        """
        **pyjsdl.time.time**
        
        Return current computer time (in ms).
        """
        ctime = JS("new Date()")
        return ctime.getTime()


class Time(object):

    def __init__(self):
        self._time_init = self.time()
        self.run = lambda: self.wait()
        self.framerate = None
        self.Clock = Clock

    def get_ticks(self):
        """
        **pyjsdl.time.get_ticks**
        
        Return ms since program start.
        """
        return self.time() - self._time_init

    def delay(self, time):
        """
        **pyjsdl.time.delay**
        
        Pause for given time (in ms). Return ms paused.
        """
        start = self.time()
        while self.time() - start < time:   #Use Timer
            pass
        return self.time() - start

    def wait(self, time=0):
        """
        **pyjsdl.time.wait**
        
        Timeout program main loop for given time (in ms).
        """
        if time:
            if self.framerate is None:
                self.framerate = env.canvas._framerate
                env.canvas._framerate = time*10
                self.timeout(time, self)
        else:
            if self.framerate is not None:
                env.canvas._framerate = self.framerate
                self.framerate = None

    def set_timer(self, eventid, time):
        """
        **pyjsdl.time.set_timer**

        Events of type eventid placed on queue at time (ms) intervals.
        Disable by time of 0.
        """
        if eventid not in _EventTimer.timers:
            _EventTimer.timers[eventid] = _EventTimer(eventid)
        _EventTimer.timers[eventid].set_timer(time)

    def time(self):
        """
        **pyjsdl.time.time**
        
        Return current computer time (in ms).
        """
        ctime = JS("new Date()")
        return ctime.getTime()

    def timeout(self, time=None, obj=None):
        #Timer.schedule with callback Canvas self.run - 'TypeError: self is undefined'
        """
        Timeout time (in ms) before triggering obj.run method.
        Code modified from pyjs.
        """
        run = lambda: obj.run()
        JS("""$wnd['setTimeout'](function() {@{{run}}();}, @{{time}});""")


class _EventTimer:
    timers = {}

    def __init__(self, eventid):
        self.event = pyjsdl.event.Event(eventid)
        self.timer = None
        self.time = 0
        self.repeat = True

    def set_timer(self, time):
        if self.timer:
            self.repeat = False
            self.clearTimeout()
        if time:
            self.time = time
            self.repeat = True
            self.setTimeout()

    def setTimeout(self):
        #Time.timeout
        timer = JS("""$wnd['setTimeout'](function() {@{{self}}['run']();}, @{{self}}['time']);""")
        self.timer = timer

    def clearTimeout(self):
        JS("""$wnd['clearTimeout'](@{{self}}['timer']);""")
        self.timer = None

    def run(self):
        pyjsdl.event.post(self.event)
        if self.repeat:
            self.setTimeout()

