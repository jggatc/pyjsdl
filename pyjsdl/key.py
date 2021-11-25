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

    def _nonimplemented_methods(self):
        self.get_focused = lambda *arg: None
        self.get_pressed = lambda *arg: None
        self.set_mods = lambda *arg: None
        self.set_repeat = lambda *arg: None
        self.get_repeat = lambda *arg: True


_charCode = {33:Const.K_EXCLAIM, 34:Const.K_QUOTEDBL, 35:Const.K_HASH, 36:Const.K_DOLLAR, 38:Const.K_AMPERSAND, 39:Const.K_QUOTE, 40:Const.K_LEFTPAREN, 41:Const.K_RIGHTPAREN, 42:Const.K_ASTERISK, 43:Const.K_PLUS, 44:Const.K_COMMA, 45:Const.K_MINUS, 46:Const.K_PERIOD, 97:Const.K_a, 98:Const.K_b, 99:Const.K_c, 100:Const.K_d, 101:Const.K_e, 102:Const.K_f, 103:Const.K_g, 104:Const.K_h, 105:Const.K_i, 106:Const.K_j, 107:Const.K_k, 108:Const.K_l, 109:Const.K_m, 110:Const.K_n, 111:Const.K_o, 112:Const.K_p, 113:Const.K_q, 114:Const.K_r, 115:Const.K_s, 116:Const.K_t, 117:Const.K_u, 118:Const.K_v, 119:Const.K_w, 120:Const.K_x, 121:Const.K_y, 122:Const.K_z}
if env.pyjs_mode.optimized:
    _modKey = {Const.K_ALT, Const.K_CTRL, Const.K_SHIFT}
    _specialKey = {Const.K_UP, Const.K_DOWN, Const.K_LEFT, Const.K_RIGHT, Const.K_HOME, Const.K_END, Const.K_PAGEDOWN, Const.K_PAGEUP, Const.K_BACKSPACE, Const.K_DELETE, Const.K_INSERT, Const.K_RETURN, Const.K_TAB, Const.K_ESCAPE}
else:
    _modKey = set([keycode.valueOf() for keycode in (Const.K_ALT, Const.K_CTRL, Const.K_SHIFT)])
    _specialKey = set([keycode.valueOf() for keycode in (Const.K_UP, Const.K_DOWN, Const.K_LEFT, Const.K_RIGHT, Const.K_HOME, Const.K_END, Const.K_PAGEDOWN, Const.K_PAGEUP, Const.K_BACKSPACE, Const.K_DELETE, Const.K_INSERT, Const.K_RETURN, Const.K_TAB, Const.K_ESCAPE)])

