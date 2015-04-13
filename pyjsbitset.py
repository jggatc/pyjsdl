#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

#PyjsBitset - Python-to-JavaScript BitSet Module
#Copyright (c) 2013 James Garnon

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

#PyjsBitset version 0.53
#Project Site: http://gatc.ca/

import math
from pyjsarray import PyUint8Array, PyUint16Array, PyUint32Array


class BitSet:

    """
    BitSet provides a bitset object to use in a Python-to-JavaScript application. It uses the PyUint8Array implementation of the JavaScript Uint8Array 8-bit typedarray. BitSet16 and BitSet32 stores data in PyUint16Array (16-bit) and PyUint32Array (32-bit) that implement the Uint16Array and Uint32Array typedarray. The BitSet will dynamically expand to hold the bits required, an optional width argument define number of bits the BitSet instance will initially hold.
    """

    __bit = 8
    __bitmask = None
    __typedarray = PyUint8Array

    def __init__(self, width=None):
        if not self.__class__.__bitmask:
            self.__class__.__bitmask = dict([(self.__class__.__bit-i-1,1<<i) for i in range(self.__class__.__bit-1,-1,-1)])
            self.__class__.__bitmask[self.__class__.__bit-1] = int(self.__class__.__bitmask[self.__class__.__bit-1])      #pyjs [1<<0] = 1L
        if width:
            self.__width = abs(width)
        else:
            self.__width = self.__bit
        self.__data = self.__typedarray( math.ceil(self.__width/(self.__bit*1.0)) )

    def __str__(self):
        """
        Return string representation of BitSet object.
        """
        return "%s" % self.__class__

    def __repr__(self):
        """
        Return string of the indexes of the set bits.
        """
        setBit = []
        for index in xrange(self.__width):
            if self.get(index):
                setBit.append(str(index))
        return "{" + ", ".join(setBit) + "}"

    def __getitem__(self, index):
        """
        Get bit by index.
        """
        return self.get(index)

    def __setitem__(self, index, value):
        """
        Set bit by index.
        """
        self.set(index, value)

    def __len__(self):
        """
        Get bit length.
        """
        for index in xrange(self.__width-1, -1, -1):
            if self.get(index):
                break
        return index+1

    def __iter__(self):
        """
        Iterate over bits.
        """
        index = 0
        while index < self.__width:
            yield self.get(index)
            index += 1

    def get(self, index, toIndex=None):
        """
        Get bit by index.
        Arguments include index of bit, and optional toIndex that return a slice as a BitSet.
        """
        if index > self.__width-1:
            if not toIndex:
                return False
            else:
                size = toIndex-index
                if size > 0:
                    return self.__class__(size)
                else:   #use exception
                    return None
        if toIndex is None:
            return bool( self.__data[ int(index/self.__bit) ] & self.__bitmask[ index%self.__bit ] )
        else:
            size = toIndex-index
            if size > 0:
                bitset = self.__class__(size)
                ix = 0
                if toIndex > self.__width:
                    toIndex = self.__width
                for i in xrange(index, toIndex):
                    bitset.set(ix, bool( self.__data[ int(i/self.__bit) ] & self.__bitmask[ i%self.__bit ] ))
                    ix += 1
                return bitset
            else:    #use exception
                return None 

    def set(self, index, value=1):
        """
        Set bit by index.
        Optional argument value is the bit state of 1(True) or 0(False). Default:1
        """
        if index > self.__width-1:
            if value:
                self.resize(index+1)
            else:
                return
        if value:
            self.__data[ int(index/self.__bit) ] = self.__data[ int(index/self.__bit) ] | self.__bitmask[ index%self.__bit ]
#            self.__data[ int(index/self.__bit) ] |= self.__bitmask[ index%self.__bit ]    #pyjs -O: |= not processed
        else:
            self.__data[ int(index/self.__bit) ] = self.__data[ int(index/self.__bit) ] & ~(self.__bitmask[ index%self.__bit ])
