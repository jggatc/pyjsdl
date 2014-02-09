#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
from math import pi
from rect import Rect
from surface import Surface
from color import Color     #0.18

__docformat__ = 'restructuredtext'


class Draw(object):
    """
    **pyjsdl.draw**
    
    * pyjsdl.draw.rect
    * pyjsdl.draw.circle
    * pyjsdl.draw.arc
    * pyjsdl.draw.polygon
    * pyjsdl.draw.line
    * pyjsdl.draw.lines
    * pyjsdl.draw.aaline
    * pyjsdl.draw.aalines
    """

    def __init__(self):
        """
        Draw shapes.
        
        Module initialization creates pyjsdl.draw instance.        
        """
        self.rad_deg = 180.0/pi

    def rect(self, surface, color, rect, width=0):
        """
        Draw rectangle shape, and returns bounding Rect.
        Argument include surface to draw, color, Rect.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        rect = Rect(rect)   #0.18
        surface.beginPath()
        if width:
            surface.setLineWidth(width)
            surface.setStrokeStyle(Color(color))     #0.18
            surface.rect(rect.x, rect.y, rect.width, rect.height)
            surface.stroke()
        else:
            surface.setFillStyle(Color(color))   #0.18
            surface.fillRect(rect.x, rect.y, rect.width, rect.height)
        return surface.get_rect().clip(rect)   #0.18

    def circle(self, surface, color, position, radius, width=0):
        """
        Draw circular shape, and returns bounding Rect.
        Argument include surface to draw, color, position and radius.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        surface.beginPath()
        surface.arc(position[0], position[1], radius, 0, 2*pi, False)
        if width:
            surface.setLineWidth(width)
            surface.setStrokeStyle(Color(color))     #0.18
            surface.stroke()
        else:
            surface.setFillStyle(Color(color))   #0.18
            surface.fill()
        return surface.get_rect().clip( Rect(position[0]-radius, position[1]-radius, 2*radius,2*radius) )   #0.18

    def arc(self, surface, color, rect, start_angle, stop_angle, width=1):
        """
        Draw arc shape, and returns bounding Rect.
        Argument include surface to draw, color, rect, start_angle, stop_angle.
        Optional width argument of outline.
        """
        rect = Rect(rect)   #0.18
        if rect.width == rect.height:
            surface.beginPath()
            surface.arc(rect.x+int(rect.width/2), rect.y+int(rect.height/2), int(rect.width/2), -start_angle, -stop_angle, True)
            if width:
                surface.setLineWidth(width)
                surface.setStrokeStyle(Color(color))     #0.18
                surface.stroke()
            else:
                surface.closePath()
                surface.setFillStyle(Color(color))   #0.18
                surface.fill()
        else:
            if rect.width < rect.height:
                dim = rect.height
            else:
                dim = rect.width
            surf = Surface((dim,dim))
            surf.beginPath()
            xdim = int(dim/2)
            surf.arc(xdim, xdim, xdim, -start_angle, -stop_angle, True)
            if width:
                surf.setLineWidth(width)
                surf.setStrokeStyle(Color(color))    #0.18
                surf.stroke()
            else:
                surface.closePath()
                surf.setFillStyle(Color(color))  #0.18
                surf.fill()
            surface.drawImage(surf.canvas, 0, 0, dim, dim, rect.x, rect.y, rect.width, rect.height)    ###pyjs0.8 *.canvas
#            surface.drawImage(surf, 0, 0, dim, dim, rect.x, rect.y, rect.width, rect.height)
        return surface.get_rect().clip(rect)   #0.18

    def polygon(self, surface, color, pointlist, width=0):
        """
        Draw polygon shape, and returns bounding Rect.
        Argument include surface to draw, color, and pointlist.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        surface.beginPath()
        surface.moveTo(*pointlist[0])
        for point in pointlist[1:]:
            surface.lineTo(*point)
        surface.closePath()
        if width:
            surface.setLineWidth(width)
            surface.setStrokeStyle(Color(color))     #0.18
            surface.stroke()
        else:
            surface.setFillStyle(Color(color))   #0.18
            surface.fill()
        xpts = [pt[0] for pt in pointlist]
        ypts = [pt[1] for pt in pointlist]
        xmin, xmax = min(xpts), max(xpts)
        ymin, ymax = min(ypts), max(ypts)
        return surface.get_rect().clip( Rect(xmin,ymin,xmax-xmin+1,ymax-ymin+1) )   #0.18

    def line(self, surface, color, point1, point2, width=1):
        """
        Draw line, and returns bounding Rect.
        Argument include surface to draw, color, point1, point2.
        Optional width argument of line.
        """
        surface.beginPath()
        surface.moveTo(*point1)
        surface.lineTo(*point2)
        surface.setLineWidth(width)
        surface.setStrokeStyle(Color(color))     #0.18
        surface.stroke()
        xpts = [pt[0] for pt in (point1,point2)]
        ypts = [pt[1] for pt in (point1,point2)]
        xmin, xmax = min(xpts), max(xpts)
        ymin, ymax = min(ypts), max(ypts)
        return surface.get_rect().clip( Rect(xmin,ymin,xmax-xmin+1,ymax-ymin+1) )   #0.18

    def lines(self, surface, color, closed, pointlist, width=1):
        """
        Draw interconnected lines, and returns Rect bound.
        Argument include surface to draw, color, closed, and pointlist.
        Optional width argument of line.
        """
        surface.beginPath()
        surface.moveTo(*pointlist[0])
        for point in pointlist[1:]:
            surface.lineTo(*point)
        if closed:
            surface.closePath()
        surface.setLineWidth(width)
        surface.setStrokeStyle(Color(color))     #0.18
        surface.stroke()
        xpts = [pt[0] for pt in pointlist]
        ypts = [pt[1] for pt in pointlist]
        xmin, xmax = min(xpts), max(xpts)
        ymin, ymax = min(ypts), max(ypts)
        return surface.get_rect().clip( Rect(xmin,ymin,xmax-xmin+1,ymax-ymin+1) )   #0.18

    def aaline(self, surface, color, point1, point2, blend=1):
        """
        Calls line(), return bounding Rect.
        """
        rect = self.line(surface, color, point1, point2, blend)
        return rect

    def aalines(self, surface, color, closed, pointlist, blend=1):
        """
        Calls lines(), return bounding Rect.
        """
        rect = self.lines(surface, color, closed, pointlist, blend)
        return rect

