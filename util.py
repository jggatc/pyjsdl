#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl.time import Time
from pyjsdl.rect import Rect
from pyjsdl import env
from __pyjamas__ import JS


class Timer(object):
    """
    Simple profiling timer.
    Output log can be directed to 'console' or to 'textarea'.
    If output is to textarea, may specify log length.
    """

    def __init__(self, log='console', log_length=5):
        self.time = Time()
        self.time_i = self.get_time()
        self.dtime = []
        self.number = 0
        self.log = None
        self.log_list = None
        self.log_num = 0
        self.log_scroll = True
        self.set_log(log, log_length)

    def get_time(self):
        """
        Get current time.
        """
        return self.time.time()

    def set_time(self):
        """
        Set current time.
        """
        self.time_i = self.get_time()

    def lap_time(self, time_i=None, time_f=None, number=100, print_result=True):
        """
        Time lapsed since previous set_time.
        Optional arguments time_i and time_f, number of calls to average, and print_results to output result.
        """
        if time_i is None:
            time_i = self.time_i
        if time_f is None:
            time_f = self.get_time()
        self.dtime.append(time_f-time_i)
        self.number += 1
        if self.number >= number:
            t_ave = ( sum(self.dtime)/number )
            self.dtime = []
            self.number = 0
            if print_result:
                if self.log_type == 'console':
                    self.log_num += 1
                    entry = "Time %d: %s" % (self.log_num, t_ave)
                    print(entry)
                else:
                    self.log_num += 1
                    entry = "Time %d: %s" % (self.log_num, t_ave)
                    self.print_log(entry)
            return t_ave

    def set_log(self, log, log_length=5):
        """
        Set log output.
        Argument log can be 'console' or 'textarea'.
        """
        if log in ('console','textarea'):
            self.log_type = log
            if log == 'textarea':
                if not self.log:
                    size = env.canvas.surface.width-5, 102
                    self.log = env.canvas.surface._display.Textarea(size)
                    self.log.setReadonly(True)
                    self.log.addMouseListener(self)
                    self.onMouseUp = lambda sender,x,y: None
                    self.onMouseMove = lambda sender,x,y: None
                    self.onMouseEnter = lambda sender: None
                    self.log_list = ['' for i in range(log_length)]
                self.log.toggle(True)
            else:
                if self.log:
                    self.log.toggle(False)
                    self.log_list = []

    def onMouseDown(self, sender, x, y):
        self.log_scroll = False

    def onMouseLeave(self, sender):
        self.log_scroll = True

    def print_log(self, text):
        """
        Print text to output.
        """
        if self.log_type == 'console':
            print(text)
        else:
            self.log_list.pop(0)
            self.log_list.append(text+'\n')
            text = ''.join(self.log_list)
            self.log.setText(text)
            if self.log_scroll:
                self.log.setCursorPos(len(text))


class PyjsMode:
    """
    Check Pyjs mode used to compile application.
    Attributes:
        strict/optimized to specify mode
        getattr_call/eq_call to specify functionality
    """
    def __init__(self):
        self.getattr_call = self.test_getattr()
        self.eq_call = self.test_eq()
        self.strict, self.optimized = self.test_mode()

    def test_mode(self):
        """
        Test if build mode is strict or optimized.
        """
        if self.getattr_call and self.eq_call:
            return True, False
        else:
            return False, True

    def test_getattr(self):
        """
        Test if object __getattr__ method is called.
        """
        return (Rect(0,0,20,20).center == (10,10))

    def test_eq(self):
        """
        Test if object __eq__ method is called.
        """
        return (Rect(0,0,20,20) == Rect(0,0,20,20))

env.set_env('pyjs_mode', PyjsMode())


def call(obj, func, args=()):
    """
    Call unbound method.
    Argument obj is the object, func is the unbound method, and optional args is a tuple of arguments for the method.
    Returns the method's return value.
    """
    return JS("@{{func}}.apply(@{{obj}}, @{{args}}['getArray']());")


#code modified from pyjs
class _dict(dict):

    def values(self):
        return dict.values(self).__iter__()

    def keys(self):
        return dict.__iter__(self)

    def items(self):
        return dict.items(self).__iter__()


def _next(obj):
    return obj.next()


try:
    _range = xrange
except NameError:
    _range = range

