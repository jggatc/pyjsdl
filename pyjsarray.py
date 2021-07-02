#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

#PyjsArray - Python-to-JavaScript TypedArray Module
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

#PyjsArray version 0.54
#Project Site: https://gatc.ca/

from math import ceil as _ceil
from __pyjamas__ import JS
import sys


def _compat():
    global range
    range = xrange

if sys.version_info < (3,):
    _compat()


class TypedArray(object):

    """
    TypedArray is the base class that wraps the JavaScript TypedArray objects.
    The derived objects provides an interface to the JavaScript array objects.
    Typedarray implemented: Uint8ClampedArray, Uint8Array, Uint16Array, Uint32Array, Int8Array, Int16Array, Int32Array, Float32Array, Float64Array.
    The module contains an Ndarray class to instantiate N-dimensional arrays, ImageData and ImageMatrix classes that provide an interface to canvas ImageData, and BitSet classes that implement a bit array.
    """

    __obj = { 'Uint8ClampedArray': Uint8ClampedArray,
              'Uint8Array':        Uint8Array,
              'Uint16Array':       Uint16Array,
              'Uint32Array':       Uint32Array,
              'Int8Array':         Int8Array,
              'Int16Array':        Int16Array,
              'Int32Array':        Int32Array,
              'Float32Array':      Float32Array,
              'Float64Array':      Float64Array }

    def __init__(self, data=None, offset=None, length=None, typedarray=None):
        """
        The TypedArray object is instantiated with either the array size, an array of TypedArray or Python type, or an existing ArrayBuffer to view, which creates a new TypedArray of size and included data as the specified type. Optional arguments include offset index at which ArrayBuffer data is inserted and length of an ArrayBuffer.
        """
        if data:
            if isinstance(data, int):
                if pyjs_mode.optimized:
                    self._data = JS("new @{{typedarray}}(@{{data}})")
                else:
                    self._data = JS("new @{{typedarray}}(@{{data}}['valueOf']())")
            elif isinstance(data, (list,tuple)):
                if pyjs_mode.optimized:
                    self._data = JS("new @{{typedarray}}(@{{data}}['getArray']())")
                else:
                    data = [dat.valueOf() for dat in data]
                    self._data = JS("new @{{typedarray}}(@{{data}}['getArray']())")
            elif isinstance(data, TypedArray):
                self._data = JS("new @{{typedarray}}(@{{data}}['_data'])")
            else:   #TypedArray or ArrayBuffer
                if offset is None and length is None:
                    self._data = JS("new @{{typedarray}}(@{{data}})")
                else:
                    if offset is None:
                        offset = 0
                    if length is None:
                        self._data = JS("new @{{typedarray}}(@{{data}}, @{{offset}})")
                    else:
                        self._data = JS("new @{{typedarray}}(@{{data}}, @{{offset}}, @{{length}})")
        else:
            self._data = None

    def _array(self, array):
        typedarray = self.__class__()
        typedarray._data = array
        return typedarray

    def __str__(self):
        return self._data.toString()

    def __iter__(self):
        index = 0
        while index < self._data.length:
            yield self[index]
            index += 1

    def __getitem__(self, index):
        return JS("@{{int}}(@{{self}}['_data'][@{{index}}]);")

    def __setitem__(self, index, value):
        if pyjs_mode.optimized:
            JS("@{{self}}['_data'][@{{index}}]=@{{value}};")
        else:
            value = value.valueOf()
            JS("@{{self}}['_data'][@{{index}}]=@{{value}};")
        return None

    def __len__(self):
        return self._data.length

    def filter(self, func):
        """
        Return typedarray filtered by provided function.
        """
        return self._array(self._data.filter(func))

    def map(self, func):
        """
        Return typedarray of applying provided function across elements.
        """
        return self._array(self._data.map(func))

    def reduce(self, func):
        """
        Return result of applying provided accumlator function.
        """
        return self._array(self._data.reduce(func))

    def slice(self, i, j):
        """
        Return typedarray from indices i,j.
        """
        return self._array(self._data.slice(i,j))

    def set(self, data, offset=0):
        """
        Set data to the array. Arguments: data is a list of either the TypedArray or Python type, offset is the start index where data will be set (defaults to 0).
        """
        if isinstance(data, (list,tuple)):
            if pyjs_mode.optimized:
                self._data.set(data.getArray(), offset)
            else:
                data = [dat.valueOf() for dat in data]
                self._data.set(data.getArray(), offset)
        elif isinstance(data, TypedArray):
            self._data.set(data._data, offset)

    def subarray(self, begin=0, end=None):
        """
        Retrieve a subarray of the array. The subarray is a is a view of the derived array. Optional arguments begin and end (default to begin/end of the array) are the index spanning the subarray.
        """
        if end is None:
            end = self._data.length
        array = self._data.subarray(begin, end)
        typedarray = self.__class__()
        typedarray._data = array
        return typedarray

    def getLength(self):
        """
        Return array.length attribute.
        """
        return self._data.length

    def getByteLength(self):
        """
        Return array.byteLength attribute.
        """
        return self._data.byteLength

    def getBuffer(self):
        """
        Return array.buffer attribute.
        """
        return self._data.buffer

    def getByteOffset(self):
        """
        Return array.byteOffset attribute.
        """
        return self._data.byteOffset

    def getBytesPerElement(self):
        """
        Return array.BYTES_PER_ELEMENT attribute.
        """
        return self._data.BYTES_PER_ELEMENT

    def getArray(self):
        """
        Return JavaScript TypedArray.
        """
        return self._data

    def setArray(self, array):
        """
        Set JavaScript TypedArray.
        """
        self._data = array
        return None


