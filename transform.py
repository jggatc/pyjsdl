#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

#from __future__ import division
import math
from surface import Surface

__docformat__ = 'restructuredtext'


class Transform(object):
    """
    **pyjsdl.transform**
    
    * pyjsdl.transform.rotate
    * pyjsdl.transform.rotozoom
    * pyjsdl.transform.scale
    * pyjsdl.transform.smoothscale
    * pyjsdl.transform.scale2x
    * pyjsdl.transform.flip
    """

    def __init__(self):
        """
        Provides image transformation methods.

        Module initialization creates pyjsdl.transform instance.
        """
        self.deg_rad = math.pi/180.0    #180>180.0

    def rotate(self, surface, angle):
        """
        Return Surface rotated by the given angle.
        """
        if not angle:
            return surface.copy()
        theta = angle*self.deg_rad
        width_i = surface.get_width()
        height_i = surface.get_height()
        cos_theta = math.fabs( math.cos(theta) )
        sin_theta = math.fabs( math.sin(theta) )
        width_f = int( (width_i*cos_theta)+(height_i*sin_theta) )
        height_f = int( (width_i*sin_theta)+(height_i*cos_theta) )
        if width_f%2:
            width_f += 1
        if height_f%2:
            height_f += 1
        surf = Surface((width_f,height_f))
        surf.saveContext()
        surf.translate(width_f/2.0, height_f/2.0)
        surf.rotate(-theta)
        surf.drawImage(surface.canvas, -width_i/2, -height_i/2)    #pyjs0.8 *.canvas
#        surf.drawImage(surface, -width_i/2, -height_i/2)
        surf.restoreContext()
        return surf

    def rotozoom(self, surface, angle, size):
        """
        Return Surface rotated and resized by the given angle and size.
        """
        surf = self.rotate(surface, angle)
        w, h = int(math.ceil(surf.get_width()*size)), int(math.ceil(surf.get_height()*size))
        if w % 2:
            w += 1
        if h % 2:
            h += 1
        surf = self.scale(surf, (w, h))
        return surf

    def scale(self, surface, size, dest=None):
        """
        Return Surface resized by the given size.
        An optional destination surface can be provided.
        """
        if not dest:
            surf = Surface(size)
        else:
            surf = dest
        surf.drawImage(surface.canvas, 0, 0, surface.get_width(), surface.get_height(), 0, 0, size[0], size[1])    #pyjs0.8 *.canvas
#        surf.drawImage(surface, 0, 0, surface.get_width(), surface.get_height(), 0, 0, size[0], size[1])
        return surf

    def smoothscale(self, surface, size):
        """
        Calls scale().
        Return Surface resized by the given size.
        """
        return self.scale(surface, size)

    def scale2x(self, surface, dest=None):
        """
        Return Surface resized to twice its size.
        An optional destination surface can be provided.
        """
        return self.scale(surface, (surface.get_width()*2,surface.get_height()*2), dest)

    def flip(self, surface, xbool=True, ybool=False):
        """
        Return Surface that is flipped horizontally, vertically, or both.
        """
        surf = Surface((surface.get_width(),surface.get_height()))
        surf.saveContext()
        if xbool and ybool:
            surf.translate(surface.get_width(), surface.get_height())
            surf.scale(-1, -1)
        elif xbool:
            surf.translate(surface.get_width(), 0)
            surf.scale(-1, 1)
        elif ybool:
            surf.translate(0, surface.get_height())
            surf.scale(1, -1)
        surf.drawImage(surface.canvas, 0, 0)    #pyjs0.8 *.canvas
#        surf.drawImage(surface, 0, 0)
        surf.restoreContext()
        return surf

