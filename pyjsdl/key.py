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
        return (self.keyMod[self.alt][self.keyPress[self.alt]] |
                self.keyMod[self.ctrl][self.keyPress[self.ctrl]] |
                self.keyMod[self.shift][self.keyPress[self.shift]])

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


_code = {'Backquote':Const.K_BACKQUOTE, 'Backslash':Const.K_BACKSLASH,
         'Backspace':Const.K_BACKSPACE, 'BracketLeft':Const.K_LEFTBRACKET,
         'BracketRight':Const.K_RIGHTBRACKET, 'Comma':Const.K_COMMA,
         'Digit0':Const.K_0, 'Digit1':Const.K_1, 'Digit2':Const.K_2,
         'Digit3':Const.K_3, 'Digit4':Const.K_4, 'Digit5':Const.K_5,
         'Digit6':Const.K_6, 'Digit7':Const.K_7, 'Digit8':Const.K_8,
         'Digit9':Const.K_8, 'Equal':Const.K_EQUALS,
         'KeyA':Const.K_a, 'KeyB':Const.K_b, 'KeyC':Const.K_c,
         'KeyD':Const.K_d, 'KeyE':Const.K_e, 'KeyF':Const.K_f,
         'KeyG':Const.K_g, 'KeyH':Const.K_h, 'KeyI':Const.K_i,
         'KeyJ':Const.K_j, 'KeyK':Const.K_k, 'KeyL':Const.K_l,
         'KeyM':Const.K_m, 'KeyN':Const.K_n, 'KeyO':Const.K_o,
         'KeyP':Const.K_p, 'KeyQ':Const.K_q, 'KeyR':Const.K_r,
         'KeyS':Const.K_s, 'KeyT':Const.K_t, 'KeyU':Const.K_u,
         'KeyV':Const.K_v, 'KeyW':Const.K_w, 'KeyX':Const.K_x,
         'KeyY':Const.K_y, 'KeyZ':Const.K_z, 'Minus':Const.K_MINUS,
         'Period':Const.K_PERIOD, 'Quote':Const.K_QUOTE,
         'Semicolon':Const.K_SEMICOLON, 'Slash':Const.K_SLASH,
         'AltLeft':Const.K_LALT, 'AltRight':Const.K_RALT,
         'CapsLock':Const.K_CAPSLOCK, 'ContextMenu':Const.K_MENU,
         'ControlLeft':Const.K_LCTRL, 'ControlRight':Const.K_RCTRL,
         'Enter':Const.K_RETURN, 'MetaLeft':Const.K_LMETA,
         'MetaRight':Const.K_RMETA, 'ShiftLeft':Const.K_LSHIFT,
         'ShiftRight':Const.K_RSHIFT, 'Space':Const.K_SPACE,
         'Tab':Const.K_TAB, 'Delete':Const.K_DELETE, 'End':Const.K_END,
         'Help':Const.K_HELP, 'Home':Const.K_HOME, 'Insert':Const.K_INSERT,
         'PageDown':Const.K_PAGEDOWN, 'PageUp':Const.K_PAGEUP,
         'ArrowDown':Const.K_DOWN, 'ArrowLeft':Const.K_LEFT,
         'ArrowRight':Const.K_RIGHT, 'ArrowUp':Const.K_UP,
         'NumLock':Const.K_NUMLOCK, 'Numpad0':Const.K_KP0,
         'Numpad1':Const.K_KP1, 'Numpad2':Const.K_KP2,
         'Numpad3':Const.K_KP3, 'Numpad4':Const.K_KP4,
         'Numpad5':Const.K_KP5, 'Numpad6':Const.K_KP6,
         'Numpad7':Const.K_KP7, 'Numpad8':Const.K_KP8,
         'Numpad9':Const.K_KP9, 'NumpadAdd':Const.K_KP_PLUS,
         'NumpadDecimal':Const.K_KP_PERIOD, 'NumpadDivide':Const.K_KP_DIVIDE,
         'NumpadEnter':Const.K_KP_ENTER, 'NumpadEqual':Const.K_KP_EQUALS,
         'NumpadMultiply':Const.K_KP_MULTIPLY, 'NumpadSubtract':Const.K_KP_MINUS,
         'F1':Const.K_F1, 'F2':Const.K_F2, 'F3':Const.K_F3,
         'F4':Const.K_F4, 'F5':Const.K_F5, 'F6':Const.K_F6,
         'F7':Const.K_F7, 'F8':Const.K_F8, 'F9':Const.K_F9,
         'F10':Const.K_F10, 'F11':Const.K_F11, 'F12':Const.K_F12,
         'PrintScreen':Const.K_PRINT, 'ScrollLock':Const.K_SCROLLOCK,
         'Pause':Const.K_PAUSE, 'Escape':Const.K_ESCAPE,
         'Unidentified':Const.K_UNKNOWN}

