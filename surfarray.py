#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

#from __future__ import division
from pyjsdl.surface import Surface
from pyjsdl.pyjsarray import PyUint8ClampedArray, PyUint8Array, PyUint32Array, Ndarray, PyImageData, PyImageMatrix

__docformat__ = 'restructuredtext'


class Surfarray(object):
    """
    **pyjsdl.surfarray**

    * pyjsdl.surfarray.array
    * pyjsdl.surfarray.array2d
    * pyjsdl.surfarray.array3d
    * pyjsdl.surfarray.array_alpha
    * pyjsdl.surfarray.make_surface
    * pyjsdl.surfarray.blit_array
    """

    def __init__(self):
        """
        Provides image pixel manipulation method.
        ImageData can be retrieved as Ndarray data in different pixel format.
        The array can be passed as ImageData to a Surface.

        Module initialization creates pyjsdl.surfarray instance.
        """
        self.initialized = False
        self._nonimplemented_methods()

    def array(self, surface):
        """
        Return data array of the Surface argument.
        Array consists of pixel data arranged by [y,x] in RGBA format.
        Data array most consistent to ImageData format.
        """
        imagedata = surface.impl.getImageData(0, 0, surface.width, surface.height)
        return PyImageMatrix(imagedata)

    def array2d(self, surface, copydata=False):
        """
        Return data array of the Surface argument.
        Array consists of pixel data arranged by [x,y] in integer color format.
        Provides an interface to ImageData format.
        Alternatively, creates a new formatted array if optional copydata argument is True.
        """
        imagedata = surface.impl.getImageData(0, 0, surface.width, surface.height)
        if not copydata:
            return PyImageMatrixInteger(imagedata)
        else:
            return PyImageInteger(imagedata)

    def array3d(self, surface, copydata=False):
        """
        Return data array of the Surface argument.
        Array consists of pixel data arranged by [x,y] in RGB format.
        Provides an interface to ImageData format.
        Alternatively, creates a new formatted array if optional copydata argument is True.
        """
        imagedata = surface.impl.getImageData(0, 0, surface.width, surface.height)
        if not copydata:
            return PyImageMatrixRGB(imagedata)
        else:
            return PyImageRGB(imagedata)

    def array_alpha(self, surface, copydata=False):
        """
        Return data array of the Surface argument.
        Array consists of pixel data arranged by [x,y] of pixel alpha value.
        Provides an interface to ImageData format.
        Alternatively, creates a new formatted array if optional copydata argument is True.
        """
        imagedata = surface.impl.getImageData(0, 0, surface.width, surface.height)
        if not copydata:
            return PyImageMatrixAlpha(imagedata)
        else:
            return PyImageAlpha(imagedata)

    def make_surface(self, array):
        """
        Generates image pixels from array data.
        Argument array containing image data.
        Return Surface generated from array.
        """
        surface = Surface((array.__imagedata.width,array.__imagedata.height))
        self.blit_array(surface, array)
        return surface

    def blit_array(self, surface, array):
        """
        Generates image pixels from array data.
        Arguments include surface to generate the image, and array containing image data.
        """
        try:
            imagedata = array.getImageData()
        except (TypeError, AttributeError):     #-O/-S: TypeError/AttributeError
            imagedata = surface.impl.getImageData(0, 0, surface.width, surface.height)
            if len(array._shape) == 2:
                array2d = PyImageMatrix(imagedata)
                for y in xrange(array2d.getHeight()):
                    for x in xrange(array2d.getWidth()):
                        value = array[x,y]
                        array2d[y,x] = (value>>16 & 0xff, value>>8 & 0xff, value & 0xff, 255)
                imagedata = array2d.getImageData()
            else:
                imagedata.data.set(array.getArray())
        surface.impl.putImageData(imagedata, 0, 0, 0, 0, surface.width, surface.height)
        return None

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.use_arraytype = lambda *arg: None


class PyImageMatrixRGB(PyImageMatrix):
    """
    Array consists of pixel data arranged by width/height in RGB format.
    Interface to ImageData.
    """

    def __getitem__(self, index):
        index = list(index)
        index[0], index[1] = index[1], index[0]
        index = tuple(index)
        return PyImageMatrix.__getitem__(self, index)

    def __setitem__(self, index, value):
        index = list(index)
        index[0], index[1] = index[1], index[0]
        index = tuple(index)
        return PyImageMatrix.__setitem__(self, index, value)


