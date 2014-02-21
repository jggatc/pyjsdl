#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
from math import pi
from rect import Rect
from surface import Surface
from color import Color

__docformat__ = 'restructuredtext'


class Draw(object):
    """
    **pyjsdl.draw**
    
    * pyjsdl.draw.rect
    * pyjsdl.draw.circle
    * pyjsdl.draw.ellipse
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
        rect = Rect(rect)
        surface.beginPath()
        if width:
            surface.setLineWidth(width)
            surface.setStrokeStyle(Color(color))
            surface.rect(rect.x, rect.y, rect.width, rect.height)
            surface.stroke()
        else:
            surface.setFillStyle(Color(color))
            surface.fillRect(rect.x, rect.y, rect.width, rect.height)
        return surface.get_rect().clip(rect)

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
            surface.setStrokeStyle(Color(color))
            surface.stroke()
        else:
            surface.setFillStyle(Color(color))
            surface.fill()
        return surface.get_rect().clip( Rect(position[0]-radius, position[1]-radius, 2*radius,2*radius) )

    def ellipse(self, surface, color, rect, width=0):
        """
        Draw ellipse shape, and returns bounding Rect.
        Argument include surface to draw, color, and rect.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        rect = Rect(rect)
        surface.saveContext()
        surface.translate(rect.x+int(rect.width/2), rect.y+int(rect.height/2))
        if rect.width >= rect.height:
            surface.scale(rect.width/rect.height, 1)
            radius = rect.height/2
        else:
            surface.scale(1, rect.height/rect.width)
            radius = rect.width/2
        surface.beginPath()
        surface.arc(0, 0, radius, 0, 2*pi, False)
        if width:
            surface.setLineWidth(width)
            surface.setStrokeStyle(Color(color))
            surface.stroke()
        else:
            surface.setFillStyle(Color(color))
            surface.fill()
        surface.restoreContext()
        return surface.get_rect().clip(rect)

    def arc(self, surface, color, rect, start_angle, stop_angle, width=1):
        """
        Draw arc shape, and returns bounding Rect.
        Argument include surface to draw, color, rect, start_angle, stop_angle.
        Optional width argument of outline.
        """
        rect = Rect(rect)
        if rect.width == rect.height:
            surface.beginPath()
            surface.arc(rect.x+int(rect.width/2), rect.y+int(rect.height/2), int(rect.width/2), -start_angle, -stop_angle, True)
            if width:
                surface.setLineWidth(width)
                surface.setStrokeStyle(Color(color))
                surface.stroke()
            else:
                surface.closePath()
                surface.setFillStyle(Color(color))
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
                surf.setStrokeStyle(Color(color))
                surf.stroke()
            else:
                surface.closePath()
                surf.setFillStyle(Color(color))
                surf.fill()
            surface.drawImage(surf.canvas, 0, 0, dim, dim, rect.x, rect.y, rect.width, rect.height)    #pyjs0.8 *.canvas
#            surface.drawImage(surf, 0, 0, dim, dim, rect.x, rect.y, rect.width, rect.height)
        return surface.get_rect().clip(rect)

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
            surface.setStrokeStyle(Color(color))
            surface.stroke()
        else:
            surface.setFillStyle(Color(color))
            surface.fill()
        xpts = [pt[0] for pt in pointlist]
        ypts = [pt[1] for pt in pointlist]
        xmin, xmax = min(xpts), max(xpts)
        ymin, ymax = min(ypts), max(ypts)
        return surface.get_rect().clip( Rect(xmin,ymin,xmax-xmin+1,ymax-ymin+1) )

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
        surface.setStrokeStyle(Color(color))
        surface.stroke()
        xpts = [pt[0] for pt in (point1,point2)]
        ypts = [pt[1] for pt in (point1,point2)]
        xmin, xmax = min(xpts), max(xpts)
        ymin, ymax = min(ypts), max(ypts)
        return surface.get_rect().clip( Rect(xmin,ymin,xmax-xmin+1,ymax-ymin+1) )

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
        surface.setStrokeStyle(Color(color))
        surface.stroke()
        xpts = [pt[0] for pt in pointlist]
        ypts = [pt[1] for pt in pointlist]
        xmin, xmax = min(xpts), max(xpts)
        ymin, ymax = min(ypts), max(ypts)
        return surface.get_rect().clip( Rect(xmin,ymin,xmax-xmin+1,ymax-ymin+1) )

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

