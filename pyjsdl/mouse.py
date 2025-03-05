#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Mouse module**

The module provides mouse functionality.
"""

from pyjsdl import env
from pyjsdl import cursors
from pyjsdl.pyjsobj import DOM


class Mouse(object):
    """
    Mouse object.
    """

    def __init__(self):
        """
        Provides methods to access the mouse function.

        Module initialization creates pyjsdl.mouse instance.
        """
        self.mousePos = env.event.mousePos
        self.mousePosPre = env.event.mousePosPre
        self.mousePosRel = env.event.mousePosRel
        self.mousePress = env.event.mousePress
        self._cursorVisible = True
        self._cursor = 'default'
        self._nonimplemented_methods()

    def get_pressed(self):
        """
        Return state of mouse buttons as a tuple of bool for button1,2,3.
        """
        return (self.mousePress[0],
                self.mousePress[1],
                self.mousePress[2])

    def get_pos(self):
        """
        Return x,y of mouse pointer.

        If the pointer is not in canvas, returns -1,-1
        """
        if self.mousePos['x'] != -1:
            return (self.mousePos['x'] + env.frame.scrollLeft,
                    self.mousePos['y'] + env.frame.scrollTop)
        else:
            return (self.mousePos['x'],  self.mousePos['y'])

    def get_rel(self):
        """
        Return relative x,y change of mouse position since last call.
        """
        if self.mousePos['x'] != -1:
            rel = (self.mousePos['x'] - self.mousePosRel['x'],
                   self.mousePos['y'] - self.mousePosRel['y'])
            self.mousePosRel['x'] = self.mousePos['x']
            self.mousePosRel['y'] = self.mousePos['y']
            return rel
        else:
            return (0, 0)

    def set_visible(self, visible):
        """
        Set mouse cursor visibility according to visible bool argument.

        Return previous cursor visibility state.
        """
        visible_pre = self._cursorVisible
        if visible:
            DOM.setStyleAttribute(env.canvas.getElement(),
                                  'cursor', self._cursor)
            self._cursorVisible = True
        else:
            DOM.setStyleAttribute(env.canvas.getElement(),
                                  'cursor', 'none')
            self._cursorVisible = False
        return visible_pre

    def get_focused(self):
        """
        Check if mouse has focus.
        """
        return self.mousePos['x'] != -1

    def set_cursor(self, *cursor):
        """
        Set mouse cursor.

        Alternative arguments:
        * system cursor or cursor object
        * image url or surface, hotspot (x,y), and optional fallback
        * size, hotspot, data, mask, and optional fallback
        Refer to cursors module for details.
        """
        args = len(cursor)
        if args == 1:
            self._cursor = cursor[0]
        elif args in (2,3):
            if isinstance(cursor[0], str):
                url = cursor[0]
            else:
                url = cursor[0].toDataURL()
            hotspot = cursor[1]
            if args == 2:
                fallback = 'default'
            else:
                fallback = cursor[2]
            self._cursor = 'url("%s") %d %d, %s' % (url,
                                                    hotspot[0],
                                                    hotspot[1],
                                                    fallback)
        elif args in (4,5):
            size = cursor[0]
            hotspot = cursor[1]
            data = cursor[2]
            mask = cursor[3]
            if args == 4:
                fallback = 'default'
            else:
                fallback = cursor[4]
            surface = cursors.create_cursor(size, data, mask)
            url = surface.toDataURL()
            self._cursor = 'url("%s") %d %d, %s' % (url,
                                                    hotspot[0],
                                                    hotspot[1],
                                                    fallback)
        else:
            self._cursor = 'default'
        if self._cursorVisible:
            DOM.setStyleAttribute(env.canvas.getElement(),
                                  'cursor', self._cursor)

    def get_cursor(self):
        """
        Return cursor object.
        """
        return self._cursor

    def _nonimplemented_methods(self):
        self.set_pos = lambda *arg: None