#            self.__data[ int(index/self.__bit) ] &= ~(self.__bitmask[ index%self.__bit ])     #pyjs -O: &= not processed
        return None

    def fill(self, index=None, toIndex=None):
        """
        Set the bit. If no argument provided, all bits are set.
        Optional argument index is bit index to set, and toIndex to set a range of bits.
        """
        if index is None and toIndex is None:
            for i in xrange(0, self.__width):
                self.set(i, 1)
        else:
            if toIndex is None:
                self.set(index, 1)
            else:
                for i in xrange(index, toIndex):
                    self.set(i, 1)

    def clear(self, index=None, toIndex=None):
        """
        Clear the bit. If no argument provided, all bits are cleared.
        Optional argument index is bit index to clear, and toIndex to clear a range of bits.
        """
        if index is None:
            for i in xrange(len(self.__data)):
                self.__data[i] = 0
        else:
            if toIndex is None:
                self.set(index, 0)
            else:
                if index == 0 and toIndex == self.__width:
                    for dat in xrange(len(self.__data)):
                        self.__data[dat] = 0
                else:
                    for i in xrange(index, toIndex):
                        self.set(i, 0)

    def flip(self, index, toIndex=None):
        """
        Flip the state of the bit.
        Argument index is the bit index to flip, and toIndex to flip a range of bits.
        """
        if toIndex is None:
            self.set(index, not self.get(index))
        else:
            if toIndex > self.__width:
                self.resize(toIndex)
                toIndex = self.__width
            if index == 0 and toIndex == self.__width:
                for dat in xrange(len(self.__data)):
                    self.__data[dat] = ~self.__data[dat]
            else:
                for i in xrange(index, toIndex):
                    self.set(i, not self.get(i))

    def cardinality(self):
        """
        Return the count of bit set.
        """
        count = 0
        for bit in xrange(self.__width):
            if self.get(bit):
                count += 1
        return count

    def intersects(self, bitset):
        """
        Check if set bits in this BitSet are also set in the bitset argument.
        Return True if bitsets intersect, otherwise return False.
        """
        for dat in xrange(len(bitset.__data)):
            if bitset.__data[dat] & self.__data[dat]:
                return True
        return False

    def andSet(self, bitset):
        """
        BitSet and BitSet.
        """
        data = min(len(self.__data), len(bitset.__data))
        for dat in xrange(data):
            self.__data[dat] = self.__data[dat] & bitset.__data[dat]
#            self.__data[dat] &= bitset.__data[dat]     #pyjs -O: &= not processed
#        pyjs -S: &= calls __and__ instead of __iand__, -O: no call to operator methods

    def orSet(self, bitset):
        """
        BitSet or BitSet.
        """
        data = min(len(self.__data), len(bitset.__data))
        for dat in xrange(data):
            self.__data[dat] = self.__data[dat] | bitset.__data[dat]
#            self.__data[dat] |= bitset.__data[dat]    #pyjs -O: |= not processed

    def xorSet(self, bitset):
        """
        BitSet xor BitSet.
        """
        data = min(len(self.__data), len(bitset.__data))
        for dat in xrange(data):
            self.__data[dat] = self.__data[dat] ^ bitset.__data[dat]
#            self.__data[dat] ^= bitset.__data[dat]    #pyjs -O: |= not processed

    def resize(self, width):
        """
        Resize the BitSet to width argument.
        """
        if width > self.__width:
            self.__width = width
            if self.__width > len(self.__data) * self.__bit:
                array = self.__typedarray( math.ceil(self.__width/(self.__bit*1.0)) )
                array.set(self.__data)
                self.__data = array
        elif width < self.__width:
            if width < len(self):
                width = len(self)
            self.__width = width
            if self.__width <= len(self.__data) * self.__bit - self.__bit:
                array = self.__typedarray( math.ceil(self.__width/(self.__bit*1.0)) )
                array.set(self.__data.subarray(0,math.ceil(self.__width/(self.__bit*1.0))))
                self.__data = array

    def size(self):
        """
        Return bits used by BitSet storage array.
        """
        return len(self.__data) * self.__bit

    def isEmpty(self):
        """
        Check whether any bit is set.
        Return True if none set, otherwise return False.
        """
        for data in self.__data:
            if data:
                return False
        return True

    def clone(self):
        """
        Return a copy of the BitSet.
        """
        new_bitset = self.__class__(1)
        data = self.__typedarray(self.__data)
        new_bitset.__data = data
        new_bitset.__width = self.__width
        return new_bitset


class BitSet16(BitSet):
    """
    BitSet using PyUint16Array.
    """
    __bit = 16
    __bitmask = None
    __typedarray = PyUint16Array

    def __init__(self, width=None):
        BitSet.__init__(self, width)


class BitSet32(BitSet):
    """
    BitSet using PyUint32Array.
    """
    __bit = 32
    __bitmask = None
    __typedarray = PyUint32Array

    def __init__(self, width=None):
        BitSet.__init__(self, width)

