#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from math import pi as _pi
from pyjsdl.rect import Rect
from pyjsdl.color import Color

__docformat__ = 'restructuredtext'

__doc__ = 'Draw shapes'


_return_rect = True


def rect(surface, color, rect, width=0):
    """
    Draw rectangle shape, and returns bounding Rect.
    Arguments include surface to draw, color, Rect.
    Optional width argument of outline, which defaults to 0 for filled shape.
    """
    if hasattr(rect, 'width'):
        _rect = rect
    else:
        _rect = Rect(rect)
    if width:
        surface.setLineWidth(width)
        if surface._stroke_style != color:
            surface._stroke_style = color
            if hasattr(color, 'a'):
                surface.setStrokeStyle(color)
            else:
                surface.setStrokeStyle(Color(color))
        surface.strokeRect(_rect.x, _rect.y, _rect.width, _rect.height)
    else:
        if surface._fill_style != color:
            surface._fill_style = color
            if hasattr(color, 'a'):
                surface.setFillStyle(color)
            else:
                surface.setFillStyle(Color(color))
        surface.fillRect(_rect.x, _rect.y, _rect.width, _rect.height)
    if not _return_rect:
        return None
    if surface._display:
        return surface._display._surface_rect.clip(_rect)
    else:
        return surface.get_rect().clip(_rect)


def circle(surface, color, position, radius, width=0):
    """
    Draw circular shape, and returns bounding Rect.
    Arguments include surface to draw, color, position and radius.
    Optional width argument of outline, which defaults to 0 for filled shape.
    """
    surface.beginPath()
    surface.arc(position[0], position[1], radius, 0, 2*_pi, False)
    if width:
        surface.setLineWidth(width)
        if surface._stroke_style != color:
            surface._stroke_style = color
            if hasattr(color, 'a'):
                surface.setStrokeStyle(color)
            else:
                surface.setStrokeStyle(Color(color))
        surface.stroke()
    else:
        if surface._fill_style != color:
            surface._fill_style = color
            if hasattr(color, 'a'):
                surface.setFillStyle(color)
            else:
                surface.setFillStyle(Color(color))
        surface.fill()
    if not _return_rect:
        return None
    if surface._display:
        return surface._display._surface_rect.clip(
            Rect(position[0]-radius, position[1]-radius, 2*radius, 2*radius))
    else:
        return surface.get_rect().clip(
            Rect(position[0]-radius, position[1]-radius, 2*radius, 2*radius))


def ellipse(surface, color, rect, width=0):
    """
    Draw ellipse shape, and returns bounding Rect.
    Arguments include surface to draw, color, and rect.
    Optional width argument of outline, which defaults to 0 for filled shape.
    """
    if hasattr(rect, 'width'):
        _rect = rect
    else:
        _rect = Rect(rect)
    surface.saveContext()
    surface.translate(_rect.x + int(_rect.width/2),
                      _rect.y + int(_rect.height/2))
    if _rect.width >= _rect.height:
        surface.scale(_rect.width / (_rect.height*1.0), 1)
        radius = int(_rect.height/2)
    else:
        surface.scale(1, _rect.height / (_rect.width*1.0))
        radius = int(_rect.width/2)
    surface.beginPath()
    surface.arc(0, 0, radius, 0, 2*_pi, False)
    if width:
        surface.setLineWidth(width)
        if surface._stroke_style != color:
            surface._stroke_style = color
            if hasattr(color, 'a'):
                surface.setStrokeStyle(color)
            else:
                surface.setStrokeStyle(Color(color))
        surface.stroke()
    else:
        if surface._fill_style != color:
            surface._fill_style = color
            if hasattr(color, 'a'):
                surface.setFillStyle(color)
            else:
                surface.setFillStyle(Color(color))
        surface.fill()
    surface.restoreContext()
    if not _return_rect:
        return None
    if surface._display:
        return surface._display._surface_rect.clip(_rect)
    else:
        return surface.get_rect().clip(_rect)


def arc(surface, color, rect, start_angle, stop_angle, width=1):
    """
    Draw arc shape, and returns bounding Rect.
    Arguments include surface to draw, color, rect, start_angle, stop_angle.
    Optional width argument of outline.
    """
    if hasattr(rect, 'width'):
        _rect = rect
    else:
        _rect = Rect(rect)
    if _rect.width == _rect.height:
        surface.beginPath()
        surface.arc(_rect.x + int(_rect.width/2), _rect.y + int(_rect.height/2),
                    int(_rect.width/2), -start_angle, -stop_angle, True)
        if width:
            surface.setLineWidth(width)
            if surface._stroke_style != color:
                surface._stroke_style = color
                if hasattr(color, 'a'):
                    surface.setStrokeStyle(color)
                else:
                    surface.setStrokeStyle(Color(color))
            surface.stroke()
        else:
            surface.closePath()
            if surface._fill_style != color:
                surface._fill_style = color
                if hasattr(color, 'a'):
                    surface.setFillStyle(color)
                else:
                    surface.setFillStyle(Color(color))
            surface.fill()
    else:
        surface.saveContext()
        surface.translate(_rect.x + int(_rect.width/2),
                          _rect.y + int(_rect.height/2))
        if _rect.width >= _rect.height:
            surface.scale(_rect.width / (_rect.height*1.0), 1)
            radius = int(_rect.height/2)
        else:
            surface.scale(1, _rect.height / (_rect.width*1.0))
            radius = int(_rect.width/2)
        surface.beginPath()
        surface.arc(0, 0, radius, -start_angle, -stop_angle, True)
        if width:
            surface.setLineWidth(width)
            if surface._stroke_style != color:
                surface._stroke_style = color
                if hasattr(color, 'a'):
                    surface.setStrokeStyle(color)
                else:
                    surface.setStrokeStyle(Color(color))
            surface.stroke()
        else:
            surface.closePath()
            if surface._fill_style != color:
                surface._fill_style = color
                if hasattr(color, 'a'):
                    surface.setFillStyle(color)
                else:
                    surface.setFillStyle(Color(color))
            surface.fill()
        surface.restoreContext()
    if not _return_rect:
        return None
    if surface._display:
        return surface._display._surface_rect.clip(_rect)
    else:
        return surface.get_rect().clip(_rect)


