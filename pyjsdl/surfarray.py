#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl.surface import Surface
from pyjsdl.pyjsarray import Ndarray
from pyjsdl.pyjsarray import Uint8ClampedArray
from pyjsdl.pyjsarray import Uint8Array
from pyjsdl.pyjsarray import Uint32Array
from pyjsdl.pyjsarray import ImageData
from pyjsdl.pyjsarray import ImageMatrix
import sys

if sys.version_info < (3,):
    from pyjsdl.util import _range as range

__docformat__ = 'restructuredtext'

__doc__ = 'Surface pixel manipulation'


def array(surface):
    """
    Return data array of the Surface argument.
    Array consists of pixel data arranged by [y,x] in RGBA format.
    Data array most consistent to ImageData format.
    """
    imagedata = surface.impl.getImageData(0, 0, surface.width, surface.height)
    return ImageMatrix(imagedata)


def array2d(surface, copydata=False):
    """
    Return data array of the Surface argument.
    Array consists of pixel data arranged by [x,y] in integer color format.
    Provides an interface to ImageData format.
    Creates a new formatted array if optional copydata argument is True.
    """
    imagedata = surface.impl.getImageData(0, 0, surface.width, surface.height)
    if not copydata:
        return ImageMatrixInteger(imagedata)
    else:
        return ImageInteger(imagedata)


def array3d(surface, copydata=False):
    """
    Return data array of the Surface argument.
    Array consists of pixel data arranged by [x,y] in RGB format.
    Provides an interface to ImageData format.
    Creates a new formatted array if optional copydata argument is True.
    """
    imagedata = surface.impl.getImageData(0, 0, surface.width, surface.height)
    if not copydata:
        return ImageMatrixRGB(imagedata)
    else:
        return ImageRGB(imagedata)


def array_alpha(surface, copydata=False):
    """
    Return data array of the Surface argument.
    Array consists of pixel data arranged by [x,y] of pixel alpha value.
    Provides an interface to ImageData format.
    Creates a new formatted array if optional copydata argument is True.
    """
    imagedata = surface.impl.getImageData(0, 0, surface.width, surface.height)
    if not copydata:
        return ImageMatrixAlpha(imagedata)
    else:
        return ImageAlpha(imagedata)


def make_surface(array):
    """
    Generates image pixels from array data.
    Argument array containing image data.
    Return Surface generated from array.
    """
    surface = Surface((array._imagedata.width,array._imagedata.height))
    blit_array(surface, array)
    return surface


def blit_array(surface, array):
    """
    Generates image pixels from array data.
    Arguments include destination Surface and array containing image data.
    """
    try:
        imagedata = array.getImageData()
    except (TypeError, AttributeError):
        imagedata = surface.impl.getImageData(0, 0, surface.width, surface.height)
        if len(array._shape) == 2:
            array2d = ImageMatrix(imagedata)
            for y in range(array2d.getHeight()):
                for x in range(array2d.getWidth()):
                    value = array[x,y]
                    array2d[y,x] = (value>>16 & 0xff,
                                    value>>8 & 0xff,
                                    value & 0xff,
                                    255)
            imagedata = array2d.getImageData()
        else:
            imagedata.data.set(array.getArray())
    surface.impl.putImageData(imagedata, 0, 0, 0, 0, surface.width, surface.height)
    return None


use_arraytype = lambda *arg: None


class ImageMatrixRGB(ImageMatrix):
    """
    Array of pixel data arranged by width/height in RGB format.
    Interface to ImageData.
    """

    shape = ImageMatrix.shape

    def __getitem__(self, index):
        index = list(index)
        index[0], index[1] = index[1], index[0]
        index = tuple(index)
        return ImageMatrix.__getitem__(self, index)

    def __setitem__(self, index, value):
        index = list(index)
        index[0], index[1] = index[1], index[0]
        index = tuple(index)
        ImageMatrix.__setitem__(self, index, value)
        return None

    def __repr__(self):
        return self.__str__()


