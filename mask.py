#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

#from __future__ import division
from pyjsdl.pyjsarray import BitSet
from pyjsdl.color import Color

__docformat__ = 'restructuredtext'


def from_surface(surface, threshold=127):
    """
    **pyjsdl.mask.from_surface**
    
    Return Mask derived from surface using alpha transparency.
    Optional argument to set alpha threshold.
    """
    mask = Mask(surface.width, surface.height)
    if not mask.bit:
        return None
    pixels = surface.impl.getImageData(0, 0, surface.width, surface.height)
    width, height = surface.width*4, surface.height
    for y in xrange(0, height):
        xpix = 0
        i = (y*width)+3
        for x in xrange(0, width, 4):
            if surface._getPixel(pixels, i+x) > threshold:
                mask.set_at((xpix,y))
            xpix += 1
    return mask


def from_threshold(surface, color, threshold=(0,0,0,255)):
    """
    **pyjsdl.mask.from_threshold**
    
    Return Mask from surface using a given color.
    Optional threshold argument to set color range and alpha threshold.
    """
    mask = Mask(surface.width, surface.height)
    if not mask.bit:
        return None
    pixels = surface.impl.getImageData(0, 0, surface.width, surface.height)
    if threshold == (0,0,0,255):
        color = Color(color)
        color = (color.r,color.g,color.b)
        width, height = surface.width*4, surface.height
        for y in xrange(0, height):
            xpix = 0
            i = y*width
            for x in xrange(0, width, 4):
                ix = i+x
                if surface._getPixel(pixels, ix) == color[0] and surface._getPixel(pixels, ix+1) == color[1] and surface._getPixel(pixels, ix+2) == color[2] and surface._getPixel(pixels, ix+3) >= threshold[3]:
                    mask.set_at((xpix,y))
                xpix += 1
    else:
        color = Color(color)
        col = {}
        for i, c in enumerate(('r','g','b')):
            if threshold[i]:
                col[c+'1'] = color[i] - threshold[i] - 1
                col[c+'2'] = color[i] + threshold[i] + 1
            else:
                col[c+'1'] = color[i] - 1
                col[c+'2'] = color[i] + 1
        col['a'] = threshold[3] - 1
        width, height = surface.width*4, surface.height
        for y in xrange(0, height):
            xpix = 0
            i = y*width
            for x in xrange(0, width, 4):
                ix = i+x
                if (col['r1'] < surface._getPixel(pixels, ix) < col['r2']) and (col['g1'] < surface._getPixel(pixels, ix+1) < col['g2']) and (col['b1'] < surface._getPixel(pixels, ix+2) < col['b2']) and (surface._getPixel(pixels, ix+3) > col['a']):
                    mask.set_at((xpix,y))
                xpix += 1
    return mask


class Mask(object):
    """
    **pyjsdl.mask.Mask**
    
    * Mask.get_size
    * Mask.get_at
    * Mask.set_at
    * Mask.fill
    * Mask.clear
    * Mask.invert
    * Mask.count
    * Mask.overlap
    * Mask.toString
    """

    def __init__(self, width, height):
        """
        Return a Mask of an image.
        The arguments include width and height of the image.
        The mask is stored as a list of bitset for each pixel row in the image.
        """
        self.width = int(width)
        self.height = int(height)
        self.bit = []
        for bitset in range(self.height):
            self.bit.append(BitSet(self.width))

    def __repr__(self):
        """
        Return string representation of Mask object.
        """
        return "%s(%r)" % (self.__class__, self.__dict__)

    def get_size(self):
        """
        Return width, height of mask.
        """
        return (self.width, self.height)

    def get_at(self, pos):
        """
        Return bit setting for given pos.
        """
        return self.bit[pos[1]].get(pos[0])

    def set_at(self, pos, value=1):
        """
        Set bit for given pos.
        Optional value to set bit, eith 1 or 0, defaults to 1.
        """
        self.bit[pos[1]].set(pos[0], value)
        return None

    def fill(self):
        """
        Fill mask.
        """
        for bitset in self.bit:
            bitset.fill()
        return None

    def clear(self):
        """
        Clear mask.
        """
        for bitset in self.bit:
            bitset.clear()
        return None

    def invert(self):
        """
        Invert bit value in mask.
        """
        for bitset in self.bit:
            bitset.flip(0,self.width)
        return None

    def count(self):
        """
        Return count of true bits in mask.
        """
        true_bits = 0
        for bitset in self.bit:
            true_bits += bitset.cardinality()
        return true_bits

    def overlap(self, mask, offset):
        """
        Return True if mask at offset position overlap with this mask.
        """
        if offset[0] > 0:
            x1 = offset[0]
            x2 = 0
        else:
            x1 = 0
            x2 = -offset[0]
        if offset[1] > 0:
            y1 = offset[1]
            y2 = 0
        else:
            y1 = 0
            y2 = -offset[1]
        w = min(self.width-x1, mask.width-x2)
        h = min(self.height-y1, mask.height-y2)
        if w > 0 and h > 0:
            for y in range(h):
                if self.bit[y1+y].get(x1, x1+w).intersects(mask.bit[y2+y].get(x2, x2+w)):
                    return True
        return None

    def toString(self, bit=('1','0')):
        """
        Return string representation of mask.
        Optional bit argument specify bit character.
        """
        cbit = {True:bit[0], False:bit[1]}
        cbitset = []
        for bitset in self.bit:
            cbitset.append('\n')
            cbitset.extend([cbit[bitset.get(bit)] for bit in range(self.width)])
        bitstr = ''.join(cbitset)
        return bitstr