class Uint8ClampedArray(TypedArray):
    """
    Create a TypedArray interface to Uint8ClampedArray.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            typedarray = TypedArray.__obj['Uint8ClampedArray']
            TypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class Uint8Array(TypedArray):
    """
    Create a TypedArray interface to Uint8Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            typedarray = TypedArray.__obj['Uint8Array']
            TypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class Uint16Array(TypedArray):
    """
    Create a TypedArray interface to Uint16Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            typedarray = TypedArray.__obj['Uint16Array']
            TypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class Uint32Array(TypedArray):
    """
    Create a TypedArray interface to Uint32Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            typedarray = TypedArray.__obj['Uint32Array']
            TypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class Int8Array(TypedArray):
    """
    Create a TypedArray interface to Int8Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            typedarray = TypedArray.__obj['Int8Array']
            TypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class Int16Array(TypedArray):
    """
    Create a TypedArray interface to Int16Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            typedarray = TypedArray.__obj['Int16Array']
            TypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class Int32Array(TypedArray):
    """
    Create a TypedArray interface to Int32Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            typedarray = TypedArray.__obj['Int32Array']
            TypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class Float32Array(TypedArray):
    """
    Create a TypedArray interface to Float32Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            typedarray = TypedArray.__obj['Float32Array']
            TypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise

    def __getitem__(self, index):
        return JS("@{{self}}['_data'][@{{index}}];")


