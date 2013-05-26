#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
from rect import Rect
try:    ###0.15
    from pyjamas.Canvas.HTML5Canvas import HTML5Canvas      ###>IE9
except ImportError:
    from pyjamas.Canvas.GWTCanvas import GWTCanvas as HTML5Canvas
from pyjamas.Canvas import Color
from __pyjamas__ import JS      ###0.15

__docformat__ = 'restructuredtext'


class Surface(HTML5Canvas):      ###0.15
    """
    **pyjsdl.Surface**
    
    * Surface.get_size
    * Surface.get_width
    * Surface.get_height
    * Surface.get_rect
    * Surface.copy
    * Surface.subsurface
    * Surface.subarea
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
    def __init__(self, size):   ###pyjs:instance creation seems long
        HTML5Canvas.__init__(self, size[0], size[1])     ###0.15
        self.width = size[0]
        self.height = size[1]
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
        surface.drawImage(self.canvas, 0, 0)    ###pyjs0.8 *.canvas
#        surface.drawImage(self, 0, 0)
        return surface

    def subsurface(self, *rect):
        """
        Return Surface that represents a subsurface.
        The rect argument is the area of the subsurface.
        """
        surface, rect = self.subarea(*rect)     ###subarea copied, data not shared
        return surface

    def subarea(self, *rect):
        """
        Return Surface and Rect that represents a subsurface.
        The rect argument is the area of the subsurface.
        """
        try:
            x,y,w,h = rect[0].x, rect[0].y, rect[0].width, rect[0].height
        except:
#        except AttributeError:
            try:
                x,y,w,h = rect[0]
            except:
#            except ValueError:
                x,y = rect[0]
                w,h = rect[1]
        rect = Rect(x, y, w, h)
        subsurf = self.getSubimage(rect.x, rect.y, rect.width, rect.height)     #bounding 
        return subsurf, rect

    def getSubImage(self, x, y, width, height):
        surf = Surface((width,height))
        surf.drawImage(self.canvas, x, y, width, height, 0, 0, width, height)    ###pyjs0.8 *.canvas
#        surf.drawImage(self, x, y, width, height, 0, 0, width, height)
        return surf

    def blit(self, surface, position, area=None):
        """
        Draw given surface on this surface at position.
        Optional area delimitates the region of given surface to draw.
        """
        x, y = position[0], position[1]
        if not area:
            self.drawImage(surface.canvas, x, y)    ###pyjs0.8 *.canvas
#            self.drawImage(surface, x, y)
            rect = Rect(x,y,surface.width,surface.height)
        else:
            sx, sy, sw, sh = area
            self.drawImage(surface.canvas, sx, sy, sw, sh, x, y, sw, sh)    ###pyjs0.8 *.canvas
#            self.drawImage(surface, sx, sy, sw, sh, x, y, sw, sh)
            rect = Rect(x,y,sw,sh)     ###0.14
        return rect     ###0.14     #clipping?

    def blits(self, surfaces):  ###
        """
        Draw list of (surface, rect) on this surface.
        """
        for surface in surfaces:
            try:
                x, y = surface[1].x, surface[1].y
            except AttributeError:
                x, y = surface[1][0], surface[1][1]
            self.drawImage(surface[0].canvas, x, y)    ###pyjs0.8 *.canvas
#            self.drawImage(surface[0], x, y)
        return None

    def _blit_clear(self, surface, rect_list):
        for r in rect_list:
            try:
                self.drawImage(surface.canvas, r.x,r.y,r.width,r.height, r.x,r.y,r.width,r.height)    ###pyjs0.8 *.canvas
#                self.drawImage(surface, r.x,r.y,r.width,r.height, r.x,r.y,r.width,r.height)
            except:     #IndexSizeError (pyjs: unknown exception)
                rx = surface.get_rect().clip(r)
                if rx.width and rx.height:
                    self.drawImage(surface.canvas, rx.x,rx.y,rx.width,rx.height, rx.x,rx.y,rx.width,rx.height)    ###pyjs0.8 *.canvas            
#                    self.drawImage(surface, rx.x,rx.y,rx.width,rx.height, rx.x,rx.y,rx.width,rx.height)

    def set_colorkey(self, color, flags=None):      ###0.15
        """
        Set surface colorkey.
        """
        if self._colorkey:
            r,g,b = self._colorkey
            self.replace_color((r,g,b,0),(r,g,b,255))
            self._colorkey = None
        if color:
            try:
                self.replace_color(color)
                self._colorkey = color
            except:
                pass
        return None

    def get_colorkey(self):
        """
        Return surface colorkey.
        """
        return self._colorkey

    def _getPixel(self, imagedata, index):     ###0.15
        return JS("""imagedata.data[@{{index}}];""")

    def _setPixel(self, imagedata, index, dat):     ###0.15
        dat = str(dat)
        JS("""imagedata.data[@{{index}}]=@{{dat}};""")
        return

    def replace_color(self, color, new_color=None):     ###0.15
        """
        Replace color with with new_color or with alpha.
        """
        pixels = self.impl.getImageData(0, 0, self.width, self.height)
#        pixels = self.getImageData(0, 0, self.width, self.height)
        color = list(color)
        if new_color:
            new_color = list(new_color)
        else:
            new_color = [color[0], color[1], color[2], 0]
        c_len = len(color)
        nc_len = len(new_color)
        for i in xrange(0,len(pixels.data),4):
            col = []
            for j in range(4):
                col.append( self._getPixel(pixels, i+j) )
            if col[0:c_len] == color:
                for j in range(nc_len):
                    self._setPixel(pixels, i+j, new_color[j])
        self.impl.putImageData(pixels, 0, 0, 0, 0, self.width, self.height)
#        self.putImageData(pixels, 0, 0)
        return None

    def get_at(self, pos):      ###0.15
        """
        Get color of a surface pixel. The pos argument represents x,y position of pixel.
        Return color (r,g,b,a) of a surface pixel.
        """
        pixel = self.impl.getImageData(pos[0], pos[1], 1, 1)
        col = []
        for i in range(4):
            col.append( self._getPixel(pixel, i) )
        return col

    def set_at(self, pos, color):      ###0.15
        """
        Set color of a surface pixel.
        The arguments represent position x,y and color of pixel.
        """
        pixel = self.impl.getImageData(pos[0], pos[1], 1, 1)
        for i in range(len(color)):
            self._setPixel(pixel, i, color[i])
        self.impl.putImageData(pixel, pos[0], pos[1], 0, 0, 1, 1)
        return None

    def fill(self, color=None, rect=None):
        """
        Fill surface with color.
        """
        if color is None:
            HTML5Canvas.fill(self)    ###0.15
            return
        self.beginPath()
        if color:
            if len(color) == 3:
                self.setFillStyle(Color.Color(color[0],color[1],color[2]))  ###0.15
            elif len(color) == 4:
                self.setFillStyle(Color.Color(color[0],color[1],color[2],color[3])) ###0.15
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

