#Pyjsdl - Copyright (C) 2013 James Garnon

import pyjsdl.event    ###0.13
import locals as Const  ###0.13
from pyjamas.ui import KeyboardListener     ###0.13

__docformat__ = 'restructuredtext'


class Key(object):
    """
    **pyjsdl.key**
    
    * pyjsdl.key.get_mods
    """

    def __init__(self):    ###0.13
        """
        Provides methods to access the key function.
        
        Module initialization creates pyjsdl.key instance.
        """
        self.keyPress = pyjsdl.event.keyPress
        self.keyMod = pyjsdl.event.keyMod
        self.alt = Const.K_ALT
        self.ctrl = Const.K_CTRL
        self.shift = Const.K_SHIFT
        self._nonimplemented_methods()

    def get_mods(self):     ###0.13
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
        self.name = lambda *arg: ''     ###0.13
        self.set_mods = lambda *arg: None
        self.set_repeat = lambda *arg: None
        self.get_repeat = lambda *arg: True

