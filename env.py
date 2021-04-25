#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

import os, sys


if os.name != 'pyjs':
    print('Use Pyjs to compile script to a JS app')
    sys.exit()


canvas = None

frame = None

pyjs_mode = None

event = None


def get_canvas():
    """
    Return Canvas object.
    """
    return canvas


def get_frame():
    """
    Return Webpage frame.
    """
    return frame


def get_pyjsmode():
    """
    Return Pyjs mode object.
    """
    return pyjs_mode


def set_env(key, val):
    setattr(sys.modules[__name__], key, val)

