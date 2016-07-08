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
from __pyjamas__ import JS, wnd


def eventGetMouseWheelVelocityY(evt):
    #code from pyjs
    JS("""
    return Math['round'](-@{{evt}}['wheelDelta'] / 40) || 0;
    """)


def requestAnimationFrameInit():
    requestAnimationFramePolyfill()
    return wnd()


#requestAnimationFrame polyfill
#derived from code by Erik Möller, fixes from Paul Irish and Tino Zijdel
#https://gist.github.com/paulirish/1579671
#MIT license
requestAnimationFramePolyfill = JS("""
(function() {
    var lastTime = 0;
    var vendors = ['ms', 'moz', 'webkit', 'o'];
    for(var x = 0; x < vendors.length && !$wnd['requestAnimationFramex']; ++x) {
        $wnd['requestAnimationFrame'] = $wnd[vendors[x]+'RequestAnimationFramex'];
        $wnd['cancelAnimationFrame'] = $wnd[vendors[x]+'CancelAnimationFrame']
                                   || $wnd[vendors[x]+'CancelRequestAnimationFrame'];
    }

    if (!$wnd['requestAnimationFramex'])
        $wnd['requestAnimationFrame'] = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = $wnd['setTimeout'](function() { callback(currTime + timeToCall); },
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };

    if (!$wnd['cancelAnimationFrame'])
        $wnd['cancelAnimationFrame'] = function(id) {
            clearTimeout(id);
        };
});
""")