class Float64Array(TypedArray):
    """
    Create a TypedArray interface to Float64Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            typedarray = TypedArray.__obj['Float64Array']
            TypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise

    def __getitem__(self, index):
        return JS("@{{self}}['_data'][@{{index}}];")


class CanvasPixelArray(TypedArray):
    """
    Create a TypedArray interface to CanvasPixelArray.
    """

    def __init__(self, data=None, offset=None, length=None):
        TypedArray.__init__(self, data, offset, length)
        self._superArray = None
        self._superIndex = (0,0)

    def __iter__(self):
        if not self._superArray:
            TypedArray.__iter__(self)
        else:
            index = self._superIndex[0]
            while index < self._superIndex[1]:
                yield self._superArray[index]
                index += 1

    def __getitem__(self, index):
        if not self._superArray:
            return TypedArray.__getitem__(self, index)
        else:
            return self._superArray.__getitem__(index+self._superIndex[0])

    def __setitem__(self, index, value):
        if not self._superArray:
            TypedArray.__setitem__(self, index, value)
        else:
            self._superArray.__setitem__(index+self._superIndex[0], value)
        return None

    def set(self, data, offset=0):
        """
        Set data to the array. Arguments: data is a list of either the TypedArray or Python type, offset is the start index where data will be set (defaults to 0).
        """
        if not self._superArray:
            for index in range(len(data)):
                self[index+offset] = data[index]
        else:
            self._superArray.set(data, offset+self._superIndex[0])

    def subarray(self, begin=0, end=None):
        """
        Retrieve a subarray of the array. The subarray is a is a view of the derived array. Optional arguments begin and end (default to begin/end of the array) are the index spanning the subarray.
        """
        if end is None:
            end = self._data.length
        array = self.__class__()
        array._data = self._data
        array._superArray = self
        array._superIndex = (begin,end)
        return array


class Ndarray(object):

    __typedarray = { 'uint8c':  Uint8ClampedArray,
                     'int8':    Int8Array,
                     'uint8':   Uint8Array,
                     'int16':   Int16Array,
                     'uint16':  Uint16Array,
                     'int32':   Int32Array,
                     'uint32':  Uint32Array,
                     'float32': Float32Array,
                     'float64': Float64Array }

    __dtypes = { 'uint8c':'uint8c', 'x':'uint8c', 0:'uint8c',
                 'int8':'int8', 'b':'int8', 4:'int8',
                 'uint8':'uint8', 'B':'uint8', 1:'uint8',
                 'int16':'int16', 'h':'int16', 5:'int16',
                 'uint16':'uint16', 'H':'uint16', 2:'uint16',
                 'int32':'int32', 'i':'int32', 6:'int32',
                 'uint32':'uint32', 'I':'uint32', 3:'uint32',
                 'float32':'float32', 'f':'float32', 7:'float32',
                 'float64':'float64', 'd':'float64', 8:'float64' }

    def __init__(self, dim, dtype='float64'):
        """
        Generate an N-dimensional array of TypedArray data.
        Argument can be size (int or tuple) or data (list or TypedArray).
        Optional argument dtype specifies TypedArray data type:
                'uint8c'    Uint8ClampedArray
                'int8'      Int8Array
                'uint8'     Uint8Array
                'int16'     Int16Array
                'uint16'    Uint16Array
                'int32'     Int32Array
                'uint32'    Uint32Array
                'float32'   Float32Array
                'float64'   Float64Array
        """
        self._dtype = self.__dtypes[dtype]
        typedarray = self.__typedarray[self._dtype]
        if isinstance(dim, tuple):
            size = 1
            for i in dim:
                size *= i
            self._data = typedarray(size)
            self._shape = dim
            indices = []
            for i in self._shape:
                size /= i
                indices.append(size)
            self._indices = tuple(indices)
        elif isinstance(dim, int):
            self._data = typedarray(dim)
            self._shape = (dim,)
            self._indices = (self._shape[0],)
        elif isinstance(dim, list):
            if not (len(dim)>0 and isinstance(dim[0], list)):
                self._data = typedarray(dim)
                self._shape = (len(dim),)
                self._indices = (self._shape[0],)
            else:
                _dat = self._lflatten(dim)
                _dim = self._lshape(dim)
                self._data = typedarray(list(_dat))
                self._shape = (len(self._data),)
                self.setshape(tuple(_dim))
        else:
            self._data = dim
            self._shape = (len(dim),)
            self._indices = (self._shape[0],)

    def getshape(self):
        """
        Return array shape.
        Ndarray.shape accessible with compilation in --strict mode,
        and with --enable-descriptor-proto option in --optimized mode.
        """
        return self._shape

    def setshape(self, *dim):
        """
        Set shape of array.
        Argument is new shape.
        Raises TypeError if shape is not appropriate.
        Ndarray.shape accessible with compilation in --strict mode,
        and with --enable-descriptor-proto option in --optimized mode.
        """
        if isinstance(dim[0], tuple):
            dim = dim[0]
        size = 1
        for i in dim:
            size *= i
        array_size = 1
        for i in self._shape:
            array_size *= i
        if size != array_size:
            raise TypeError("array size cannot change")
        self._shape = dim
        indices = []
        for i in self._shape:
            size /= i
            indices.append(size)
        self._indices = tuple(indices)
        return None

    shape = property(getshape, setshape)

    def _lflatten(self, l):
        for el in l:
            if isinstance(el, list):
                for _l in self._lflatten(el):
                    yield _l
            else:
                yield el

    def _lshape(self, l):
        _l = l
        while isinstance(_l, list):
            yield len(_l)
            _l = _l[0]

    def __getitem__(self, index):
        if hasattr(index, '__len__'):
            indexLn, shapeLn = index.__len__(), len(self._shape)
            if indexLn == shapeLn:
                return self._data[sum([index[i]*self._indices[i] for i in range(indexLn)])]
            else:
                begin = sum([index[i]*self._indices[i] for i in range(indexLn)])
                end = begin + self._indices[indexLn-1]
                subarray = self._data.subarray(begin, end)
                array = Ndarray(subarray, self._dtype)
                array._shape = self._shape[indexLn:]
                array._indices = self._indices[indexLn:]
                return array
        else:
            if len(self._shape) == 1:
                return self._data[index]
            else:
                begin = index * self._indices[0]
                end = begin + self._indices[0]
                subarray = self._data.subarray(begin, end)
                array = Ndarray(subarray, self._dtype)
                array._shape = self._shape[1:]
                array._indices = self._indices[1:]
                return array

    def __setitem__(self, index, value):
        def unpack(obj, lst=None):
            if lst is None:
                lst = []
            for element in obj:
                if isinstance(element, (list,tuple)):
                    unpack(element, lst)
                else:
                    lst.append(element)
            return lst
        if hasattr(index, '__len__'):
            indexLn, shapeLn = index.__len__(), len(self._shape)
            if indexLn == shapeLn:
                self._data[sum([index[i]*self._indices[i] for i in range(indexLn)])] = value
            else:
                begin = sum([index[i]*self._indices[i] for i in range(indexLn)])
                end = begin + self._indices[indexLn-1]
                subarray = self._data.subarray(begin, end)
                if isinstance(value, Ndarray):
                    value = value._data
                else:
                    if isinstance(value[0], (list,tuple)):
                        value = unpack(value)
                subarray.set(value)
        else:
            if len(self._shape) == 1:
                self._data[index] = value
            else:
                begin = index * self._indices[0]
                end = begin + self._indices[0]
                subarray = self._data.subarray(begin, end)
                if isinstance(value, Ndarray):
                    value = value._data
                else:
                    if isinstance(value[0], (list,tuple)):
                        value = unpack(value)
                subarray.set(value)
        return None

    def __getslice__(self, lower, upper):
        subarray = self._data.subarray(lower, upper)
        return Ndarray(subarray, self._dtype)

    def __setslice__(self, lower, upper, data):
        subarray = self._data.subarray(lower, upper)
        subarray.set(data)
        return None

    def __iter__(self):
        if len(self._shape) > 1:
            index = 0
            while index < self._shape[0]:
                begin = index * self._indices[0]
                end = begin + self._indices[0]
                subarray = self._data.subarray(begin, end)
                array = Ndarray(subarray, self._dtype)
                array._shape = self._shape[1:]
                array._indices = self._indices[1:]
                yield array
                index += 1
        else:
            index = 0
            while index < self._shape[0]:
                yield self._data[index]
                index += 1

    def _array_dim(self):
        if 'int' in self._dtype:
            vmax = len(str(max(self._data)))
            vmin = len(str(min(self._data)))
            vlen = {True:vmax, False:vmin}[vmax>vmin]
            vfmt = '%*d'
        else:
            vlen = max([len('%0.4f'%v) for v in self._data])
            vfmt = '%*.4f'
        return vlen, vfmt

    def _array_str(self, array, vlen, vfmt, vstr):
        if len(array._shape) == 1:
            s = [vfmt % (vlen,val) for val in array]
            vstr.append('[%s]' % ' '.join(s))
        else:
            for i, a in enumerate(array):
                if i == 0:
                    vstr.append('[')
                else:
                    vstr.append(' '*(len(self._shape)-len(a._shape)))
                self._array_str(a, vlen, vfmt, vstr)
                if i < len(array)-1:
                    vstr.append('\n')
                else:
                    if vstr[-1] == ']\n':
                        vstr[-1] = ']'
                    if array._shape != self._shape:
                        vstr.append(']\n')
                    else:
                        vstr.append(']')
        return vstr

    def __str__(self):
        vlen, vfmt = self._array_dim()
        vstr = self._array_str(self, vlen, vfmt, [])
        return ''.join(vstr)

    def __repr__(self):
        s = str(self.tolist())
        sl = len(self._shape)
        for d in range(1, sl):
            s = s.replace(' '+'['*d, '\n'+' '*(sl+8-d)+'['*d)
        return 'Ndarray(%s, dtype=%s)' % (s, repr(self._dtype))

    def __len__(self):
        return self._shape[0]

    def __lt__(self, other):
        ndarray = Ndarray(len(self._data), 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] < other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] < other_data[i]
        return ndarray

    def __le__(self, other):
        ndarray = Ndarray(self._shape, 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] <= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] <= other_data[i]
        return ndarray
    
    def __eq__(self, other):
        ndarray = Ndarray(self._shape, 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] == other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] == other_data[i]
        return ndarray
    
    def __ne__(self, other):
        ndarray = Ndarray(self._shape, 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] != other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] != other_data[i]
        return ndarray
    
    def __gt__(self, other):
        ndarray = Ndarray(self._shape, 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] > other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] > other_data[i]
        return ndarray

    def __ge__(self, other):
        ndarray = Ndarray(self._shape, 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] >= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] >= other_data[i]
        return ndarray

    def __add__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] + other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] + other_data[i]
        return ndarray

    def __sub__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] - other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] - other_data[i]
        return ndarray

    def __mul__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] * other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] * other_data[i]
        return ndarray

    def __div__(self, other):
        return self.__truediv__(other)

    def __truediv__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] / other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] / other_data[i]
        return ndarray

    def __floordiv__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] // other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] // other_data[i]
        return ndarray

    def __divmod__(self, other):
        return self.__floordiv__(other), self.__mod__(other)

    def __mod__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] % other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] % other_data[i]
        return ndarray

    def __pow__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] ** other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] ** other_data[i]
        return ndarray

    def __neg__(self):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        for i in range(len(data)):
            ndarray_data[i] = -data[i]
        return ndarray

    def __pos__(self):
        ndarray = self.copy()
        return ndarray

    def __abs__(self):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        for i in range(len(data)):
            if data[i] < 0:
                ndarray_data[i] = -data[i]
        return ndarray

    def __matmul__(self, other):
        _other = self._get_array(other)
        x_dim = len(self._shape)
        y_dim = len(_other._shape)
        if x_dim != y_dim:
            raise ValueError('incompatible array shapes for matmul')
        if x_dim == 1:
            if self._shape[0] == _other._shape[0]:
                data = self._data
                other_data = _other._data
                result = 0
                for i in range(len(data)):
                    result += (data[i] * other_data[i])
                return result
            else:
                raise ValueError('incompatible array shapes for matmul')
        xshape = self._shape[-2:]
        yshape = _other._shape[-2:]
        if xshape[1] == yshape[0]:
            m = xshape[1]
            n = xshape[0]
            p = yshape[1]
            d = self._shape[:-2]
            d_len = 1
            for v in d:
                d_len*=v
        else:
            raise ValueError('incompatible array shapes for matmul')
        _data = self._data.__class__(d_len*n*p)
        array = Ndarray(_data, self._dtype)
        array.setshape(d+(n,p))
        if x_dim == 2:
            arrays = [(self, _other, array)]
        elif x_dim == 3:
            arrays = [(self[i], _other[i], array[i])
              for i in range(d[0])]
        elif x_dim == 4:
            arrays = [(self[i,j], _other[i,j], array[i,j])
              for i,j in [(i,j) for i in range(d[0]) for j in range(d[1])]]
        elif x_dim == 5:
            arrays = [(self[i,j,k], _other[i,j,k], array[i,j,k])
              for i,j,k in [(i,j,k) for i in range(d[0]) for j in range(d[1]) for k in range(d[2])]]
        else:
            raise ValueError('incompatible array shapes for matmul')
        for _x, _y, _array in arrays:
            _x_data = _x._data
            _y_data = _y._data
            _array_data = _array._data
            for i in range(n):
                for j in range(p):
                    result = 0
                    for k in range(m):
                        result += (_x_data[i*m+k] * _y_data[k*p+j])
                    _array_data[i*p+j] = result
        return array

    def __iadd__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] += other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] += other_data[i]
        return self

    def __isub__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] -= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] -= other_data[i]
        return self

    def __imul__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] *= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] *= other_data[i]
        return self

    def __idiv__(self, other):
        return self.__itruediv__(other)

    def __itruediv__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] /= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] /= other_data[i]
        return self

    def __ifloordiv__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] //= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] //= other_data[i]
        return self

    def __imod__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] %= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] %= other_data[i]
        return self

    def __ipow__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] **= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] **= other_data[i]
        return self

    def __lshift__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] << other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] << other_data[i]
        return ndarray

    def __rshift__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] >> other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] >> other_data[i]
        return ndarray

    def __and__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] & other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] & other_data[i]
        return ndarray

    def __or__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] | other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] | other_data[i]
        return ndarray

    def __xor__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] ^ other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] ^ other_data[i]
        return ndarray

    def __ilshift__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] << other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] << other_data[i]
        return self

    def __irshift__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] >> other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] >> other_data[i]
        return self

    def __iand__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] & other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] & other_data[i]
        return self

    def __ior__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] | other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] | other_data[i]
        return self

    def __ixor__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] ^ other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] ^ other_data[i]
        return self

    def __invert__(self):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        for i in range(len(data)):
            ndarray_data[i] = ~data[i]
        return ndarray

    def _get_data(self, other):
        if not isinstance(other, Ndarray):
            if isinstance(other, list):
                other = Ndarray(other, self._dtype)
            else:
                other = Ndarray(list(other), self._dtype)
        if self._shape != other._shape:
            raise TypeError("array shapes are not compatible")
        return other._data

    def _get_array(self, other):
        if not isinstance(other, Ndarray):
            if isinstance(other, list):
                other = Ndarray(other, self._dtype)
            else:
                other = Ndarray(list(other), self._dtype)
        return other

    def op(self, operator, other):
        """
        Arithemtic operation across array elements.
        Arguments include operator and int/array.
        Operators: 'add', 'sub', 'mul', 'div', etc.
        Return array of the operation.
        Note: operator special methods not called in
        Pyjs --optimized mode unless build with
        the --enable-operator-funcs option.
        """
        return getattr(self, '__'+operator+'__')(other)

    def cmp(self, operator, other):
        """
        Comparison operation across array elements.
        Arguments include operator and int/array.
        Operators: 'lt', 'le', 'eq', 'ne', 'gt', 'ge'.
        Return comparison array.
        Note: comparison special methods not called.
        """
        return getattr(self, '__'+operator+'__')(other)

    def matmul(self, other):
        """
        Matrix multiplication.
        Argument is an int or array.
        Return matrix multiplied array.
        """
        return self.__matmul__(other)

    def reshape(self, dim):
        """
        Return view of array with new shape.
        Argument is new shape.
        Raises TypeError if shape is not appropriate.
        """
        size = 1
        for i in dim:
            size *= i
        array_size = 1
        for i in self._shape:
            array_size *= i
        if size != array_size:
            raise TypeError("array size cannot change")
        subarray = self._data.subarray(0)
        array = Ndarray(subarray)
        array._shape = dim
        indices = []
        for i in array._shape:
            size /= i
            indices.append(size)
        array._indices = tuple(indices)
        return array

    def set(self, data):
        """
        Set array elements.
        Data argument can be a 1d/2d array or number used to set Ndarray elements, data used repetitively if consists of fewer elements than Ndarray.
        """
        if isinstance(data, (list,tuple)):
            if pyjs_mode.optimized:
                if isinstance(data[0], (list,tuple,TypedArray)):
                    data = [value for dat in data for value in dat]
            else:
                if not isinstance(data[0], (list,tuple,TypedArray)):
                    data = [dat.valueOf() for dat in data]
                else:
                    data = [value.valueOf() for dat in data for value in dat]
            dataLn = len(data)
            data = data.getArray()
        elif isinstance(data, (Ndarray,TypedArray)):
            data = data.getArray()
            dataLn = data.length
        else:
            if pyjs_mode.optimized:
                for index in range(self._data._data.length):
                    JS("@{{self}}['_data']['_data'][@{{index}}]=@{{data}};")
            else:
                data = data.valueOf()
                for index in range(self._data._data.length):
                    JS("@{{self}}['_data']['_data'][@{{index}}]=@{{data}};")
            return None
        if dataLn == self._data._data.length:
            for index in range(self._data._data.length):
                JS("@{{self}}['_data']['_data'][@{{index}}]=@{{data}}[@{{index}}];")
        else:
            for index in range(self._data._data.length):
                JS("@{{self}}['_data']['_data'][@{{index}}]=@{{data}}[@{{index}}%@{{dataLn}}];")
        return None

    def fill(self, value):
        """
        Set array elements to value argument.
        """
        if pyjs_mode.optimized:
            for index in range(self._data._data.length):
                JS("@{{self}}['_data']['_data'][@{{index}}]=@{{value}};")
        else:
            value = value.valueOf()
            for index in range(self._data._data.length):
                JS("@{{self}}['_data']['_data'][@{{index}}]=@{{value}};")
        return None

    def copy(self):
        """
        Return copy of array.
        """
        array = self._data.__class__(self._data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        return ndarray

    def empty(self):
        """
        Return empty copy of array.
        """
        ndarray = Ndarray(len(self._data), self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        return ndarray

    def astype(self, dtype):
        """
        Return copy of array.
        Argument dtype is TypedArray data type.
        """
        typedarray = self.__typedarray[self.__dtypes[dtype]]
        array = typedarray(self._data)
        ndarray = Ndarray(array, dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        return ndarray

    def view(self):
        """
        Return view of array.
        """
        subarray = self._data.subarray(0)
        array = Ndarray(subarray)
        array._shape = self._shape
        array._indices = self._indices
        return array

    def swapaxes(self, axis1, axis2):
        """
        Swap axes of array.
        Arguments are the axis to swap.
        Return view of array with axes changed.
        """
        array = Ndarray(self._data, self._dtype)
        shape = list(self._shape)
        shape[axis1], shape[axis2] = shape[axis2], shape[axis1]
        array._shape = tuple(shape)
        indices = list(self._indices)
        indices[axis1], indices[axis2] = indices[axis2], indices[axis1]
        array._indices = tuple(indices)
        return array

    def tolist(self):
        """
        Return array as a list.
        """
        def to_list(array, l):
            if hasattr(array[0], '__iter__'):
                if len(l) == 0:
                    _l = l
                else:
                    l = [l]
                    _l = l[0]
                for i, a in enumerate(array):
                    _l.append([])
                    to_list(a, _l[i])
            else:
                l.extend([v for v in array])
            return l
        return to_list(self, [])

    def getArray(self):
        """
        Return JavaScript TypedArray.
        """
        return self._data.getArray()


class NP(object):

    def zeros(self, size, dtype):
        """
        Return Ndarray of size and dtype with zeroed values.
        """
        return Ndarray(size, dtype)

    def swapaxes(self, array, axis1, axis2):
        """
        Return array with axes swapped.
        """
        return array.swapaxes(axis1, axis2)

    def append(self, array, values):
        """
        Return Ndarray set with array extended with values.
        """
        if isinstance(values[0], (list,tuple,TypedArray)):
            values = [value for dat in values for value in dat]
        newarray = Ndarray(len(array)+len(values), array._dtype)
        newarray._data.set(array._data)
        newarray._data.set(values, len(array))
        return newarray

np = NP()


class ImageData(object):

    def __init__(self, imagedata):
        """
        Provides an interface to canvas ImageData.
        The argument required is the ImageData instance to be accessed.
        """
        self._imagedata = imagedata
        if not isUndefined(TypedArray.__obj['Uint8ClampedArray']):
            self.data = Uint8ClampedArray()
        else:
            self.data = CanvasPixelArray()
        self.data._data = imagedata.data
        self.width = imagedata.width
        self.height = imagedata.height

    def getImageData(self):
        """
        Return JavaScript ImageData instance.
        """
        return self._imagedata


class ImageMatrix(Ndarray):

    def __init__(self, imagedata):
        """
        Provides an interface to canvas ImageData as an Ndarray array.
        The argument required is the ImageData instance to be accessed.
        """
        self._imagedata = ImageData(imagedata)
        if isinstance(self._imagedata.data, Uint8ClampedArray):
            Ndarray.__init__(self, self._imagedata.data, 'uint8c')
        else:
            Ndarray.__init__(self, self._imagedata.data, 'uint8')
        self.setshape(self._imagedata.height,self._imagedata.width,4)

    shape = Ndarray.shape

    def getWidth(self):
        """
        Return ImageData width.
        """
        return self._imagedata.width

    def getHeight(self):
        """
        Return ImageData height.
        """
        return self._imagedata.height

    def getPixel(self, index):
        """
        Get pixel RGBA.
        The index arguement references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return (self._imagedata.data[i], self._imagedata.data[i+1], self._imagedata.data[i+2], self._imagedata.data[i+3])

    def setPixel(self, index, value):
        """
        Set pixel RGBA.
        The arguements index references the 2D array element and value is pixel RGBA.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self._imagedata.data[i], self._imagedata.data[i+1], self._imagedata.data[i+2], self._imagedata.data[i+3] = value[0], value[1], value[2], value[3]
        return None

    def getPixelRGB(self, index):
        """
        Get pixel RGB.
        The index arguement references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return (self._imagedata.data[i], self._imagedata.data[i+1], self._imagedata.data[i+2])

    def setPixelRGB(self, index, value):
        """
        Set pixel RGB.
        The arguements index references the 2D array element and value is pixel RGB.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self._imagedata.data[i], self._imagedata.data[i+1], self._imagedata.data[i+2] = value[0], value[1], value[2]
        return None

    def getPixelAlpha(self, index):
        """
        Get pixel alpha.
        The index arguement references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return self._imagedata.data[i+3]

    def setPixelAlpha(self, index, value):
        """
        Set pixel alpha.
        The arguements index references the 2D array element and value is pixel alpha.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self._imagedata.data[i+3] = value
        return None

    def getPixelInteger(self, index):
        """
        Get pixel integer color.
        The index arguement references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return self._imagedata.data[i]<<16 | self._imagedata.data[i+1]<<8 | self._imagedata.data[i+2] | self.imagedata.data[i+3]<<24

    def setPixelInteger(self, index, value):
        """
        Set pixel integer color.
        The arguements index references the 2D array element and value is pixel color.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self._imagedata.data[i], self._imagedata.data[i+1], self._imagedata.data[i+2], self._imagedata.data[i+3] = value>>16 & 0xff, value>>8 & 0xff, value & 0xff, value>>24 & 0xff
        return None

    def getImageData(self):
        """
        Return JavaScript ImageData instance.
        """
        return self._imagedata.getImageData()


class BitSet(object):

    """
    BitSet provides a bitset object to use in a Python-to-JavaScript application. The object stores data in a JavaScript Uint8Array 8-bit typedarray. BitSet16 and BitSet32 stores data in Uint16Array (16-bit) and Uint32Array (32-bit) typedarray. The BitSet will dynamically expand to hold the bits required, an optional width argument define number of bits the BitSet instance will initially hold.
    """

    _bit = 8
    _bitmask = None
    __typedarray = Uint8Array

    def __init__(self, width=None):
        if not self._bitmask:
            self._bitmask = dict([(self._bit-i-1,1<<i) for i in range(self._bit-1,-1,-1)])
            self._bitmask[self._bit-1] = int(self._bitmask[self._bit-1])      #pyjs [1<<0] = 1L
        if width:
            self._width = abs(width)
        else:
            self._width = self._bit
        self._data = self.__typedarray( _ceil(self._width/(self._bit*1.0)) )

    def __str__(self):
        v = {True:'1', False:'0'}
        s = []
        for i in range(self.size()):
            s.append(v[self.get(i)])
            if not (i+1)%64:
                s.append('\n')
        return ''.join(s)

    def __repr__(self):
        setBit = []
        for index in range(self._width):
            if self.get(index):
                setBit.append(str(index))
        return "{" + ", ".join(setBit) + "}"

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, value):
        self.set(index, value)

    def __len__(self):
        for index in range(self._width-1, -1, -1):
            if self.get(index):
                break
        return index+1

    def __iter__(self):
        index = 0
        while index < self._width:
            yield self.get(index)
            index += 1

    def get(self, index, toIndex=None):
        """
        Get bit by index.
        Arguments include index of bit, and optional toIndex that return a slice as a BitSet.
        """
        if index > self._width-1:
            if not toIndex:
                return False
            else:
                size = toIndex-index
                if size > 0:
                    return self.__class__(size)
                else:
                    return None
        if toIndex is None:
            return bool( self._data[ int(index/self._bit) ] & self._bitmask[ index%self._bit ] )
        else:
            size = toIndex-index
            if size > 0:
                bitset = self.__class__(size)
                ix = 0
                if toIndex > self._width:
                    toIndex = self._width
                for i in range(index, toIndex):
                    bitset.set(ix, bool( self._data[ int(i/self._bit) ] & self._bitmask[ i%self._bit ] ))
                    ix += 1
                return bitset
            else:
                return None

    def set(self, index, value=1):
        """
        Set bit by index.
        Optional argument value is the bit state of 1(True) or 0(False). Default:1
        """
        if index > self._width-1:
            if value:
                self.resize(index+1)
            else:
                return
        if value:
            self._data[ int(index/self._bit) ] = self._data[ int(index/self._bit) ] | self._bitmask[ index%self._bit ]
#            self._data[ int(index/self._bit) ] |= self._bitmask[ index%self._bit ]    #pyjs -O: |= not processed
        else:
            self._data[ int(index/self._bit) ] = self._data[ int(index/self._bit) ] & ~(self._bitmask[ index%self._bit ])
#            self._data[ int(index/self._bit) ] &= ~(self._bitmask[ index%self._bit ])     #pyjs -O: &= not processed
        return None

    def fill(self, index=None, toIndex=None):
        """
        Set the bit. If no argument provided, all bits are set.
        Optional argument index is bit index to set, and toIndex to set a range of bits.
        """
        if index is None and toIndex is None:
            for i in range(0, self._width):
                self.set(i, 1)
        else:
            if toIndex is None:
                self.set(index, 1)
            else:
                for i in range(index, toIndex):
                    self.set(i, 1)

    def clear(self, index=None, toIndex=None):
        """
        Clear the bit. If no argument provided, all bits are cleared.
        Optional argument index is bit index to clear, and toIndex to clear a range of bits.
        """
        if index is None:
            for i in range(len(self._data)):
                self._data[i] = 0
        else:
            if toIndex is None:
                self.set(index, 0)
            else:
                if index == 0 and toIndex == self._width:
                    for dat in range(len(self._data)):
                        self._data[dat] = 0
                else:
                    for i in range(index, toIndex):
                        self.set(i, 0)

    def flip(self, index, toIndex=None):
        """
        Flip the state of the bit.
        Argument index is the bit index to flip, and toIndex to flip a range of bits.
        """
        if toIndex is None:
            self.set(index, not self.get(index))
        else:
            if toIndex > self._width:
                self.resize(toIndex)
                toIndex = self._width
            if index == 0 and toIndex == self._width:
                for dat in range(len(self._data)):
                    self._data[dat] = ~self._data[dat]
            else:
                for i in range(index, toIndex):
                    self.set(i, not self.get(i))

    def cardinality(self):
        """
        Return the count of bit set.
        """
        count = 0
        for bit in range(self._width):
            if self.get(bit):
                count += 1
        return count

    def intersects(self, bitset):
        """
        Check if set bits in this BitSet are also set in the bitset argument.
        Return True if bitsets intersect, otherwise return False.
        """
        for dat in range(len(bitset._data)):
            if bitset._data[dat] & self._data[dat]:
                return True
        return False

    def andSet(self, bitset):
        """
        BitSet and BitSet.
        """
        data = min(len(self._data), len(bitset._data))
        for dat in range(data):
            self._data[dat] = self._data[dat] & bitset._data[dat]
#            self._data[dat] &= bitset._data[dat]     #pyjs -O: &= not processed
#        pyjs -S: &= calls __and__ instead of __iand__, -O: no call to operator methods

    def orSet(self, bitset):
        """
        BitSet or BitSet.
        """
        data = min(len(self._data), len(bitset._data))
        for dat in range(data):
            self._data[dat] = self._data[dat] | bitset._data[dat]
#            self._data[dat] |= bitset._data[dat]    #pyjs -O: |= not processed

    def xorSet(self, bitset):
        """
        BitSet xor BitSet.
        """
        data = min(len(self._data), len(bitset._data))
        for dat in range(data):
            self._data[dat] = self._data[dat] ^ bitset._data[dat]
#            self._data[dat] ^= bitset._data[dat]    #pyjs -O: |= not processed

    def resize(self, width):
        """
        Resize the BitSet to width argument.
        """
        if width > self._width:
            self._width = width
            if self._width > len(self._data) * self._bit:
                array = self.__typedarray( _ceil(self._width/(self._bit*1.0)) )
                array.set(self._data)
                self._data = array
        elif width < self._width:
            if width < len(self):
                width = len(self)
            self._width = width
            if self._width <= len(self._data) * self._bit - self._bit:
                array = self.__typedarray( _ceil(self._width/(self._bit*1.0)) )
                array.set(self._data.subarray(0,_ceil(self._width/(self._bit*1.0))))
                self._data = array

    def size(self):
        """
        Return bits used by BitSet storage array.
        """
        return len(self._data) * self._bit

    def isEmpty(self):
        """
        Check whether any bit is set.
        Return True if none set, otherwise return False.
        """
        for data in self._data:
            if data:
                return False
        return True

    def clone(self):
        """
        Return a copy of the BitSet.
        """
        new_bitset = self.__class__(1)
        data = self.__typedarray(self._data)
        new_bitset._data = data
        new_bitset._width = self._width
        return new_bitset


class BitSet16(BitSet):
    """
    BitSet using Uint16Array typedarray.
    """
    _bit = 16
    _bitmask = None
    __typedarray = Uint16Array

    def __init__(self, width=None):
        BitSet.__init__(self, width)


class BitSet32(BitSet):
    """
    BitSet using Uint32Array typedarray.
    """
    _bit = 32
    _bitmask = None
    __typedarray = Uint32Array

    def __init__(self, width=None):
        BitSet.__init__(self, width)


def typeOf(obj):
    """
    Return typeof obj.
    """
    if pyjs_mode.optimized:
        return JS("typeof @{{obj}};")
    else:
        return JS("typeof @{{obj}}['valueOf']();")


class PyjsMode(object):

    def __init__(self):
        self.strict, self.optimized = self._setmode()

    def __getattr__(self, attr):
        if attr == '__strict_mode':
            return True

    def _setmode(self):
        if self.__strict_mode == True:
            return True, False
        else:
            return False, True

pyjs_mode = PyjsMode()


#depreciated
PyTypedArray = TypedArray
PyUint8ClampedArray = Uint8ClampedArray
PyUint8Array = Uint8Array
PyUint16Array = Uint16Array
PyUint32Array = Uint32Array
PyInt8Array = Int8Array
PyInt16Array = Int16Array
PyInt32Array = Int32Array
PyFloat32Array = Float32Array
PyFloat64Array = Float64Array
PyCanvasPixelArray = CanvasPixelArray
PyImageData = ImageData
PyImageMatrix = ImageMatrix

