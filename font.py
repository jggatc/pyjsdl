#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

#from __future__ import division
from math import ceil as _ceil
from pyjsdl.surface import Surface
from pyjsdl.color import Color
from pyjsdl.pyjsobj import HTML5Canvas

__docformat__ = 'restructuredtext'


_initialized = False
_surf = None


def init():
    """
    **pyjsdl.font.init**
    
    Initialize font module.
    """
    global _surf, _initialized, match_font
    if _initialized:
        return
    try:
        _surf = HTML5Canvas(1,1)
        _surf.measureText('x')
    except:
        _surf = None
    _initialized = True
init()


def quit():
    """
    **pyjsdl.font.quit**
    
    Unintialize font module.
    """
    global _surf, _initialized
    _surf = None
    _initialized = False


def get_init():
    """
    **pyjsdl.font.get_init**
    
    Check if font module is initialized.
    """
    return _initialized


def get_default_font():
    """
    **pyjs2d.font.get_default_font**
    
    Return default font.
    """
    return Font._font[0]


def get_fonts():
    """
    **pyjsdl.font.get_fonts**
    
    Return font names, which have fallback fonts if unavailable.
    """
    return Font._font


def match_font(name):
    """
    **pyjsdl.font.match_font**
    
    Argument name is a font name, or comma-delimited string of font names.
    Return font string in compliant format.
    """
    fallback = False
    font = [fn.strip().lower() for fn in name.split(',')]
    for i, fn in enumerate(font):
        if fn in Font._font:
            fallback = True
            continue
        else:
            f = ''.join(c for c in fn if c.isalnum())
            if f in Font._font_alt:
                font[i] = Font._font[Font._font_alt[f]]
                fallback = True
    if not fallback:
        font.append(Font._font[0])
    font = ','.join(font)
    return font


class Font(object):
    """
    **pyjsdl.font.Font**
    
    * Font.render
    * Font.size
    * Font.set_underline
    * Font.get_underline
    * Font.set_bold
    * Font.get_bold
    * Font.set_italic
    * Font.get_italic
    * Font.get_linesize
    """

    _font = ['arial', 'bitstream vera sans', 'bitstream vera serif', 'book antiqua', 'comic sans ms', 'courier new', 'courier', 'dejavu sans', 'dejavu sans mono', 'dejavu serif', 'freesans', 'garamond', 'georgia', 'helvetica', 'impact', 'liberation sans', 'liberation serif', 'lucida console', 'lucida serif', 'nimbus mono l', 'nimbus roman no9 l', 'nimbus sans l', 'palatino', 'times new roman', 'times', 'tahoma', 'verdana', 'cursive', 'monospace', 'sans-serif', 'serif']

    _font_alt = {'arial':0, 'bitstreamverasans':1, 'bitstreamveraserif':2, 'bookantiqua':3, 'comicsansms':4, 'couriernew':5, 'courier':6, 'dejavusans':7, 'dejavusansmono':8, 'dejavuserif':9, 'freesans':10, 'garamond':11, 'georgia':12, 'helvetica':13, 'impact':14, 'liberationsans':15, 'liberationserif':16, 'lucidaconsole':17, 'lucidaserif':18, 'nimbusmonol':19, 'nimbusromanno9l':20, 'nimbussansl':21, 'palatino':22, 'timesnewroman':23, 'times':24, 'tahoma':25, 'verdana':26, 'cursive':27, 'monospace':28, 'sansserif':29, 'serif':30}
    
    _font_family = [['arial', 'helvetica', 'liberation sans',  'nimbus sans l', 'freesans', 'tahoma', 'sans-serif'], ['verdana', 'bitstream vera sans', 'dejavu sans', 'sans-serif'], ['impact', 'sans-serif'], ['comic sans ms', 'cursive', 'sans-serif'], ['courier new', 'courier', 'lucida console', 'dejavu sans mono', 'monospace'], ['times new roman', 'times', 'liberation serif', 'nimbus roman no9 l', 'serif'], ['garamond',  'book antiqua', 'palatino', 'liberation serif', 'nimbus roman no9 l', 'serif'], ['georgia', 'bitstream vera serif', 'lucida serif', 'liberation serif', 'dejavu serif', 'serif']]

    def __init__(self, name, size):
        """
        Return Font object.
        Arguments include name of a system font and size of font. The name argument can be a string of comma-delimited names to specify fallbacks and use a default font if none found.
        """
        if not name:
            name = Font._font[0]
        font = [fn.strip().lower() for fn in name.split(',')]
        fallback = None
        for i, fn in enumerate(font):
            if fn in Font._font:
                if not fallback:
                    fallback = fn
            else:
                f = ''.join(c for c in fn if c.isalnum())
                if f in Font._font_alt:
                    font[i] = Font._font[Font._font_alt[f]]
                    if not fallback:
                        fallback = font[i]
        if fallback:
            for ff in Font._font_family:
                if fallback in ff:
                    font.extend(f for f in ff if f not in font)
                    break
        else:
            font.extend(Font._font_family[0])
        self.fontname = ','.join(font)
        self.fontsize = size
        self.bold = ''
        self.italic = ''
        self.fontstyle = self.bold + ' ' + self.italic
        self.underline = False
        self.char_size = None
        self._nonimplemented_methods()

    def __repr__(self):
        """
        Return string representation of Font object.
        """
        return "%s(%r)" % (self.__class__, self.__dict__)

    def render(self, text, antialias=True, color=(0,0,0), background=None, surface=None):      #optional surface for text rendering
        """
        Render text onto surface.
        Arguments are text to render, and optional antialias, RGB color of text, RGB color of background, and surface for text rendering.
        """
        if not surface:
            w,h = self.size(text)
            surf = Surface((w,h))
        else:
            surf = surface
            w,h = surface.width, surface.height
        if background:
            surf.setFillStyle(Color(background))
            surf.fillRect(0,0,w,h)
        surf.setFont('%s %dpx %s' % (self.fontstyle, self.fontsize, self.fontname))
