#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

import pyjsdl.event
from pyjsdl import locals as Const

__docformat__ = 'restructuredtext'


class Key(object):
    """
    **pyjsdl.key**
    
    * pyjsdl.key.name
    * pyjsdl.key.get_mods
    """

    def __init__(self):
        """
        Provides methods to access the key function.
        
        Module initialization creates pyjsdl.key instance.
        """
        self.keyPress = pyjsdl.event.keyPress
        self.keyMod = pyjsdl.event.keyMod
        self.alt = Const.K_ALT
        self.ctrl = Const.K_CTRL
        self.shift = Const.K_SHIFT
        self._keys = {}
        self._nonimplemented_methods()

    def name(self, keycode):
        """
        Return name of key of a keycode.
        """
        if not self._keys:
            for keyname in dir(Const):
                if keyname.startswith('K_'):
                    self._keys[getattr(Const, keyname)] = keyname.split('_')[-1].lower()
            self._keys[0] = 'unknown key'
        if keycode not in self._keys:
            keycode = 0
        return self._keys[keycode]

    def get_mods(self):
        """
        Return int modifier keys alt|ctrl|shift.
        """
        return self.keyMod[self.alt][self.keyPress[self.alt]] | self.keyMod[self.ctrl][self.keyPress[self.ctrl]] | self.keyMod[self.shift][self.keyPress[self.shift]]

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.get_focused = lambda *arg: None
        self.get_pressed = lambda *arg: None
        self.set_mods = lambda *arg: None
        self.set_repeat = lambda *arg: None
        self.get_repeat = lambda *arg: True

