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

from display import Display
from surface import Surface
from rect import Rect
from image import Image
from draw import Draw
from event import Event
from key import Key
from mouse import Mouse
from transform import Transform
from surfarray import Surfarray
from color import Color
from mixer import Mixer
from time import Time
import util
import mask
import font
import sprite
from locals import *

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