class ImageRGB(Ndarray):
    """
    Array of pixel data arranged by width/height in RGB format.
    Array data derived from ImageData.
    """

    def __init__(self, imagedata):
        self._imagedata = ImageData(imagedata)
        array = Ndarray(self._imagedata.data)
        array.setshape(self._imagedata.height, self._imagedata.width, 4)
        try:
            data = Uint8ClampedArray(self._imagedata.height
                                    * self._imagedata.width * 3)
        except NotImplementedError:
            data = Uint8Array(self._imagedata.height
                             * self._imagedata.width * 3)
        index = 0
        for x in range(self._imagedata.width):
            for y in range(self._imagedata.height):
                for i in range(3):
                    data[index] = array[y, x, i]
                    index += 1
        try:
            Ndarray.__init__(self, data, 'uint8c')
        except NotImplementedError:
            Ndarray.__init__(self, data, 'uint8')
        self.setshape(self._imagedata.width, self._imagedata.height, 3)

    shape = Ndarray.shape

    def getImageData(self):
        """
        Get ImageData.
        """
        index = 0
        for x in range(self._imagedata.height):
            for y in range(self._imagedata.width):
                for i in range(3):
                    self._imagedata.data[index + i] = self[y, x, i]
                index += 4
        return self._imagedata.getImageData()


class ImageMatrixAlpha(ImageMatrix):
    """
    Array of pixel data arranged by width/height of pixel alpha value.
    Interface to ImageData.
    """

    shape = ImageMatrix.shape

    def __getitem__(self, index):
        return ImageMatrix.__getitem__(self, (index[1], index[0], 3))

    def __setitem__(self, index, value):
        ImageMatrix.__setitem__(self, (index[1], index[0], 3), value)
        return None

    def __repr__(self):
        return self.__str__()


class ImageAlpha(Ndarray):
    """
    Array of pixel data arranged by width/height of pixel alpha value.
    Array data derived from ImageData.
    """

    def __init__(self, imagedata):
        self._imagedata = ImageData(imagedata)
        array = Ndarray(self._imagedata.data)
        array.setshape(self._imagedata.height, self._imagedata.width, 4)
        try:
            data = Uint8ClampedArray(self._imagedata.height
                                    * self._imagedata.width)
        except NotImplementedError:
            data = Uint8Array(self._imagedata.height
                             * self._imagedata.width)
        index = 0
        for x in range(self._imagedata.width):
            for y in range(self._imagedata.height):
                data[index] = array[y, x, 3]
                index += 1
        try:
            Ndarray.__init__(self, data, 'uint8c')
        except NotImplementedError:
            Ndarray.__init__(self, data, 'uint8')
        self.setshape(self._imagedata.width, self._imagedata.height)

    shape = Ndarray.shape

    def getImageData(self):
        """
        Get ImageData.
        """
        index = 0
        for x in range(self._imagedata.height):
            for y in range(self._imagedata.width):
                self._imagedata.data[index + 3] = self[y, x]
                index += 4
        return self._imagedata.getImageData()


class ImageMatrixInteger(ImageMatrix):
    """
    Array of pixel data arranged by width/height in integer color format.
    Interface to ImageData.
    """

    shape = ImageMatrix.shape

    def __getitem__(self, index):
        value = ImageMatrix.__getitem__(self, (index[1], index[0]))
        return value[0]<<16 | value[1]<<8 | value[2] | value[3]<<24

    def __setitem__(self, index, value):
        ImageMatrix.__setitem__(self, (index[1], index[0]),
                                      (value>>16 & 0xff,
                                       value>>8 & 0xff,
                                       value & 0xff,
                                       value>>24 & 0xff))
        return None

    def __repr__(self):
        return self.__str__()


class ImageInteger(Ndarray):
    """
    Array of pixel data arranged by width/height in integer color format.
    Array data derived from ImageData.
    """

    def __init__(self, imagedata):
        self._imagedata = ImageData(imagedata)
        array = Ndarray(self._imagedata.data)
        array.setshape(self._imagedata.height, self._imagedata.width, 4)
        data = Uint32Array(self._imagedata.height
                          * self._imagedata.width)
        index = 0
        for x in range(self._imagedata.width):
            for y in range(self._imagedata.height):
                data[index] = (array[y, x, 0] << 16 |
                               array[y, x, 1] << 8 |
                               array[y, x, 2] |
                               array[y, x, 3] << 24)
                index += 1
        Ndarray.__init__(self, data, 'uint32')
        self.setshape(self._imagedata.width, self._imagedata.height)

    shape = Ndarray.shape

    def getImageData(self):
        """
        Get ImageData.
        """
        index = 0
        for x in range(self._imagedata.height):
            for y in range(self._imagedata.width):
                dat = self[y, x]
                self._imagedata.data[index] = dat>>16 & 0xff
                self._imagedata.data[index + 1] = dat>>8 & 0xff
                self._imagedata.data[index + 2] = dat & 0xff
                self._imagedata.data[index + 3] =  dat>>24 & 0xff
                index += 4
        return self._imagedata.getImageData()

