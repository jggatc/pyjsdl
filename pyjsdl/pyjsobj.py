#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjamas import DOM
from pyjamas import Window
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.FocusPanel import SimplePanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.Canvas.Color import Color
from pyjamas.Canvas.ImageLoader import loadImages
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui import Event
from pyjamas.Canvas.HTML5Canvas import HTML5Canvas as _HTML5Canvas
from pyjamas.media.Audio import Audio
from __pyjamas__ import JS, wnd


class MouseWheelHandler(object):

    _listener = {}

    def __init__(self):
        element = self.getElement()
        if hasattr(element, 'onwheel'):
            self._mousewheel = 'wheel'
        elif hasattr(element, 'onmousewheel'):
            self._mousewheel = 'mousewheel'
        else:
            self._mousewheel = 'DOMMouseScroll'

    def addMouseWheelListener(self):
        element = self.getElement()
        listener = lambda event: self.onMouseWheel(event)
        self._listener[self] = listener
        element.addEventListener(self._mousewheel, listener)

    def removeMouseWheelListener(self):
        element = self.getElement()
        listener = self._listener[self]
        del self._listener[self]
        element.removeEventListener(self._mousewheel, listener)

    def onMouseWheel(self, event):
        pass


class HTML5Canvas(_HTML5Canvas, MouseWheelHandler):

    def __init__(self, coordX, coordY, *args, **kwargs):
        _HTML5Canvas.__init__(self, coordX, coordY, *args, **kwargs)
        MouseWheelHandler.__init__(self)

    def addMouseListener(self, listener):
        _HTML5Canvas.addMouseListener(self, listener)
        self.addMouseWheelListener()

    def addKeyEventListener(self, obj):
        element = obj.getElement()
        element.setAttribute('tabindex','0')
        listener = lambda event: self.onKeyEvent(event)
        _listener[self] = listener
        element.addEventListener('keydown', listener)

    def removeKeyEventListener(self, obj):
        element = obj.getElement()
        listener = _listener[self]
        del _listener[self]
        element.removeEventListener('keydown', listener)


_listener = {}


def requestAnimationFrameInit():
    requestAnimationFramePolyfill()
    return wnd()


def performanceNowInit():
    performanceNowPolyfill()
    return wnd()


def requestAnimationFramePolyfill():
    JS(
"""
// http://paulirish.com/2011/requestanimationframe-for-smart-animating/
// http://my.opera.com/emoller/blog/2011/12/20/requestanimationframe-for-smart-er-animating

// requestAnimationFrame polyfill by Erik Möller. fixes from Paul Irish and Tino Zijdel

// MIT license

(function() {
    var lastTime = 0;
    var vendors = ['ms', 'moz', 'webkit', 'o'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x]+'CancelAnimationFrame'] 
                                   || window[vendors[x]+'CancelRequestAnimationFrame'];
    }
 
    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); }, 
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };
 
    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}());
"""
    )


def performanceNowPolyfill():
    JS(
"""
// @license http://opensource.org/licenses/MIT
// copyright Paul Irish 2015


// Date.now() is supported everywhere except IE8. For IE8 we use the Date.now polyfill
//   github.com/Financial-Times/polyfill-service/blob/master/polyfills/Date.now/polyfill.js
// as Safari 6 doesn't have support for NavigationTiming, we use a Date.now() timestamp for relative values

// if you want values similar to what you'd get with real perf.now, place this towards the head of the page
// but in reality, you're just getting the delta between now() calls, so it's not terribly important where it's placed


(function(){

  if ("performance" in window == false) {
      window.performance = {};
  }
  
  Date.now = (Date.now || function () {  // thanks IE8
	  return new Date().getTime();
  });

  if ("now" in window.performance == false){
    
    var nowOffset = Date.now();
    
    if (performance.timing && performance.timing.navigationStart){
      nowOffset = performance.timing.navigationStart
    }

    window.performance.now = function now(){
      return Date.now() - nowOffset;
    }
  }

})();
"""
    )

