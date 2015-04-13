#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __pyjamas__ import JS
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
        self.time_diff = [0 for i in range(10)]
        self.pos = 0
        self.tick = self._tick_init

    def get_time(self):
        """
        Return time (in ms) between last two calls to tick().
        """
        return self.time_diff[self.pos]

    def _tick_init(self, framerate=0):
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
            if framerate:
                env.canvas.set_timeout( ( 1000/framerate ) - self.time_diff[self.pos] )
        else:
            self.pos = 0
            self.time_diff[self.pos] = time_diff
            self.tick = self._tick
        return self.time_diff[self.pos]

    def _tick(self, framerate=0):
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

