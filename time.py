#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from pyjsdl import env
from pyjsdl.pyjsobj import performanceNowInit
try:
    from __pyjamas__ import JS
except ImportError:
    pass

__docformat__ = 'restructuredtext'


class Clock(object):
    """
    **pyjsdl.time.Clock**
    
    * Clock.get_time
    * Clock.tick
    * Clock.tick_busy_loop
    * Clock.get_fps
    """

    _wnd = None

    def __init__(self):
        self._time = self.time()
        self._time_init = self._time
        self._time_diff = 0
        self._framerate = 0

    def get_time(self):
        """
        Return time (in ms) between last two calls to tick().
        """
        return self._time_diff

    def tick(self, framerate=0):
        """
        Call once per program cycle, returns ms since last call.
        An optional framerate will add pause to limit rate.
        """
        if self._framerate != framerate and not env.canvas._pause:
            self._framerate = framerate
            if framerate:
                env.canvas._framerate = 1000/framerate
            else:
                env.canvas._framerate = 0
        self._time = self.time()
        self._time_diff = self._time-self._time_init
        self._time_init = self._time
        return self._time_diff

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
        if not env.canvas._pause:
            return 1000/env.canvas._frametime
        else:
            return 0.0

    def time(self):
        """
        **pyjsdl.time.time**
        
        Return system time (in ms).
        """
        return self._wnd.performance.now()


class Time(object):

    _wnd = None

    def __init__(self):
        self.Clock = Clock
        Time._wnd = performanceNowInit()
        Clock._wnd = Time._wnd
        self._time_init = self.time()
        self._framerate = 0
        self.run = lambda: self.wait()

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
        Suspends the program, preferably use time.wait.
        """
        start = self.time()
        while True:
            if self.time() - start > time:
                return self.time() - start

    def wait(self, time=0):
        """
        **pyjsdl.time.wait**
        
        Timeout program callback for given time (in ms).
        """
        if time:
            if not env.canvas._pause:
                self._framerate = env.canvas._framerate
                env.canvas._framerate = time*10
                env.canvas._pause = True
                self.timeout(time, self)
        else:
            if env.canvas._pause:
                env.canvas._framerate = self._framerate
                env.canvas._rendertime = self.time()
                env.canvas._pause = False
        return time

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
        
        Return system time (in ms).
        """
        return self._wnd.performance.now()

    def timeout(self, time=None, obj=None):
        """
        Timeout time (in ms) before triggering obj.run method.
        """
        #code modified from pyjs
        run = lambda: obj.run()
        JS("$wnd['setTimeout'](function() {@{{run}}();}, @{{time}});")


class _EventTimer:
    timers = {}

    def __init__(self, eventid):
        self.event = env.event.Event(eventid)
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
        timer = JS("$wnd['setTimeout'](function() {@{{self}}['run']();}, @{{self}}['time']);")
        self.timer = timer

    def clearTimeout(self):
        JS("$wnd['clearTimeout'](@{{self}}['timer']);")
        self.timer = None

    def run(self):
        env.event.post(self.event)
        if self.repeat:
            self.setTimeout()