class PyImageRGB(Ndarray):
    """
    Array consists of pixel data arranged by width/height in RGB format.
    Array data derived from ImageData.
    """

    def __init__(self, imagedata):
        self.__imagedata = PyImageData(imagedata)
        array = Ndarray(self.__imagedata.data)
        array.setshape(self.__imagedata.height,self.__imagedata.width,4)
        try:
            data = PyUint8ClampedArray(self.__imagedata.height*self.__imagedata.width*3)
        except NotImplementedError:     #ie10 supports typedarray, not uint8clampedarray
            data = PyUint8Array(self.__imagedata.height*self.__imagedata.width*3)
        index = 0
        for x in xrange(self.__imagedata.width):
            for y in xrange(self.__imagedata.height):
                for i in xrange(3):
                    data[index] = array[y,x,i]
                    index += 1
        try:
            Ndarray.__init__(self, data, 0)
        except NotImplementedError:
            Ndarray.__init__(self, data, 1)
        self.setshape(self.__imagedata.width,self.__imagedata.height,3)

    def getImageData(self):
        index = 0
        for x in xrange(self.__imagedata.height):
            for y in xrange(self.__imagedata.width):
                for i in xrange(3):
                    self.__imagedata.data[index+i] = self[y,x,i]
                index += 4
        return self.__imagedata.getImageData()


class PyImageMatrixAlpha(PyImageMatrix):
    """
    Array consists of pixel data arranged by width/height of pixel alpha value.
    Interface to ImageData.
    """

    def __getitem__(self, index):
        return PyImageMatrix.__getitem__(self, (index[1],index[0],3))

    def __setitem__(self, index, value):
        return PyImageMatrix.__setitem__(self, (index[1],index[0],3), value)


class PyImageAlpha(Ndarray):
    """
    Array consists of pixel data arranged by width/height of pixel alpha value.
    Array data derived from ImageData.
    """

    def __init__(self, imagedata):
        self.__imagedata = PyImageData(imagedata)
        array = Ndarray(self.__imagedata.data)
        array.setshape(self.__imagedata.height,self.__imagedata.width,4)
        try:
            data = PyUint8ClampedArray(self.__imagedata.height*self.__imagedata.width)
        except NotImplementedError:     #ie10 supports typedarray, not uint8clampedarray
            data = PyUint8Array(self.__imagedata.height*self.__imagedata.width)
        index = 0
        for x in xrange(self.__imagedata.width):
            for y in xrange(self.__imagedata.height):
                data[index] = array[y,x,3]
                index += 1
        try:
            Ndarray.__init__(self, data, 0)
        except NotImplementedError:
            Ndarray.__init__(self, data, 1)
        self.setshape(self.__imagedata.width,self.__imagedata.height)

    def getImageData(self):
        index = 0
        for x in xrange(self.__imagedata.height):
            for y in xrange(self.__imagedata.width):
                self.__imagedata.data[index+3] = self[y,x]
                index += 4
        return self.__imagedata.getImageData()


class PyImageMatrixInteger(PyImageMatrix):
    """
    Array consists of pixel data arranged by width/height in integer color format.
    Interface to ImageData.
    """

    def __getitem__(self, index):
        value = PyImageMatrix.__getitem__(self, (index[1],index[0]))
        return value[0]<<16 | value[1]<<8 | value[2] | value[3]<<24

    def __setitem__(self, index, value):
        return PyImageMatrix.__setitem__(self, (index[1],index[0]), (value>>16 & 0xff, value>>8 & 0xff, value & 0xff, value>>24 & 0xff))


class PyImageInteger(Ndarray):
    """
    Array consists of pixel data arranged by width/height in integer color format.
    Array data derived from ImageData.
    """

    def __init__(self, imagedata):
        self.__imagedata = PyImageData(imagedata)
        array = Ndarray(self.__imagedata.data)
        array.setshape(self.__imagedata.height,self.__imagedata.width,4)
        data = PyUint32Array(self.__imagedata.height*self.__imagedata.width)
        index = 0
        for x in xrange(self.__imagedata.width):
            for y in xrange(self.__imagedata.height):
                data[index] = array[y,x,0]<<16 | array[y,x,1]<<8 | array[y,x,2] | array[y,x,3]<<24
                index += 1
        Ndarray.__init__(self, data, 3)
        self.setshape(self.__imagedata.width,self.__imagedata.height)

    def getImageData(self):
        index = 0
        for x in xrange(self.__imagedata.height):
            for y in xrange(self.__imagedata.width):
                self.__imagedata.data[index], self.__imagedata.data[index+1], self.__imagedata.data[index+2], self.__imagedata.data[index+3] = self[y,x]>>16 & 0xff, self[y,x]>>8 & 0xff, self[y,x] & 0xff, self[y,x]>>24 & 0xff
                index += 4
        return self.__imagedata.getImageData()