def polygon(surface, color, pointlist, width=0):
    """
    Draw polygon shape, and returns bounding Rect.
    Arguments include surface to draw, color, and pointlist.
    Optional width argument of outline, which defaults to 0 for filled shape.
    """
    surface.beginPath()
    surface.moveTo(*pointlist[0])
    for point in pointlist[1:]:
        surface.lineTo(*point)
    surface.closePath()
    if width:
        surface.setLineWidth(width)
        if surface._stroke_style != color:
            surface._stroke_style = color
            if hasattr(color, 'a'):
                surface.setStrokeStyle(color)
            else:
                surface.setStrokeStyle(Color(color))
        surface.stroke()
    else:
        if surface._fill_style != color:
            surface._fill_style = color
            if hasattr(color, 'a'):
                surface.setFillStyle(color)
            else:
                surface.setFillStyle(Color(color))
        surface.fill()
    if not _return_rect:
        return None
    xpts = [pt[0] for pt in pointlist]
    ypts = [pt[1] for pt in pointlist]
    xmin, xmax = min(xpts), max(xpts)
    ymin, ymax = min(ypts), max(ypts)
    if surface._display:
        return surface._display._surface_rect.clip(
            Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1))
    else:
        return surface.get_rect().clip(
            Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1))


def line(surface, color, point1, point2, width=1):
    """
    Draw line, and returns bounding Rect.
    Arguments include surface to draw, color, point1, point2.
    Optional width argument of line.
    """
    surface.beginPath()
    surface.moveTo(*point1)
    surface.lineTo(*point2)
    surface.setLineWidth(width)
    if surface._stroke_style != color:
        surface._stroke_style = color
        if hasattr(color, 'a'):
            surface.setStrokeStyle(color)
        else:
            surface.setStrokeStyle(Color(color))
    surface.stroke()
    if not _return_rect:
        return None
    xpts = [pt[0] for pt in (point1,point2)]
    ypts = [pt[1] for pt in (point1,point2)]
    xmin, xmax = min(xpts), max(xpts)
    ymin, ymax = min(ypts), max(ypts)
    if surface._display:
        return surface._display._surface_rect.clip(
            Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1))
    else:
        return surface.get_rect().clip(
            Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1))


def lines(surface, color, closed, pointlist, width=1):
    """
    Draw interconnected lines, and returns Rect bound.
    Arguments include surface to draw, color, closed, and pointlist.
    Optional width argument of line.
    """
    surface.beginPath()
    surface.moveTo(*pointlist[0])
    for point in pointlist[1:]:
        surface.lineTo(*point)
    if closed:
        surface.closePath()
    surface.setLineWidth(width)
    if surface._stroke_style != color:
        surface._stroke_style = color
        if hasattr(color, 'a'):
            surface.setStrokeStyle(color)
        else:
            surface.setStrokeStyle(Color(color))
    surface.stroke()
    if not _return_rect:
        return None
    xpts = [pt[0] for pt in pointlist]
    ypts = [pt[1] for pt in pointlist]
    xmin, xmax = min(xpts), max(xpts)
    ymin, ymax = min(ypts), max(ypts)
    if surface._display:
        return surface._display._surface_rect.clip(
            Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1))
    else:
        return surface.get_rect().clip(
            Rect(xmin, ymin, xmax-xmin+1, ymax-ymin+1))


def aaline(surface, color, point1, point2, blend=1):
    """
    Draw line, and returns bounding Rect.
    Arguments include surface to draw, color, point1, point2.
    """
    rect = line(surface, color, point1, point2)
    return rect


def aalines(surface, color, closed, pointlist, blend=1):
    """
    Draw interconnected lines, and returns Rect bound.
    Arguments include surface to draw, color, closed, and pointlist.
    """
    rect = lines(surface, color, closed, pointlist)
    return rect


def bounding_rect_return(setting):
    """
    Set whether draw functions return bounding Rect.
    Setting (bool) defaults to True on module initialization.
    """
    global _return_rect
    _return_rect = setting


#depreciated
def _set_return(*args):
    msg = 'set_return depreciated, use bounding_rect_return'
    print(msg)
    raise Exception(msg)
set_return = _set_return

