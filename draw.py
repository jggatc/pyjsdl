#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from math import pi as _pi
from pyjsdl.rect import Rect
from pyjsdl.surface import Surface
from pyjsdl.color import Color

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
        self.rad_deg = 180.0/_pi

    def rect(self, surface, color, rect, width=0):
        """
        Draw rectangle shape, and returns bounding Rect.
        Argument include surface to draw, color, Rect.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        if hasattr(rect, 'width'):
            _rect = rect
        else:
            _rect = Rect(rect)
        if width:
            surface.setLineWidth(width)
            if hasattr(color, 'a'):
                surface.setStrokeStyle(color)
            else:
                surface.setStrokeStyle(Color(color))
            surface.strokeRect(_rect.x, _rect.y, _rect.width, _rect.height)
        else:
            if hasattr(color, 'a'):
                surface.setFillStyle(color)
            else:
                surface.setFillStyle(Color(color))
            surface.fillRect(_rect.x, _rect.y, _rect.width, _rect.height)
        if surface._display:
            return surface._display._surface_rect.clip(_rect)
        else:
            return surface.get_rect().clip(_rect)

    def circle(self, surface, color, position, radius, width=0):
        """
        Draw circular shape, and returns bounding Rect.
        Argument include surface to draw, color, position and radius.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        surface.beginPath()
        surface.arc(position[0], position[1], radius, 0, 2*_pi, False)
        if width:
            surface.setLineWidth(width)
            if hasattr(color, 'a'):
                surface.setStrokeStyle(color)
            else:
                surface.setStrokeStyle(Color(color))
            surface.stroke()
        else:
            if hasattr(color, 'a'):
                surface.setFillStyle(color)
            else:
                surface.setFillStyle(Color(color))
            surface.fill()
        if surface._display:
            return surface._display._surface_rect.clip( Rect(position[0]-radius, position[1]-radius, 2*radius, 2*radius) )
        else:
            return surface.get_rect().clip( Rect(position[0]-radius, position[1]-radius, 2*radius, 2*radius) )

    def ellipse(self, surface, color, rect, width=0):
        """
        Draw ellipse shape, and returns bounding Rect.
        Argument include surface to draw, color, and rect.
        Optional width argument of outline, which defaults to 0 for filled shape.
        """
        if hasattr(rect, 'width'):
            _rect = rect
        else:
            _rect = Rect(rect)
        surface.saveContext()
        surface.translate(_rect.x+int(_rect.width/2), _rect.y+int(_rect.height/2))
        if _rect.width >= _rect.height:
            surface.scale(_rect.width/(_rect.height*1.0), 1)
            radius = _rect.height/2
        else:
            surface.scale(1, _rect.height/(_rect.width*1.0))
            radius = _rect.width/2
        surface.beginPath()
        surface.arc(0, 0, radius, 0, 2*_pi, False)
        if width:
            surface.setLineWidth(width)
            if hasattr(color, 'a'):
                surface.setStrokeStyle(color)
            else:
                surface.setStrokeStyle(Color(color))
            surface.stroke()
        else:
            if hasattr(color, 'a'):
                surface.setFillStyle(color)
            else:
                surface.setFillStyle(Color(color))
            surface.fill()
        surface.restoreContext()
        if surface._display:
            return surface._display._surface_rect.clip(_rect)
        else:
            return surface.get_rect().clip(_rect)

    def arc(self, surface, color, rect, start_angle, stop_angle, width=1):
        """
        Draw arc shape, and returns bounding Rect.
        Argument include surface to draw, color, rect, start_angle, stop_angle.
        Optional width argument of outline.
        """
        if hasattr(rect, 'width'):
            _rect = rect
        else:
            _rect = Rect(rect)
        if _rect.width == _rect.height:
            surface.beginPath()
            surface.arc(_rect.x+int(_rect.width/2), _rect.y+int(_rect.height/2), int(_rect.width/2), -start_angle, -stop_angle, True)
            if width:
                surface.setLineWidth(width)
                if hasattr(color, 'a'):
                    surface.setStrokeStyle(color)
                else:
                    surface.setStrokeStyle(Color(color))
                surface.stroke()
            else:
                surface.closePath()
                if hasattr(color, 'a'):
                    surface.setFillStyle(color)
                else:
                    surface.setFillStyle(Color(color))
                surface.fill()
        else:
            surface.saveContext()
            surface.translate(_rect.x+int(_rect.width/2), _rect.y+int(_rect.height/2))
            if _rect.width >= _rect.height:
                surface.scale(_rect.width/(_rect.height*1.0), 1)
                radius = _rect.height/2
            else:
                surface.scale(1, _rect.height/(_rect.width*1.0))
                radius = _rect.width/2
            surface.beginPath()
            surface.arc(0, 0, radius, -start_angle, -stop_angle, True)
            if width:
                surface.setLineWidth(width)
                if hasattr(color, 'a'):
                    surface.setStrokeStyle(color)
                else:
                    surface.setStrokeStyle(Color(color))
                surface.stroke()
            else:
                surface.closePath()
                if hasattr(color, 'a'):
                    surface.setFillStyle(color)
                else:
                    surface.setFillStyle(Color(color))
                surface.fill()
            surface.restoreContext()
        if surface._display:
            return surface._display._surface_rect.clip(_rect)
        else:
            return surface.get_rect().clip(_rect)

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
            if hasattr(color, 'a'):
                surface.setStrokeStyle(color)
            else:
                surface.setStrokeStyle(Color(color))
            surface.stroke()
        else:
            if hasattr(color, 'a'):
                surface.setFillStyle(color)
            else:
                surface.setFillStyle(Color(color))
            surface.fill()
        xpts = [pt[0] for pt in pointlist]
        ypts = [pt[1] for pt in pointlist]
        xmin, xmax = min(xpts), max(xpts)
        ymin, ymax = min(ypts), max(ypts)
        if surface._display:
            return surface._display._surface_rect.clip( Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1) )
        else:
            return surface.get_rect().clip( Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1) )

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
        if hasattr(color, 'a'):
            surface.setStrokeStyle(color)
        else:
            surface.setStrokeStyle(Color(color))
        surface.stroke()
        xpts = [pt[0] for pt in (point1,point2)]
        ypts = [pt[1] for pt in (point1,point2)]
        xmin, xmax = min(xpts), max(xpts)
        ymin, ymax = min(ypts), max(ypts)
        if surface._display:
            return surface._display._surface_rect.clip( Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1) )
        else:
            return surface.get_rect().clip( Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1) )

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
        if hasattr(color, 'a'):
            surface.setStrokeStyle(color)
        else:
            surface.setStrokeStyle(Color(color))
        surface.stroke()
        xpts = [pt[0] for pt in pointlist]
        ypts = [pt[1] for pt in pointlist]
        xmin, xmax = min(xpts), max(xpts)
        ymin, ymax = min(ypts), max(ypts)
        if surface._display:
            return surface._display._surface_rect.clip( Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1) )
        else:
            return surface.get_rect().clip( Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1) )

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

