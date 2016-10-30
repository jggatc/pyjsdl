#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

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
            self.r,self.g,self.b,self.a = _color[0],_color[1],_color[2],_color[3]
        elif ln == 3:
            self.r,self.g,self.b,self.a = _color[0],_color[1],_color[2],255
        else:
            self.r,self.g,self.b,self.a = (_color>>16) & 0xff, (_color>>8) & 0xff, _color & 0xff, (_color>>24) & 0xff

    def __repr__(self):
        """
        Return string representation of Color object.
        """
        return "(%d,%d,%d,%d)" % (self.r, self.g, self.b, self.a)

    def __str__(self):
        """
        Return string representation of Color object.
        """
        return "rgba(%d,%d,%d,%f)" % (self.r, self.g, self.b, self.a/255.0)

    def __getitem__(self, index):
        """
        Get Color [r,g,b,a] attributes by index.
        """
        return {0:self.r, 1:self.g, 2:self.b, 3:self.a}[index]

    def __setitem__(self, index, val):
        self.__setattr__({0:'r', 1:'g', 2:'b', 3:'a'}[index], val)

    def __iter__(self):
        return iter([self.r, self.g, self.b, self.a])

    def __len__(self):
        return 4

    def __eq__(self, other):
        if hasattr(other, 'a'):
            return self.r==other.r and self.g==other.g and self.b==other.b and self.a==other.a
        else:
            if len(other) == 4:
                return self.a==other[3] and self.r==other[0] and self.g==other[1] and self.b==other[2]
            else:
                return self.r==other[0] and self.g==other[1] and self.b==other[2]

    def __ne__(self, other):
        if hasattr(other, 'a'):
            return self.r!=other.r or self.g!=other.g or self.b!=other.b or self.a!=other.a
        else:
            if len(other) == 4:
                return self.a!=other[3] or self.r!=other[0] or self.g!=other[1] or self.b!=other[2]
            else:
                return self.r!=other[0] or self.g!=other[1] or self.b!=other[2]

