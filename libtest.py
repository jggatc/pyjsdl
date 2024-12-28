#!/usr/bin/env python

"""
Libtest

Check doc/libtest.txt for information.


tests = ['surface_test',
         'rect_test',
         'draw_test',
         'transform_test',
         'surfarray_test',
         'mask_test',
         'color_test',
         'cursor_test',
         'sprite_test',
         'event_test',
         'time_test',
         'vector_test']
"""


tests = []    #test specific module if added to tests list, default all tests
catch_exception = True    #exception in test caught, set to False to raise exception


import sys
sys.dont_write_bytecode = True

from test import libtest

libtest.main(tests, catch_exception)

