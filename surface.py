#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
from rect import Rect
from color import Color
from pyjamas.Canvas.HTML5Canvas import HTML5Canvas
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
    * Surface.blits
    * Surface.set_colorkey
    * Surface.get_colorkey
    * Surface.replace_color
    * Surface.get_at
    * Surface.set_at
    * Surface.fill
    * Surface.get_parent
    * Surface.get_offset
    """
    def __init__(self, size, *args, **kwargs):   #pyjs:instance creation seems long
        self.width, self.height = int(size[0]), int(size[1])
        HTML5Canvas.__init__(self, self.width, self.height)
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
        self.width, self.height = int(width), int(height)
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
        w, h = self.get_width(), self.get_height()
        surface = Surface((w,h))
        surface.drawImage(self.canvas, 0, 0)    #pyjs0.8 *.canvas
#        surface.drawImage(self, 0, 0)
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
        rect = Rect(rect)
        surf_rect = self.get_rect()
        if not surf_rect.contains(rect.x,rect.y) or not surf_rect.contains(rect.x+rect.width,rect.y+rect.height):
            raise ValueError, 'subsurface outside surface area'
        surface = self.getSubimage(rect.x, rect.y, rect.width, height)
        surface._super_surface = self
        surface._offset = (rect.x,rect.y)
        surface._colorkey = self._colorkey
        return surface

    def getSubimage(self, x, y, width, height):
        """
        Return subimage of Surface.
        Arguments include x, y, width, and height of the subimage.
        """
        surface = Surface((width,height))
        surface.drawImage(self.canvas, x, y, width, height, 0, 0, width, height)    #pyjs0.8 *.canvas
#        surface.drawImage(self, x, y, width, height, 0, 0, width, height)
        return surface

    def blit(self, surface, position, area=None):
        """
        Draw given surface on this surface at position.
        Optional area delimitates the region of given surface to draw.
        """
        if not area:
            rect = Rect(position[0],position[1],surface.width,surface.height)
            self.drawImage(surface.canvas, rect.x, rect.y)    #pyjs0.8 *.canvas
#            self.drawImage(surface, rect.x, rect.y)
        else:
            rect = Rect(position[0],position[1],area[2], area[3])
            self.drawImage(surface.canvas, area[0], area[1], area[2], area[3], rect.x, rect.y, area[2], area[3])    #pyjs0.8 *.canvas
#            self.drawImage(surface, area[0], area[1], area[2], area[3], rect.x, rect.y, area[2], area[3])
        return rect     #clipping?

    def blits(self, surfaces):
        """
        Draw list of (surface, rect) on this surface.
        """
        for surface in surfaces:
            try:
                x, y = surface[1].x, surface[1].y
            except AttributeError:
                x, y = surface[1][0], surface[1][1]
            self.drawImage(surface[0].canvas, x, y)    #pyjs0.8 *.canvas
#            self.drawImage(surface[0], x, y)
        return None

    def _blit_clear(self, surface, rect_list):
        for r in rect_list:
            try:
                self.drawImage(surface.canvas, r.x,r.y,r.width,r.height, r.x,r.y,r.width,r.height)    #pyjs0.8 *.canvas
#                self.drawImage(surface, r.x,r.y,r.width,r.height, r.x,r.y,r.width,r.height)
            except IndexSizeError:
                rx = surface.get_rect().clip(r)
                if rx.width and rx.height:
                    self.drawImage(surface.canvas, rx.x,rx.y,rx.width,rx.height, rx.x,rx.y,rx.width,rx.height)    #pyjs0.8 *.canvas
#                    self.drawImage(surface, rx.x,rx.y,rx.width,rx.height, rx.x,rx.y,rx.width,rx.height)

    def set_colorkey(self, color, flags=None):
        """
        Set surface colorkey.
        """
        if self._colorkey:
            r,g,b = self._colorkey.r,self._colorkey.g,self._colorkey.b
            self.replace_color((r,g,b,0),(r,g,b,255))
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
        dat = str(dat)
        JS("""imagedata.data[@{{index}}]=@{{dat}};""")
        return

    def replace_color(self, color, new_color=None):
        """
        Replace color with with new_color or with alpha.
        """
        pixels = self.impl.getImageData(0, 0, self.width, self.height)
#        pixels = self.getImageData(0, 0, self.width, self.height)
        color1 = Color(color)
        if new_color:
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
#        self.putImageData(pixels, 0, 0)
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
        pixel = self.impl.getImageData(pos[0], pos[1], 1, 1)
        color = Color(color)
        for i in range(4):
            self._setPixel(pixel, i, color[i])
        self.impl.putImageData(pixel, pos[0], pos[1], 0, 0, 1, 1)
        return None

    def fill(self, color=None, rect=None):
        """
        Fill surface with color.
        """
        if color is None:
            HTML5Canvas.fill(self)
            return
        self.beginPath()
        if color:
            self.setFillStyle(Color(color))
            if not rect:
                rect = Rect(0, 0, self.width, self.height)
            else:
                rect = self.get_rect().clip( Rect(rect) )
                if not rect.width or not rect.height:
                    return rect
            self.fillRect(rect.x, rect.y, rect.width, rect.height)
        else:
            rect = Rect(0, 0, self.width, self.height)
            self.clear()
        return rect

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


class Surf:

    def __init__(self, image):
        self.canvas = image
        element = image.getElement()
        self.width, self.height = element.width, element.height
        self.get_size = Surface.get_size
        self.get_width = Surface.get_width
        self.get_height = Surface.get_height
        self.get_rect = Surface.get_rect
        self._nonimplemented_methods = Surface._nonimplemented_methods
        self._nonimplemented_methods()


class IndexSizeError(Exception):
    pass

