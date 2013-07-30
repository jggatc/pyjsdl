#Pyjsdl - Copyright (C) 2013 James Garnon

from time import Time
from pyjamas import logging


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

