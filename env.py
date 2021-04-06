#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>


canvas = None

frame = None

event = None

pyjs_mode = None


def set_env(key, val):
    global canvas, frame, event, pyjs_mode
    if key == 'canvas':
        canvas = val
    elif key == 'frame':
        frame = val
    elif key == 'event':
        event = val
    elif key == 'pyjs_mode':
        pyjs_mode = val

