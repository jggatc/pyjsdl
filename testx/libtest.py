#Libtest

#check doc/libtest.txt for information


platform = None

# __pragma__ ('skip')

import os, sys

if os.name in ('posix', 'nt', 'os2', 'ce', 'riscos'):
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame as pg
    platform = 'pc'
    executor = 'python'
    library = 'pygame'
elif os.name == 'java':
    import pyj2d as pg
    platform = 'jvm'
    executor = 'jython'
    library = 'pyj2d'
else:
    import pyjsdl as pg
    platform = 'js'
    executor = 'pyjs'
    library = 'pyjsdl'

# __pragma__ ('noskip')

if platform is None:
    # '__pragma__' statements declare ts options
    import pyjsdl as pg
    platform = 'js'
    executor = 'transcrypt'
    library = 'pyjsdl-ts'

from test import surface_test
from test import rect_test
from test import draw_test
from test import transform_test
from test import surfarray_test
from test import mask_test
from test import color_test
from test import cursor_test
from test import sprite_test
from test import event_test
from test import time_test
from test import vector_test


if executor in ('python', 'jython', 'pyjs'):
    has_assert = True
    if hasattr('', 'format'):
        _name = lambda f: f.__name__
        _str = lambda n, t, r: 'Test {}  {} {}'.format(n, _name(t), r)
    else:
        _name = lambda f: f.__name__
        _str = lambda n, t, r: 'Test %3d  %-30s %10s' % (n, _name(t), r)
elif executor == 'transcrypt':
    try:
        assert False
        has_assert = False
    except AssertionError:
        has_assert = True
    # __pragma__ ('noalias', 'name')
    _name = lambda f: f.name
    _str = lambda n, t, r: 'Test {}  {} {}'.format(n, _name(t), r)


def set_pyjsmode():
    #pyjsbuild -S: opt=False/attr=True
    #pyjsbuild -O: opt=True/attr=False
    #pyjsbuild -O descriptor-proto/operator-funcs: opt=True/attr=True
    if executor == 'pyjs':
        pyjs_opt = pg.env.pyjs_mode.optimized
        pyjs_attr = pg.env.pyjs_mode.getattr_call
    else:
        pyjs_opt = False
        pyjs_attr = True
    return pyjs_opt, pyjs_attr


class Log:

    def __init__(self):
        self._log = self._set_log()
        self._log_text = []

    def write(self, text):
        if self._log:
            self._log_text.append(text + '\n')
            self._log.setText(''.join(self._log_text))
        else:
            print(text)

    def _set_log(self):
        if platform == 'js':
            try:
                pg.display.textbox_init()
                log = pg.display.textarea
                log.resize(400, 500)
                log.toggle()
            except:
                log = None
        else:
            log = None
        return log


lib_tests = [surface_test,
             rect_test,
             draw_test,
             transform_test,
             surfarray_test,
             mask_test,
             color_test,
             cursor_test,
             sprite_test,
             event_test,
             time_test,
             vector_test]


env = {}
log = None
tests = []
test_num = -1
tests_failed = []
tests_success = True
tests_skipped = False
test_repeat = False
catch_exc = False


def tests_init():
    global log
    pg.init()
    width, height = 20,20
    display = pg.display.set_mode((width, height))
    surface = pg.Surface((width, height))
    pyjs_opt, pyjs_attr = set_pyjsmode()
    log = Log()
    env['pg'] = pg
    env['platform'] = platform
    env['executor'] = executor
    env['library'] = library
    env['log'] = log
    env['pyjs_opt'] = pyjs_opt
    env['pyjs_attr'] = pyjs_attr
    env['display'] = display
    env['surface'] = surface
    env['width'] = width
    env['height'] = height
    for tst in lib_tests:
        test_list = tst.init(env)
        tests.extend(test_list)


def run_test():
    global tests_success, tests_failed, tests_skipped, test_repeat
    result = 'passed'
    try:
        ret = tests[test_num]()
        if ret is not None:
            if ret:
                test_repeat = True
                return
            else:
                test_repeat = False
    except AssertionError:
        result = 'failed'
        tests_success = False
        test_repeat = False
        tests_failed.append(test_num)
    except NotImplementedError:
        result = 'skipped'
        tests_skipped = True
        test_repeat = False
    except:
        result = 'error'
        tests_success = False
        test_repeat = False
        if test_num not in tests_failed:
            tests_failed.append(test_num)
        if not catch_exc:
            log.write(_str(test_num, tests[test_num], result))
            raise
    log.write(_str(test_num, tests[test_num], result))


def run_tests():
    global test_num
    while True:
        if test_num < len(tests)-1:
            test_num += 1
            run_test()
        else:
            break
    test_complete()


def run_tests_js():
    global test_num
    if test_num < len(tests)-1:
        if not test_repeat:
            test_num += 1
        run_test()
    else:
        test_complete()


def test_complete():
    if tests_success:
        log.write('Tests passed.')
    else:
        log.write('Tests that failed: ' + str(tests_failed))
    if not tests_success or tests_skipped:
        log.write('\nCheck doc/libtest.txt for information.')
    pg.quit()


def main():
    tests_init()
    if env['platform'] in ('pc', 'jvm'):
        run_tests()
    else:
        if has_assert:
            pg.setup(run_tests_js)
        else:
            log.write('\nCheck doc/libtest.txt for information.')


if __name__ == '__main__':
    main()

