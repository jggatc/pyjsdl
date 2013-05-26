#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
from pyjsbitset import BitSet

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
    for y in xrange(0, surface.height):
        xpix = 0
        for x in xrange(0, surface.width*4, 4):
            if surface._getPixel(pixels, (y*(surface.width*4)+x+3)) > threshold:
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
        for y in xrange(0, surface.height):
            xpix = 0
            for x in xrange(0, surface.width*4, 4):
                if surface._getPixel(pixels, (y*(surface.width*4)+x)) == color[0] and surface._getPixel(pixels, (y*(surface.width*4)+x+1)) == color[1] and surface._getPixel(pixels, (y*(surface.width*4)+x+2)) == color[2] and surface._getPixel(pixels, (y*(surface.width*4)+x+3)) == threshold[3]:
                    mask.set_at((xpix,y))
                xpix += 1
    else:
        col = []
        for i in range(len(color)):
            if threshold[i]:
                l = color[i] - threshold[i]
                if l < 0: l = 0
                h = color[i] + threshold[i]
                if h > 255: h = 255
                col.append( (l,h) )
            else:
                col[i].append( (color[i],color[i]) )
        for y in xrange(0, surface.height):
            xpix = 0
            for x in xrange(0, surface.width*4, 4):
                if (col[0][0] <= surface._getPixel(pixels, (y*(surface.width*4)+x)) <= col[0][1]) and (col[1][0] <= surface._getPixel(pixels, (y*(surface.width*4)+x+1)) <= col[1][1]) and (col[2][0] <= surface._getPixel(pixels, (y*(surface.width*4)+x+2)) <= col[2][1]) and (surface._getPixel(pixels, (y*(surface.width*4)+x+3)) == threshold[3]):
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
    * Mask.print_mask
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
            bitset.set(0,self.width)
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

    def print_mask(self, onchar=None, offchar=None):
        """
        Print mask.
        """
        def prt(char):
            print char,
        if not onchar:
            onbit = lambda bit: prt(int(bit))
        else:
            onbit = lambda bit: prt(onchar)
        if not offchar:
            offbit = lambda bit: prt(int(bit))
        else:
            offbit = lambda bit: prt(offchar)
        print
        i = 0
        for bitset in self.bit:
            print str(i)[-1],
            for bit in range(self.width):
                b = bitset.get(bit)
                if b:
                    onbit(b)
                else:
                    offbit(b)
            i += 1
            print
        print

