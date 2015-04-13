#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from pyjamas import DOM
from pyjamas import Window
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.FocusPanel import FocusPanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.Canvas.Color import Color
from pyjamas.Canvas.ImageLoader import loadImages
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui import Event
from pyjamas.ui.MouseListener import MouseWheelHandler
from pyjamas.Canvas.HTML5Canvas import HTML5Canvas
from pyjamas.media.Audio import Audio
from __pyjamas__ import JS


def eventGetMouseWheelVelocityY(evt):
    #code from pyjs
    JS("""
    return Math['round'](-@{{evt}}['wheelDelta'] / 40) || 0;
    """)

