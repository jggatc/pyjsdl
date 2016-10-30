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
#Pyjsdl version 0.21
#Project Site: http://gatc.ca/

from pyjsdl import util
from pyjsdl.display import Display
from pyjsdl.surface import Surface
from pyjsdl.rect import Rect
from pyjsdl.image import Image
from pyjsdl.draw import Draw
from pyjsdl.event import Event
from pyjsdl.key import Key
from pyjsdl.mouse import Mouse
from pyjsdl.transform import Transform
from pyjsdl.surfarray import Surfarray
from pyjsdl.color import Color
from pyjsdl.mixer import Mixer
from pyjsdl.time import Time
from pyjsdl import mask
from pyjsdl import font
from pyjsdl import sprite
from pyjsdl import cursors
from pyjsdl.locals import *

time = Time()
display = Display()
image = Image()
draw = Draw()
transform = Transform()
surfarray = Surfarray()
mixer = Mixer()
event = Event()
mouse = Mouse()
key = Key()

init = lambda:None

def quit():
    canvas = display.get_canvas()
    canvas.stop()

class error(RuntimeError):
    pass

