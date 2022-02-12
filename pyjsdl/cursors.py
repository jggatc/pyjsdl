#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl.surface import Surface
from pyjsdl.color import Color
from pyjsdl import constants as Const


#cursors not implemented
arrow = diamond = broken_x = tri_left = tri_right = ()


def compile(strings, black='X', white='.', xor='o'):
    """
    Compile binary data from cursor string.
    Arguments cursor string, and optional symbols representing colors.
    Data represents black and white pixels, xor color defaulting to black.
    Data should be a string list of width divisible by 8.
    Return cursor data and mask, can be used with mouse.set_cursor.
    """
    data = []
    mask = []
    dbit = {black:1, white:0, xor:1}
    mbit = {black:1, white:1, xor:0}
    string = ''.join(strings)
    for i in range(0, len(string), 8):
        s = string[i:i+8]
        db = mb = 0
        if s != '        ':
            for j in range(8):
                c = s[j]
                if c == ' ':
                    continue
                if dbit[c]:
                    db |= 0x01<<7-j
                if mbit[c]:
                    mb |= 0x01<<7-j
        data.append(int(db))
        mask.append(int(mb))
    return tuple(data), tuple(mask)


def create_cursor(size, data, mask):
    """
    Create cursor image from binary data.
    Arguments cursor size and its binary data and mask.
    Return surface, can be used with mouse.set_cursor.
    """
    surface = Surface(size, Const.SRCALPHA)
    black = Color(0,0,0,255)
    white = Color(255,255,255,255)
    x = y = 0
    for i in range(len(data)):
        if data[i] or mask[i]:
            for j in range(8):
                if data[i] & 0x01<<7-j:
                    surface.setFillStyle(black)
                    surface.fillRect(x+j, y, 1, 1)
                elif mask[i] & 0x01<<7-j:
                    surface.setFillStyle(white)
                    surface.fillRect(x+j, y, 1, 1)
        x += 8
        if x >= size[0]:
            x = 0
            y += 1
    return surface


def get_cursor_types():
    #https://developer.mozilla.org/en-US/docs/Web/CSS/cursor
    """
    Return list of cursor types from CSS Cursor API.
    """
    types = ['default', 'auto', 'none', 'context-menu', 'help',
             'pointer', 'progress', 'wait', 'cell', 'crosshair',
             'text', 'vertical-text', 'alias', 'copy', 'move',
             'no-drop', 'not-allowed', 'e-resize', 'n-resize',
             'ne-resize', 'nw-resize', 's-resize', 'se-resize',
             'sw-resize', 'w-resize', 'ew-resize', 'ns-resize',
             'nesw-resize', 'nwse-resize', 'col-resize',
             'row-resize', 'all-scroll', 'zoom-in', 'zoom-out',
             'grab', 'grabbing']
    return types