_modKey = {'Alt':Const.K_ALT , 'Control':Const.K_CTRL, 'Shift':Const.K_SHIFT}

_modKeyCode = {Const.K_ALT, Const.K_CTRL, Const.K_SHIFT}

_specialKey = {'ArrowUp':Const.K_UP, 'ArrowDown':Const.K_DOWN,
               'ArrowLeft':Const.K_LEFT, 'ArrowRight':Const.K_RIGHT,
               'Up':Const.K_UP, 'Down':Const.K_DOWN,
               'Left':Const.K_LEFT, 'Right':Const.K_RIGHT,
               'Home':Const.K_HOME, 'End':Const.K_END,
               'PageUp':Const.K_PAGEUP, 'PageDown':Const.K_PAGEDOWN,
               'Backspace':Const.K_BACKSPACE, 'Delete':Const.K_DELETE,
               'Insert':Const.K_INSERT, 'Clear':Const.K_CLEAR,
               'Escape':Const.K_ESCAPE, 'Esc':Const.K_ESCAPE,
               'CapsLock':Const.K_CAPSLOCK, 'Meta':Const.K_LMETA,
               'ContextMenu':Const.K_MENU, 'PrintScreen':Const.K_PRINT,
               'ScrollLock':Const.K_SCROLLLOCK, 'Pause':Const.K_PAUSE,
               'NumLock':Const.K_NUMLOCK,
               'F1':Const.K_F1, 'F2':Const.K_F2, 'F3':Const.K_F3,
               'F4':Const.K_F4, 'F5':Const.K_F5, 'F6':Const.K_F6,
               'F7':Const.K_F7, 'F8':Const.K_F8, 'F9':Const.K_F9,
               'F10':Const.K_F10, 'F11':Const.K_F11, 'F12':Const.K_F12,
               'Alt':Const.K_ALT , 'Control':Const.K_CTRL, 'Shift':Const.K_SHIFT}

_specialKeyCode = {38:Const.K_UP, 40:Const.K_DOWN,
                   37:Const.K_LEFT, 39:Const.K_RIGHT,
                   36:Const.K_HOME, 35:Const.K_END,
                   33:Const.K_PAGEUP, 34:Const.K_PAGEDOWN,
                   8:Const.K_BACKSPACE, 46:Const.K_DELETE,
                   45:Const.K_INSERT, 12:Const.K_CLEAR,
                   13:Const.K_RETURN, 9:Const.K_TAB,
                   27:Const.K_ESCAPE, 20:Const.K_CAPSLOCK,
                   92:Const.K_LMETA, 93:Const.K_MENU,
                   44:Const.K_PRINT, 145:Const.K_SCROLLLOCK,
                   19:Const.K_PAUSE, 144:Const.K_NUMLOCK,
                   112:Const.K_F1, 113:Const.K_F2, 114:Const.K_F3,
                   115:Const.K_F4, 116:Const.K_F5, 117:Const.K_F6,
                   118:Const.K_F7, 119:Const.K_F8, 120:Const.K_F9,
                   121:Const.K_F10, 122:Const.K_F11, 123:Const.K_F12,
                   18:Const.K_ALT, 17:Const.K_CTRL, 16:Const.K_SHIFT}

