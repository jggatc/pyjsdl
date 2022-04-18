#Pyjsdl - Python-to-JavaScript Multimedia Framework
#Copyright (c) 2013 James Garnon
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
#
#Pyjsdl version 0.26
#Project Site: https://gatc.ca/

from pyjsdl import env
from pyjsdl import util
from pyjsdl.display import Display
from pyjsdl.surface import Surface
from pyjsdl.rect import Rect
from pyjsdl.image import Image
from pyjsdl.event import Event
from pyjsdl.key import Key
from pyjsdl.mouse import Mouse
from pyjsdl.color import Color
from pyjsdl.mixer import Mixer
from pyjsdl.time import Time
from pyjsdl.vector import Vector2
from pyjsdl import draw
from pyjsdl import transform
from pyjsdl import surface
from pyjsdl import surfarray
from pyjsdl import mask
from pyjsdl import font
from pyjsdl import sprite
from pyjsdl import cursors
from pyjsdl.constants import *


_initialized = False

def init():
    """
    Initialize module.
    """
    global time, display, image, event, key, mouse, mixer, _initialized
    if _initialized:
        return
    else:
        _initialized = True
    event = Event()
    env.set_env('event', event)
    time = Time()
    display = Display()
    image = Image()
    mixer = Mixer()
    mouse = Mouse()
    key = Key()

init()


def setup(callback, images=None):
    """
    Initialize module for script execution.
    Argument include callback function to run and optional images list to preload.
    Callback function can also be an object with a run method to call.
    The images can be image URL, or file-like object or base64 data in format (name.ext,data).
    """
    display.setup(callback, images)


def set_callback(callback):
    """
    Set callback function.
    Argument callback function to run.
    Callback function can also be an object with a run method to call.
    """
    display.set_callback(callback)


def setup_images(images):
    """
    Add images to image preload list.
    The argument is an image or list of images representing an image URL, or file-like object or base64 data in format (name.ext,data).
    Image preloading occurs at setup call.
    """
    display.set_images(images)


def quit():
    """
    Terminates canvas repaint and callback function.
    """
    canvas = display.get_canvas()
    canvas.stop()
    mixer.quit()
    time._stop_timers()


class error(RuntimeError):
    pass


def bounding_rect_return(setting):
    """
    Set whether blit/draw return bounding Rect.
    Setting (bool) defaults to True on module initialization.
    """
    surface.bounding_rect_return(setting)
    draw.bounding_rect_return(setting)

