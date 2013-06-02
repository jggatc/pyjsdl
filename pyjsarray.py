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

    def __init__(self, data, offset=0, length=None, typedarray=None):
        """
        The PyTypedArray is instantiated with either the array size, an array of the TypedArray or Python type, or an existing ArrayBuffer to view, which creates a new TypedArray of size and included data as the specified type. Optional arguments include offset index at which ArrayBuffer data is inserted and length of an ArrayBuffer. The PyTypedArray interface to the TypedArray object include index syntax, iteration, and math operations.
        """
        if isinstance(data, int):
            self.__array = typedarray(float(data))
        elif isinstance(data, list):
            data = [float(dat) for dat in data]
            self.__array = typedarray(data.getArray())
        elif isinstance(data, PyTypedArray):
            self.__array = typedarray(data.__array)
        elif isinstance(data, tuple) and data[0] == 'subarray':
            self.__array = data[1]
        else:
            if length is None:
                self.__array = typedarray(data, offset)
            else:
                self.__array = typedarray(data, offset, length)

    def __str__(self):
        """
        Return string representation of PyTypedArray object.
        """
        return self.__array.toString()

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
        return self.__array.length

    def set(self, data, offset=0):
        """
        Set data to the array. Arguments: data is a list of either the TypedArray or Python type, offset is the start index where data will be set (defaults to 0).
        """
        if isinstance(data, list):
            data = [float(dat) for dat in data]
            data = data.getArray()
            self.__array.set(data, offset)
        elif isinstance(data, PyTypedArray):
            self.__array.set(data.__array, offset)

    def subarray(self, begin, end=None):
        """
        Retrieve a subarray of the array. The subarray is a TypedArray and is a view of the derived array. Arguments begin and optional end (defaults to array end) are the index spanning the subarray.
        """
        if end is None:
            end = self.__array.length
        array = self.__array.subarray(begin, end)
        return PyTypedArray(('subarray', array))

    def getLength(self):
        """
        Return array.length attribute.
        """
        return self.__array.length

    def getByteLength(self):
        """
        Return array.byteLength attribute.
        """
        return self.__array.byteLength

    def getBuffer(self):
        """
        Return array.buffer attribute.
        """
        return self.__array.buffer

    def getByteOffset(self):
        """
        Return array.byteOffset attribute.
        """
        return self.__array.byteOffset

    def getBytesPerElement(self):
        """
        Return array.BYTES_PER_ELEMENT attribute.
        """
        return self.__array.BYTES_PER_ELEMENT

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
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Uint8ClampedArray)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError, 'TypedArray data type not implemented'
            else:
                raise


class PyUint8Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Uint8Array.
    """

    def __init__(self, data, offset=0, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Uint8Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError, 'TypedArray data type not implemented'
            else:
                raise


class PyUint16Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Uint16Array.
    """

    def __init__(self, data, offset=0, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Uint16Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError, 'TypedArray data type not implemented'
            else:
                raise


class PyUint32Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Uint32Array.
    """

    def __init__(self, data, offset=0, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Uint32Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError, 'TypedArray data type not implemented'
            else:
                raise


class PyInt8Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Int8Array.
    """

    def __init__(self, data, offset=0, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Int8Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError, 'TypedArray data type not implemented'
            else:
                raise


class PyInt16Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Int16Array.
    """

    def __init__(self, data, offset=0, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Int16Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError, 'TypedArray data type not implemented'
            else:
                raise


class PyInt32Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Int32Array.
    """

    def __init__(self, data, offset=0, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Int32Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError, 'TypedArray data type not implemented'
            else:
                raise


class PyFloat32Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Float32Array.
    """

    def __init__(self, data, offset=0, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Float32Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError, 'TypedArray data type not implemented'
            else:
                raise

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
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Float64Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError, 'TypedArray data type not implemented'
            else:
                raise

    def __getitem__(self, index):
        """
        Get TypedArray element by index.
        """
        return JS("""@{{self}}['__array'][@{{index}}];""")

