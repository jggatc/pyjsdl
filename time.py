#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __pyjamas__ import JS
import pyjsdl.event
import env

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
        self.time_init = self.time()
        self.time_diff = [33 for i in range(10)]
        self.pos = 0

    def get_time(self):
        """
        Return time (in ms) between last two calls to tick().
        """
        return self.time_diff[self.pos]

    def tick(self, framerate=0):
        """
        Call once per program cycle, returns ms since last call.
        An optional framerate will add pause to limit rate.
        """
        if not env.canvas.time_wait:
            time = self.time()
        else:
            self.time_init += env.canvas.time_wait
            return
        time_diff = time-self.time_init
        self.time_init = time
        if self.pos < 9:
            self.pos += 1
            self.time_diff[self.pos] = time_diff
        else:
            self.pos = 0
            self.time_diff[self.pos] = time_diff
            if framerate:
                env.canvas.set_timeout( ( 1000/framerate ) - ( sum(self.time_diff)/10 ) )
        return self.time_diff[self.pos]

    def tick_busy_loop(self, framerate=0):
        """
        Calls tick() with optional framerate.
        Returns ms since last call.
        """
        time_diff = self.tick(framerate)
        return time_diff

    def get_fps(self):
        """
        Return fps.
        """
        return 1000/(sum(self.time_diff)/10)

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
            env.canvas.set_timeWait(time)
            self.timeout(time, self)
        else:
            env.canvas.set_timeWait(time)

    def set_timer(self, eventid, time):
        """
        **pyjsdl.time.set_timer**

        Events of type eventid placed on queue at time (ms) intervals.
        Disable by time of 0.
        """
        if eventid not in _EventTimer.timers:
            _EventTimer.timers[eventid] = _EventTimer(eventid)
        if time:
            _EventTimer.timers[eventid].start(time)
        else:
            _EventTimer.timers[eventid].cancel()

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
        self.eventid = eventid
        self.time = 0
        self.timer = None
        self.repeat = True

    def run(self):
        pyjsdl.event.post( pyjsdl.event.Event(self.eventid) )
        if self.repeat:
            self.timeout()

    def timeout(self):
        timer = JS("""$wnd['setTimeout'](function() {@{{self}}['run']();}, @{{self}}['time']);""") #Time.timeout
        self.timer = timer

    def start(self, time):
        if self.timer:
            self.cancel()
        self.time = time
        self.repeat = True
        self.timeout()

    def cancel(self):
        if self.timer:
            JS("""$wnd['clearTimeout'](@{{self}}['timer']);""")
            self.timer = None
        self.repeat = False

