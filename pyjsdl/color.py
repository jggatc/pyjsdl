#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl.pyjsobj import Color as _Color

__docformat__ = 'restructuredtext'


class Color(_Color):

    def __init__(self, *color):
        """
        Return Color object.
        
        Alternative arguments:
        
        * r,g,b,a
        * r,g,b
        * (r,g,b,a)
        * (r,g,b)
        * integer rgba
        * Color

        Color has the attributes::
        
            r, g, b, a

        Module initialization places pyjsdl.Color in module's namespace.
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
            if hasattr(_color, 'startswith') and _color.startswith('#'):
                _color = '0x' + _color[1:]
            self.r = (_color>>16) & 0xff
            self.g = (_color>>8) & 0xff
            self.b = _color & 0xff
            self.a = (_color>>24) & 0xff

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

