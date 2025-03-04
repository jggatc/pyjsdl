#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Color module**

The module provides a color object.
"""

from pyjsdl.pyjsobj import Color as _Color


class Color(_Color):
    """
    Color object.
    """

    def __init__(self, *color):
        """
        Initialize Color object.
        
        Alternative arguments::
        
        * r,g,b,a
        * r,g,b
        * (r,g,b,a)
        * (r,g,b)
        * integer argb
        * html string '#rrggbb[aa]'
        * hex string '0xrrggbb[aa]'
        * Color

        Color has the attributes::
        
            r, g, b, a

        Operator functionality in --optimized mode (-O) requires --enable-operator-funcs.
        Module initialization places Color in module's namespace.
        """
        ln = len(color)
        if ln == 1:
            _color = color[0]
            if hasattr(_color, '__len__'):
                ln = len(_color)
        else:
            _color = color
        if ln == 4:
            self.r = _color[0]
            self.g = _color[1]
            self.b = _color[2]
            self.a = _color[3]
        elif ln == 3:
            self.r = _color[0]
            self.g = _color[1]
            self.b = _color[2]
            self.a = 255
        else:
            if not hasattr(_color, 'startswith'):
                self.r = (_color>>16) & 0xff
                self.g = (_color>>8) & 0xff
                self.b = _color & 0xff
                self.a = (_color>>24) & 0xff
            else:
                _color = _color.lower()
                if _color.startswith('#'):
                    _color = _color.lstrip('#')
                elif _color.startswith('0x'):
                    _color = _color.lstrip('0x')
                if len(_color) == 6:
                    _color += 'ff'
                self.r = int(_color[0:2], 16)
                self.g = int(_color[2:4], 16)
                self.b = int(_color[4:6], 16)
                self.a = int(_color[6:8], 16)

    def __str__(self):
        return "rgba(%d, %d, %d, %f)" % (self.r, self.g, self.b, self.a/255.0)

    def __repr__(self):
        return "(%d, %d, %d, %d)" % (self.r, self.g, self.b, self.a)

    def __getitem__(self, index):
        return {0:self.r, 1:self.g, 2:self.b, 3:self.a}[index]

    def __setitem__(self, index, val):
        self.__setattr__({0:'r', 1:'g', 2:'b', 3:'a'}[index], val)

    def __iter__(self):
        return iter([self.r, self.g, self.b, self.a])

    def __len__(self):
        return 4

    def __eq__(self, other):
        if hasattr(other, 'a'):
            return ( self.r == other.r and
                     self.g == other.g and
                     self.b == other.b and
                     self.a == other.a )
        else:
            if len(other) == 4:
                return ( self.a == other[3] and
                         self.r == other[0] and
                         self.g == other[1] and
                         self.b == other[2] )
            else:
                return ( self.r == other[0] and
                         self.g == other[1] and
                         self.b == other[2] )

    def __ne__(self, other):
        if hasattr(other, 'a'):
            return ( self.r != other.r or
                     self.g != other.g or
                     self.b != other.b or
                     self.a != other.a )
        else:
            if len(other) == 4:
                return ( self.a != other[3] or
                         self.r != other[0] or
                         self.g != other[1] or
                         self.b != other[2] )
            else:
                return ( self.r != other[0] or
                         self.g != other[1] or
                         self.b != other[2] )

    def __add__(self, other):
        r = self.r + other.r
        if r > 255: r = 255
        g = self.g + other.g
        if g > 255: g = 255
        b = self.b + other.b
        if b > 255: b = 255
        a = self.a + other.a
        if a > 255: a = 255
        return self.__class__(r,g,b,a)

    def __sub__(self, other):
        r = self.r - other.r
        if r < 0: r = 0
        g = self.g - other.g
        if g < 0: g = 0
        b = self.b - other.b
        if b < 0: b = 0
        a = self.a - other.a
        if a < 0: a = 0
        return self.__class__(r,g,b,a)

    def __mul__(self, other):
        r = self.r * other.r
        if r > 255: r = 255
        g = self.g * other.g
        if g > 255: g = 255
        b = self.b * other.b
        if b > 255: b = 255
        a = self.a * other.a
        if a > 255: a = 255
        return self.__class__(r,g,b,a)

    def __floordiv__(self, other):
        if other.r != 0: r = int(self.r // other.r)
        else: r = 0
        if other.g != 0: g = int(self.g // other.g)
        else: g = 0
        if other.b != 0: b = int(self.b // other.b)
        else: b = 0
        if other.a != 0: a = int(self.a // other.a)
        else: a = 0
        return self.__class__(r,g,b,a)

    def __mod__(self, other):
        if other.r != 0: r = self.r % other.r
        else: r = 0
        if other.g != 0: g = self.g % other.g
        else: g = 0
        if other.b != 0: b = self.b % other.b
        else: b = 0
        if other.a != 0: a = self.a % other.a
        else: a = 0
        return self.__class__(r,g,b,a)

    def __iadd__(self, other):
        self.r += other.r
        if self.r > 255: self.r = 255
        self.g += other.g
        if self.g > 255: self.g = 255
        self.b += other.b
        if self.b > 255: self.b = 255
        self.a += other.a
        if self.a > 255: self.a = 255
        return self

    def __isub__(self, other):
        self.r -= other.r
        if self.r < 0: self.r = 0
        self.g -= other.g
        if self.g < 0: self.g = 0
        self.b -= other.b
        if self.b < 0: self.b = 0
        self.a -= other.a
        if self.a < 0: self.a = 0
        return self

    def __imul__(self, other):
        self.r *= other.r
        if self.r > 255: self.r = 255
        self.g *= other.g
        if self.g > 255: self.g = 255
        self.b *= other.b
        if self.b > 255: self.b = 255
        self.a *= other.a
        if self.a > 255: self.a = 255
        return self

    def __ifloordiv__(self, other):
        if other.r != 0: self.r //= other.r
        else: self.r = 0
        if other.g != 0: self.g //= other.g
        else: self.g = 0
        if other.b != 0: self.b //= other.b
        else: self.b = 0
        if other.a != 0: self.a //= other.a
        else: self.a = 0
        return self

    def __imod__(self, other):
        if other.r != 0: self.r %= other.r
        else: self.r = 0
        if other.g != 0: self.g %= other.g
        else: self.g = 0
        if other.b != 0: self.b %= other.b
        else: self.b = 0
        if other.a != 0: self.a %= other.a
        else: self.a = 0
        return self

    def __invert__(self):
        return self.__class__(~self.r + 256,
                              ~self.g + 256,
                              ~self.b + 256,
                              ~self.a + 256)

    def normalize(self):
        """
        Return normalized color values.
        """
        return (self.r / 255.0,
                self.g / 255.0,
                self.b / 255.0,
                self.a / 255.0)

    def correct_gamma(self, gamma):
        """
        Return gamma-corrected Color.
        """
        return self.__class__(int(round((((self.r) / 255.0)**gamma) * 255.0)),
                              int(round((((self.g) / 255.0)**gamma) * 255.0)),
                              int(round((((self.b) / 255.0)**gamma) * 255.0)),
                              int(round((((self.a) / 255.0)**gamma) * 255.0)))

    def premul_alpha(self):
        """
        Return alpha-multipled Color.
        """
        return self.__class__(int(round(self.r * (self.a/255.0))),
                              int(round(self.g * (self.a/255.0))),
                              int(round(self.b * (self.a/255.0))),
                              self.a)

    def lerp(self, color, t):
        """
        Return a Color linear interpolated by t to the given color.
        """
        if t < 0.0 or t > 1.0:
            raise ValueError('Argument t must be in range 0 to 1')
        if hasattr(color, 'a'):
            return self.__class__(int(round(self.r * (1-t) + color.r * t)),
                                  int(round(self.g * (1-t) + color.g * t)),
                                  int(round(self.b * (1-t) + color.b * t)),
                                  int(round(self.a * (1-t) + color.a * t)))
        else:
            if len(color) == 3:
                return self.__class__(int(round(self.r * (1-t) + color[0] * t)),
                                      int(round(self.g * (1-t) + color[1] * t)),
                                      int(round(self.b * (1-t) + color[2] * t)),
                                      int(round(self.a * (1-t) + 255 * t)))
            elif len(color) == 4:
                return self.__class__(int(round(self.r * (1-t) + color[0] * t)),
                                      int(round(self.g * (1-t) + color[1] * t)),
                                      int(round(self.b * (1-t) + color[2] * t)),
                                      int(round(self.a * (1-t) + color[3] * t)))
            else:
                raise ValueError('invalid color argument')

    def update(self, *color):
        """
        Update color values.
        """
        ln = len(color)
        if ln == 1:
            _color = color[0]
            if hasattr(_color, '__len__'):
                ln = len(_color)
        else:
            _color = color
        if ln == 4:
            self.r = _color[0]
            self.g = _color[1]
            self.b = _color[2]
            self.a = _color[3]
        elif ln == 3:
            self.r = _color[0]
            self.g = _color[1]
            self.b = _color[2]
            self.a = 255
        else:
            if not hasattr(_color, 'startswith'):
                self.r = (_color>>16) & 0xff
                self.g = (_color>>8) & 0xff
                self.b = _color & 0xff
                self.a = (_color>>24) & 0xff
            else:
                _color = _color.lower()
                if _color.startswith('#'):
                    _color = _color.lstrip('#')
                elif _color.startswith('0x'):
                    _color = _color.lstrip('0x')
                if len(_color) == 6:
                    _color += 'ff'
                self.r = int(_color[0:2], 16)
                self.g = int(_color[2:4], 16)
                self.b = int(_color[4:6], 16)
                self.a = int(_color[6:8], 16)

    def _get_cmy(self):
        return _rgb_to_cmy(self.r, self.g, self.b)

    def _set_cmy(self, val):
        self.r, self.g, self.b = _cmy_to_rgb(*val)

    def _get_hsva(self):
        return _rgba_to_hsva(self.r, self.g, self.b, self.a)

    def _set_hsva(self, val):
        self.r, self.g, self.b, self.a = _hsva_to_rgba(*val)

    def _get_hsla(self):
        return _rgba_to_hsla(self.r, self.g, self.b, self.a)

    def _set_hsla(self, val):
        self.r, self.g, self.b, self.a = _hsla_to_rgba(*val)

    cmy = property(_get_cmy, _set_cmy)
    "CMY color."

    hsva = property(_get_hsva, _set_hsva)
    "HSVA color."

    hsla = property(_get_hsla, _set_hsla)
    "HSLA color."


def _rgb_to_cmy(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    c, m, y = 1-r, 1-g, 1-b
    return (c, m, y)


def _cmy_to_rgb(c, m, y):
    r, g, b = 1-c, 1-m, 1-y
    return (int(r*255), int(g*255), int(b*255))


def _rgba_to_hsva(r, g, b, a):
    r, g, b, a = r/255.0, g/255.0, b/255.0, a/255.0
    c_max = max(r, g, b)
    c_min = min(r, g, b)
    delta = c_max - c_min
    if delta == 0:
        h = 0.0
    elif c_max == r:
        h = (60 * ((g - b) / delta) + 360) % 360.0
    elif c_max == g:
        h = (60 * ((b - r) / delta) + 120) % 360.0
    elif c_max == b:
        h = (60 * ((r - g) / delta) + 240) % 360.0
    if c_max == 0:
        s = 0.0
    else:
        s = (delta / c_max)
    v = c_max
    return h, s*100.0, v*100.0, a*100.0


def _hsva_to_rgba(h, s, v, a):
    h, s, v, a = h/360.0, s/100.0, v/100.0, a/100.0
    i = int(h*6.0)
    f = (h*6.0) - i
    p = (v * (1.0 - s))
    q = (v * (1.0 - s * f))
    t = (v * (1.0 - (s * (1.0-f))))
    i %= 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    elif i == 5:
        r, g, b = v, p, q
    return int(r*255), int(g*255), int(b*255), int(a*255)


def _rgba_to_hsla(r, g, b, a):
    r, g, b, a = r/255.0, g/255.0, b/255.0, a/255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin
    l = (cmax + cmin) / 2.0
    if delta == 0:
        s = 0.0
    else:
        s = delta / (1-abs(2*l-1))
    if delta == 0:
        h = 0.0
    elif cmax == r:
        h = (60 * ((g - b) / delta) + 360) % 360.0
    elif cmax == g:
        h = (60 * ((b - r) / delta) + 120) % 360.0
    elif cmax == b:
        h = (60 * ((r - g) / delta) + 240) % 360.0
    return h, s*100.0, l*100.0, a*100.0


def _hsla_to_rgba(h, s, l, a):
    h, s, l, a = h/360.0, s/100.0, l/100.0, a/100.0
    if l < 0.5:
        q = l * (1+s)
    else:
        q = l + s - l * s
    p = 2 * l - q
    t = h + 1.0/3.0
    if t < 0.0: t += 1.0
    elif t > 1.0: t -= 1.0
    if t < 1.0/6.0:
        r = p + (q - p) * 6.0 * t
    elif t < 1.0/2.0:
        r = q
    elif t < 2.0/3.0:
        r = p + (q - p) * (2.0/3.0-t) * 6.0
    else:
        r = p
    t = h
    if t < 0.0: t += 1.0
    elif t > 1.0: t -= 1.0
    if t < 1.0/6.0:
        g = p + (q - p) * 6.0 * t
    elif t < 1.0/2.0:
        g = q
    elif t < 2.0/3.0:
        g = p + (q - p) * (2.0/3.0-t) * 6.0
    else:
        g = p
    t = h - 1.0/3.0
    if t < 0.0: t += 1.0
    elif t > 1.0: t -= 1.0
    if t < 1.0/6.0:
        b = p + (q - p) * 6.0 * t
    elif t < 1.0/2.0:
        b = q
    elif t < 2.0/3.0:
        b = p + (q - p) * (2.0/3.0-t) * 6.0
    else:
        b = p
    return int(r*255), int(g*255), int(b*255), int(a*255)

