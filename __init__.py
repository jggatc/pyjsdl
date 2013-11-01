#Pyjsdl - Copyright (C) 2013 James Garnon

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#Pyjsdl version 0.17
#Download Site: http://gatc.ca

from display import Display
from surface import Surface
from rect import Rect
from image import Image
from draw import Draw
from event import Event
from key import Key
from mouse import Mouse
from transform import Transform
from surfarray import Surfarray     ###0.16
from time import Time
import util       ###0.17
import mask     ###0.15
import font
import sprite
from locals import *

time = Time()
display = Display()
image = Image()
draw = Draw()
transform = Transform()
surfarray = Surfarray()     ###0.16
event = Event()
mouse = Mouse()
key = Key()

init = lambda:None
quit = lambda:None

class error(RuntimeError):     ###0.16
    pass

