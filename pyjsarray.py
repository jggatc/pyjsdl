#PyjsArray - Copyright (C) 2013 James Garnon

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#PyjsArray version 0.5
#Project Site: http://gatc.ca

from __pyjamas__ import JS


class PyTypedArray:

    """
    PyTypedArray is the base class that wraps the JavaScript TypedArray objects.
    The derived objects provides an interface to the JavaScript array objects:
        PyUint8ClampedArray     [Uint8ClampedArray]
        PyUint8Array            [Uint8Array]
        PyUint16Array           [Uint16Array]
        PyUint32Array           [Uint32Array]
        PyInt8Array             [Int8Array]
        PyInt16Array            [Int16Array]
        PyInt32Array            [Int32Array]
        PyFloat32Array          [Float32Array]
        PyFloat64Array          [Float64Array]
    """

    def __init__(self, data, offset=0, length=None):
        """
        The PyTypedArray is instantiated with either the array size, an array of the TypedArray or Python type, or an existing ArrayBuffer to view, which creates a new TypedArray of size and included data as the specified type. Optional arguments include offset index at which ArrayBuffer data is inserted and length of an ArrayBuffer. The PyTypedArray interface to the TypedArray object include index syntax, iteration, and math operations.
        """
        if isinstance(data, int):
            data = float(data)
            JS("""@{{self}}['__array'] = new __typedarray(@{{data}});""")
        elif isinstance(data, list):
            size = float( len(data)+offset )
            JS("""@{{self}}['__array'] = new __typedarray(@{{size}});""")
            for index, dat in enumerate(data):
                dat = float(dat)
                JS("""@{{self}}['__array'][@{{index}}+@{{offset}}] = @{{dat}};""")
        elif isinstance(data, PyTypedArray):
            JS("""@{{self}}['__array'] = new __typedarray(@{{data}}['__array'],@{{offset}});""")
        elif isinstance(data, tuple) and data[0] == 'subarray':
            self.__array = data[1]
        else:
            if length is None:
                JS("""@{{self}}['__array'] = new __typedarray(@{{data}},@{{offset}});""")
            else:
                JS("""@{{self}}['__array'] = new __typedarray(@{{data}},@{{offset}},@{{length}});""")

    def __str__(self):
        """
        Return string representation of PyTypedArray object.
        """
        return JS("""@{{self}}['__array'].toString();""")

    def __getitem__(self, index):
        """
        Get TypedArray element by index.
        """
        return JS("""@{{int}}(@{{self}}['__array'][@{{index}}]);""")

    def __setitem__(self, index, value):
        """
        Set TypedArray element by index.
        """
        value = float(value)
        JS("""@{{self}}['__array'][@{{index}}]=@{{value}};""")
        return None

    def __len__(self):
        """
        Get TypedArray array length.
        """
        return JS("""@{{self}}['__array'].length;""")

    def set(self, data, offset=0):
        """
        Set data to the array. Arguments: data is a list of either the TypedArray or Python type, offset is the start index where data will be set (defaults to 0).
        """
        if isinstance(data, list):
            length = JS("""@{{self}}['__array'].length;""")
            if len(data) > (length-offset):
                JS("""throw RangeError("invalid array length");""")
            for dat in data:
                dat = float(dat)
                JS("""@{{self}}['__array'][@{{offset}}++] = @{{dat}};""")
        elif isinstance(data, PyTypedArray):
            JS("""@{{self}}['__array'].set(@{{data}}['__array'],@{{offset}});""")

    def subarray(self, begin, end=None):
        """
        Retrieve a subarray of the array. The subarray is a TypedArray and is a view of the derived array. Arguments begin and optional end (defaults to array end) are the index spanning the subarray.
        """
        if end is None:
            end = JS("""@{{self}}['__array'].length;""")
        array = JS("""@{{self}}['__array'].subarray(@{{begin}},@{{end}});""")
        return PyTypedArray(('subarray', array))

    def getLength(self):
        """
        Return array.length attribute.
        """
        return JS("""@{{self}}['__array'].length;""")

    def getByteLength(self):
        """
        Return array.byteLength attribute.
        """
        return JS("""@{{self}}['__array'].byteLength;""")

    def getBuffer(self):
        """
        Return array.buffer attribute.
        """
        return JS("""@{{self}}['__array'].buffer;""")

    def getByteOffset(self):
        """
        Return array.byteOffset attribute.
        """
        return JS("""@{{self}}['__array'].byteOffset;""")

    def getBytesPerElement(self):
        """
        Return array.BYTES_PER_ELEMENT attribute.
        """
        return JS("""@{{self}}['__array'].BYTES_PER_ELEMENT;""")

    def getArray(self):
        """
        Return JavaScript TypedArray.
        """
        return self.__array


class PyUint8ClampedArray(PyTypedArray):
    """
    Create a PyTypedArray interface to Uint8ClampedArray.
    """

    def __init__(self, data, offset=0, length=None):
        JS("""__typedarray = Uint8ClampedArray;""")
        PyTypedArray.__init__(self, data, offset, length)


class PyUint8Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Uint8Array.
    """

    def __init__(self, data, offset=0, length=None):
        JS("""__typedarray = Uint8Array;""")
        PyTypedArray.__init__(self, data, offset, length)


class PyUint16Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Uint16Array.
    """

    def __init__(self, data, offset=0, length=None):
        JS("""__typedarray = Uint16Array;""")
        PyTypedArray.__init__(self, data, offset, length)


class PyUint32Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Uint32Array.
    """

    def __init__(self, data, offset=0, length=None):
        JS("""__typedarray = Uint32Array;""")
        PyTypedArray.__init__(self, data, offset, length)


class PyInt8Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Int8Array.
    """

    def __init__(self, data, offset=0, length=None):
        JS("""__typedarray = Int8Array;""")
        PyTypedArray.__init__(self, data, offset, length)


class PyInt16Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Int16Array.
    """

    def __init__(self, data, offset=0, length=None):
        JS("""__typedarray = Int16Array;""")
        PyTypedArray.__init__(self, data, offset, length)


class PyInt32Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Int32Array.
    """

    def __init__(self, data, offset=0, length=None):
        JS("""__typedarray = Int32Array;""")
        PyTypedArray.__init__(self, data, offset, length)


class PyFloat32Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Float32Array.
    """

    def __init__(self, data, offset=0, length=None):
        JS("""__typedarray = Float32Array;""")
        PyTypedArray.__init__(self, data, offset, length)

    def __getitem__(self, index):
        """
        Get TypedArray element by index.
        """
        return JS("""@{{self}}['__array'][@{{index}}];""")


class PyFloat64Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Float64Array.
    """

    def __init__(self, data, offset=0, length=None):
        JS("""__typedarray = Float64Array;""")
        PyTypedArray.__init__(self, data, offset, length)

    def __getitem__(self, index):
        """
        Get TypedArray element by index.
        """
        return JS("""@{{self}}['__array'][@{{index}}];""")

