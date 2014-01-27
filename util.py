#Pyjsdl - Copyright (C) 2013 James Garnon

from time import Time
from pyjamas import logging
from __pyjamas__ import JS      ###0.17


class Timer(object):

    def __init__(self):
        self.time = Time()
        self.time_i = self.get_time()
        self.dtime = []
        self.number = 0
        self.log = logging.getConsoleLogger()
        self.log_type = 'print'

    def get_time(self):
        return self.time.time()

    def set_time(self):
        self.time_i = self.get_time()

    def lap_time(self, time_i=None, time_f=None, number=100, print_result=True):
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
                if self.log_type == 'print':
                    print "Time:%s" % t_ave
                else:
                    self.print_log(t_ave)
            return t_ave

    def set_log(self, log):
        if log in ('print','log'):
            self.log_type = log 

    def print_log(self, var):
        self.log.info("Time:%s", var)


class Pyjs_Mode:    #0.18
    """
    Check Pyjs mode used to compile application.
    Attributes included strict or optimized to specifying mode.
    """

    def __init__(self):
        self.strict, self.optimized = self._setmode()

    def __getattr__(self, attr):
        if attr == '__strict_mode':
            return True

    def _setmode(self):
        if self.__strict_mode == True:
            return True, False
        else:
            return False, True


def call(obj, func, args=()):      ###0.17
    """
    Call unbound method.
    Argument obj is the object, func is the unbound method, and optional args is a tuple of arguments for the method.
    Returns the method's return value.
    """
    return JS("""@{{func}}.apply(@{{obj}}, @{{args}}['getArray']());""")