#        if antialias: pass
        surf.setFillStyle(Color(color))
        surf.fillText(text,0,self.fontsize)
        if self.underline:
            surf.setLineWidth(1)
            surf.setStrokeStyle(Color(color))
            surf.setStroke(BasicStroke(1))
            surf.moveTo(0, h-1)
            surf.lineTo(w-1, h-1)
            surf.stroke()
        return surf

    def size(self, text):
        """
        Return size x,y of a surface for of given text.
        """
        if _surf:   #>IE9 - use exception if HTML5Canvas not implemented
            _surf.setFont('%s %dpx %s' % (self.fontstyle, self.fontsize, self.fontname))
            x = _surf.measureText(text)
        else:   #estimate
            x = self._size_estimate(text)
        if x < 1:
            x = 1
        y = self.fontsize + 5
        return (x, y)

    def _size_estimate(self, text=None):   #for browsers HTML5Canvas not implemented
        if not self.char_size:
            self.char_size = self._get_char_size()
        self.fontname = ','.join(Font._font_family[0])
        self.fontstyle = ''
        size = []
        for char in text:
            try:
                size.append(self.char_size[char] * self.fontsize)
            except KeyError:
                size.append(self.char_size['x'] * self.fontsize)
        x = _ceil( sum(size) )
        return x

    def set_underline(self, setting=True):
        """
        Set font underline style.
        Optional setting argument, default to True.
        """
        self.underline = setting

    def get_underline(self):
        """
        Check if font is underlined.
        """
        return self.underline

    def set_bold(self, setting=True):
        """
        Set font bold style.
        Optional setting argument, default to True.
        """
        self.bold = {True:'bold', False:''}[setting]
        self.fontstyle = self.bold + ' ' + self.italic

    def get_bold(self):
        """
        Check if font is bold.
        """
        if self.bold:
            return True
        else:
            return False

    def set_italic(self, setting=True):
        """
        Set font italic style.
        Optional setting argument, default to True.
        """
        self.italic = {True:'italic', False:''}[setting]
        self.fontstyle = self.bold + ' ' + self.italic

    def get_italic(self):
        """
        Check if font is italized.
        """
        if self.italic:
            return True
        else:
            return False

    def get_linesize(self):
        """
        Return linesize of font.
        """
        return int(self.fontsize*1.2)

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.metrics = lambda *arg: []
        self.get_height = lambda *arg: 0
        self.get_ascent = lambda *arg: 0
        self.get_descent = lambda *arg: 0

    def _get_char_size(self, font=None):    #for browsers HTML5Canvas not implemented
        if not font:
            return {'a': 0.6, 'b': 0.6, 'c': 0.5, 'd': 0.6, 'e': 0.6, 'f': 0.3, 'g': 0.6, 'h': 0.6, 'i': 0.2, 'j': 0.2, 'k': 0.5, 'l': 0.2, 'm': 0.8, 'n': 0.6, 'o': 0.6, 'p': 0.6, 'q': 0.6, 'r': 0.3, 's': 0.5, 't': 0.3, 'u': 0.6, 'v': 0.5, 'w': 0.7, 'x': 0.5, 'y': 0.5, 'z': 0.5, 'A': 0.7, 'B': 0.7, 'C': 0.7, 'D': 0.7, 'E': 0.7, 'F': 0.6, 'G': 0.8, 'H': 0.7, 'I': 0.3, 'J': 0.5, 'K': 0.7, 'L': 0.6, 'M': 0.8, 'N': 0.7, 'O': 0.8, 'P': 0.7, 'Q': 0.8, 'R': 0.7, 'S': 0.7, 'T': 0.6, 'U': 0.7, 'V': 0.7, 'W': 0.9, 'X': 0.7, 'Y': 0.7, 'Z': 0.6, '0': 0.6, '1': 0.6, '2': 0.6, '3': 0.6, '4': 0.6, '5': 0.6, '6': 0.6, '7': 0.6, '8': 0.6, '9': 0.6, '.': 0.3, ',': 0.3, ':': 0.3, ';': 0.3, '?': 0.6, '~': 0.6, '!': 0.3, '@': 1, '#': 0.6, '$': 0.6, '%': 0.9, '^': 0.5, '&': 0.7, '=': 0.6, '+': 0.6, '-': 0.3, '*': 0.4, '/': 0.3, '\\': 0.3, '_': 0.6, '<': 0.6, '>': 0.6, '(': 0.3, ')': 0.3, '{': 0.3, '}': 0.3, '[': 0.3, ']': 0.3, "'": 0.2, '"': 0.4, ' ': 0.3}
        else:
            fontsize = 10
            _surf.setFont('%dpx %s' % (fontsize, font))     #generated font='arial'
            char_size = {}
            for char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,:;?~!@#$%^&=+-*/\_<>(){}[]\'\" ':
                char_size[char] = float(_surf.measureText(char)/fontsize)
            return char_size


class SysFont(Font):
    """
    **pyjsdl.font.SysFont**
    
    * Font subclass
    """

    def __init__(self, name, size, bold=False, italic=False):
        """
        Return SysFont subclassed of Font.
        Arguments include name of a system font and size of font, with optional bold and italic style. The name argument can be a string of comma-delimited names to specify fallbacks and use a default font if none found.
        """
        Font.__init__(self,name,size)
        self.bold = {True:'bold', False:''}[bold]
        self.italic = {True:'italic', False:''}[bold]
        self.fontstyle = self.bold + ' ' + self.italic

