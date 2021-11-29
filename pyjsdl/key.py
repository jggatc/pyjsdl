#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl import env
from pyjsdl import constants as Const

__docformat__ = 'restructuredtext'


class Key(object):
    """
    **pyjsdl.key**
    
    * pyjsdl.key.name
    * pyjsdl.key.get_mods
    * pyjsdl.key.set_repeat
    * pyjsdl.key.get_repeat
    """

    def __init__(self):
        """
        Provides methods to access the key function.
        
        Module initialization creates pyjsdl.key instance.
        """
        self.keyPress = env.event.keyPress
        self.keyMod = env.event.keyMod
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
                    name = keyname.split('_')[1].lower()
                    if len(name) != 1:
                        self._keys[getattr(Const, keyname)] = name
        if keycode in self._keys:
           return self._keys[keycode]
        else:
           return chr(keycode)

    def get_mods(self):
        """
        Return int modifier keys alt|ctrl|shift.
        """
        return self.keyMod[self.alt][self.keyPress[self.alt]] | self.keyMod[self.ctrl][self.keyPress[self.ctrl]] | self.keyMod[self.shift][self.keyPress[self.shift]]

    def set_repeat(self, delay=0, interval=0):
        """
        Set key repeat delay (ms) and interval (ms) settings.
        Key repeat initially disabled.
        """
        if delay < 0 or interval < 0:
            raise ValueError('repeat settings must be positive integers')
        if not delay:
            env.event.keyRepeat[0] = 0
            env.event.keyRepeat[1] = 0
        else:
            env.event.keyRepeat[0] = delay
            if interval:
                env.event.keyRepeat[1] = interval
            else:
                env.event.keyRepeat[1] = delay
        return None

    def get_repeat(self):
        """
        Get key repeat settings.
        """
        return env.event.keyRepeat

    def _nonimplemented_methods(self):
        self.get_focused = lambda *arg: None
        self.get_pressed = lambda *arg: None
        self.set_mods = lambda *arg: None


_modKey = {Const.K_ALT, Const.K_CTRL, Const.K_SHIFT}

_specialKey = {38:Const.K_UP, 40:Const.K_DOWN, 37:Const.K_LEFT, 39:Const.K_RIGHT, 36:Const.K_HOME, 35:Const.K_END, 33:Const.K_PAGEUP, 34:Const.K_PAGEDOWN,  8:Const.K_BACKSPACE, 46:Const.K_DELETE, 45:Const.K_INSERT, 12:Const.K_CLEAR, 13:Const.K_RETURN, 9:Const.K_TAB, 27:Const.K_ESCAPE, 20:Const.K_CAPSLOCK, 92:Const.K_LMETA, 93:Const.K_MENU, 44:Const.K_PRINT, 145:Const.K_SCROLLLOCK, 19:Const.K_PAUSE, 144:Const.K_NUMLOCK, 112:Const.K_F1, 113:Const.K_F2, 114:Const.K_F3, 115:Const.K_F4, 116:Const.K_F5, 117:Const.K_F6, 118:Const.K_F7, 119:Const.K_F8, 120:Const.K_F9, 121:Const.K_F10, 122:Const.K_F11, 123:Const.K_F12, 18:Const.K_ALT, 17:Const.K_CTRL, 16:Const.K_SHIFT}

