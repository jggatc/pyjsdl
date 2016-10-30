#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from pyjsdl.pyjsobj import HTML5Canvas
from pyjsdl.rect import Rect, rectPool
from pyjsdl.color import Color
from __pyjamas__ import JS

__docformat__ = 'restructuredtext'


class Surface(HTML5Canvas):
    """
    **pyjsdl.Surface**
    
    * Surface.get_size
    * Surface.get_width
    * Surface.get_height
    * Surface.get_rect
    * Surface.resize
    * Surface.copy
    * Surface.subsurface
    * Surface.getSubimage
    * Surface.blit
    * Surface.set_colorkey
    * Surface.get_colorkey
    * Surface.replace_color
    * Surface.get_at
    * Surface.set_at
    * Surface.fill
    * Surface.get_parent
    * Surface.get_offset
    * Surface.toDataURL
    """
    def __init__(self, size, *args, **kwargs):
        """
        Return Surface subclassed from a Canvas implementation.
        The size argument is the dimension (w,h) of surface.

        Module initialization places pyjsdl.Surface in module's namespace.
        """
        self.width = int(size[0])
        self.height = int(size[1])
        HTML5Canvas.__init__(self, self.width, self.height)
        HTML5Canvas.resize(self, self.width, self.height)
        self._display = None    #display surface
        self._super_surface = None
        self._offset = (0,0)
        self._colorkey = None
        self._nonimplemented_methods()

    def __repr__(self):
        """
        Return string representation of Surface object.
        """
        return "%s(%d,%d)" % (self.__class__, self.width, self.height)

    def get_size(self):
        """
        Return width and height of surface.
        """
        return (self.width, self.height)

    def get_width(self):
        """
        Return width of surface.
        """
        return self.width

    def get_height(self):
        """
        Return height of surface.
        """
        return self.height

    def resize(self, width, height):
        self.width = int(width)
        self.height = int(height)
        HTML5Canvas.resize(self, self.width, self.height)

    def get_rect(self, **attr):
        """
        Return rect of the surface.
        An optional keyword argument of the rect position.
        """
        rect = Rect(0, 0, self.width, self.height)
        for key in attr:
            rect.__setattr__(key,attr[key])
        return rect

    def copy(self):
        """
        Return Surface that is a copy of this surface.
        """
        surface = Surface((self.width,self.height))
        surface.drawImage(self.canvas, 0, 0)
        return surface

    def subsurface(self, rect):
        """
        Return Surface that represents a subsurface.
        The rect argument is the area of the subsurface.
        Argument can be 't'/'f' for data sync to/from subsurface.
        """
        if rect in ('t', 'f'):
            if not self._super_surface:
                return
            if rect == 't':
                self.drawImage(self._super_surface.canvas, self._offset[0], self._offset[1], self.width, self.height, 0, 0, self.width, self.height)
            else:
                self._super_surface.drawImage(self.canvas, self._offset[0], self._offset[1])
            return
        if hasattr(rect, 'width'):
            _rect = rect
        else:
            _rect = Rect(rect)
        surf_rect = self.get_rect()
        if not surf_rect.contains(_rect):
            raise ValueError('subsurface outside surface area')
        surface = self.getSubimage(_rect.x, _rect.y, _rect.width, _rect.height)
        surface._super_surface = self
        surface._offset = (_rect.x,_rect.y)
        surface._colorkey = self._colorkey
        return surface

    def getSubimage(self, x, y, width, height):
        """
        Return subimage of Surface.
        Arguments include x, y, width, and height of the subimage.
        """
        surface = Surface((width,height))
        surface.drawImage(self.canvas, x, y, width, height, 0, 0, width, height)
        return surface

    def blit(self, surface, position, area=None):
        """
        Draw given surface on this surface at position.
        Optional area delimitates the region of given surface to draw.
        """
        if not area:
            rect = rectPool.get(position[0],position[1],surface.width,surface.height)
            self.impl.canvasContext.drawImage(surface.canvas, rect.x, rect.y)
        else:
            rect = rectPool.get(position[0],position[1],area[2], area[3])
            self.impl.canvasContext.drawImage(surface.canvas, area[0], area[1], area[2], area[3], rect.x, rect.y, area[2], area[3])
        if self._display:
            surface_rect = self._display._surface_rect
        else:
            surface_rect = self.get_rect()
        changed_rect = surface_rect.clip(rect)
        rectPool.append(rect)
        return changed_rect

    def _blits(self, surfaces):
        ctx = self.impl.canvasContext
        for s in surfaces:
            ctx.drawImage(s.image.canvas, s.rect.x, s.rect.y)

    def _blit_clear(self, surface, rect_list):
        ctx = self.impl.canvasContext
        for r in rect_list:
            ctx.drawImage(surface.canvas, r.x,r.y,r.width,r.height, r.x,r.y,r.width,r.height)

    def set_colorkey(self, color, flags=None):
        """
        Set surface colorkey.
        """
        if self._colorkey:
            r = self._colorkey.r
            g = self._colorkey.g
            b = self._colorkey.b
            self._colorkey = None
        if color:
            try:
                color = Color(color)
                self._colorkey = color
                self.replace_color((color.r,color.g,color.b))
            except:
                pass
        return None

    def get_colorkey(self):
        """
        Return surface colorkey.
        """
        try:
            return self._colorkey.r, self._colorkey.g, self._colorkey.b, 255
        except (TypeError,AttributeError):      #-O/-S TypeError/AttributeError
            return None

    def _getPixel(self, imagedata, index):
        return JS("""imagedata.data[@{{index}}];""")

    def _setPixel(self, imagedata, index, dat):
        data = str(dat)
        JS("""imagedata.data[@{{index}}]=@{{data}};""")
        return

    def replace_color(self, color, new_color=None):
        """
        Replace color with with new_color or with alpha.
        """
        pixels = self.impl.getImageData(0, 0, self.width, self.height)
        if hasattr(color, 'a'):
            color1 = color
        else:
            color1 = Color(color)
        if new_color:
            if hasattr(new_color, 'a'):
                color2 = new_color
            else:
                color2 = Color(new_color)
        else:
            color2 = Color(color1.r,color1.g,color1.b,0)
        col1 = (color1.r, color1.g, color1.b, color1.a)
        col2 = (color2.r, color2.g, color2.b, color2.a)
        for i in xrange(0,len(pixels.data),4):
            if (self._getPixel(pixels, i), self._getPixel(pixels, i+1), self._getPixel(pixels, i+2), self._getPixel(pixels, i+3)) == col1:
                for j in range(4):
                    self._setPixel(pixels, i+j, col2[j])
        self.impl.putImageData(pixels, 0, 0, 0, 0, self.width, self.height)
        return None

    def get_at(self, pos):
        """
        Get color of a surface pixel. The pos argument represents x,y position of pixel.
        Return color (r,g,b,a) of a surface pixel.
        """
        pixel = self.impl.getImageData(pos[0], pos[1], 1, 1)
        return self._getPixel(pixel,0), self._getPixel(pixel,1), self._getPixel(pixel,2), self._getPixel(pixel,3)

    def set_at(self, pos, color):
        """
        Set color of a surface pixel.
        The arguments represent position x,y and color of pixel.
        """
        if hasattr(color, 'a'):
            _color = color
        else:
            _color = Color(color)
        self.setFillStyle(_color)
        self.fillRect(pos[0], pos[1], 1, 1)
        return None

    def fill(self, color=None, rect=None):
        """
        Fill surface with color.
        """
        if color is None:
            HTML5Canvas.fill(self)
            return
        if color:
            if hasattr(color, 'a'):
                self.setFillStyle(color)
            else:
                self.setFillStyle(Color(color))
            if not rect:
                _rect = Rect(0, 0, self.width, self.height)
            else:
                if self._display:
                    surface_rect = self._display._surface_rect
                else:
                    surface_rect = self.get_rect()
                if hasattr(rect, 'width'):
                    _rect = surface_rect.clip( rect )
                else:
                    _rect = surface_rect.clip( Rect(rect) )
                if not _rect.width or not _rect.height:
                    return _rect
            self.fillRect(_rect.x, _rect.y, _rect.width, _rect.height)
        else:
            _rect = Rect(0, 0, self.width, self.height)
            self.clear()
        return _rect

    def get_parent(self):
        """
        Return parent Surface of subsurface.
        """
        return self._super_surface   #if delete, delete subsurface...

    def get_offset(self):
        """
        Return offset of subsurface in surface.
        """
        return self._offset

    def toDataURL(self, datatype=None):
        """
        Return surface data as a base64 data string.
        Optional datatype to set data format, default to 'image/png'.
        Implemented with HTML5 Canvas toDataURL method.
        """
        if not datatype:
            return self.canvas.toDataURL()
        else:
            return self.canvas.toDataURL(datatype)

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.convert = lambda *arg: self
        self.convert_alpha = lambda *arg: self
        self.set_alpha = lambda *arg: None
        self.get_alpha = lambda *arg: None
        self.lock = lambda *arg: None
        self.unlock = lambda *arg: None
        self.mustlock = lambda *arg: False
        self.get_locked = lambda *arg: False
        self.get_locks = lambda *arg: ()


class Surf(object):

    def __init__(self, image):
        self.canvas = image
        self.width, self.height = self.canvas.width, self.canvas.height
        self._nonimplemented_methods()

    def get_size(self):
        return (self.width, self.height)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_rect(self, **attr):
        rect = Rect(0, 0, self.width, self.height)
        for key in attr:
            rect.__setattr__(key,attr[key])
        return rect

    def _nonimplemented_methods(self):
        self.convert = lambda *arg: self
        self.convert_alpha = lambda *arg: self
        self.set_alpha = lambda *arg: None
        self.get_alpha = lambda *arg: None
        self.lock = lambda *arg: None
        self.unlock = lambda *arg: None
        self.mustlock = lambda *arg: False
        self.get_locked = lambda *arg: False
        self.get_locks = lambda *arg: ()


class IndexSizeError(Exception):
    pass

