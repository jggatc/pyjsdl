#Pyjsdl - Copyright (C) 2013 James Garnon

#Not Implemented
#from __future__ import division
#from java.awt.image import BufferedImage
from surface import Surface

__docformat__ = 'restructuredtext'


class Surfarray(object):
    """
    **pyjsdl.surfarray**
    
    * pyjsdl.surfarray.blit_array
    """

    def __init__(self):
        """
        Provides image pixel manipulation method.

        Module initialization creates pyjsdl.surfarray instance.
        """
        self.initialized = False
        self._nonimplemented_methods()

    def _init(self):
        """
        Initialize surfarray module.
        """
        global Numeric
        try:
            import Numeric      #JNumeric
        except ImportError:
            raise ImportError, "JNumeric module is required."
        #JNumeric doesn't work on Jython2.2.1
        #JNumeric updated to work on Jython2.5.2:
        #https://bitbucket.org/zornslemon/jnumeric-ra/
        self.initialized = True

    def blit_array(self, surface, array):
        """
        Generates image pixels from a JNumeric array.
        Arguments include surface to generate the image, and array of integer colors.
        """
        if not self.initialized:
            self._init()
        w,h = array.shape
        data = Numeric.reshape(array, (1,w*h))[0]
        if not surface.getColorModel().hasAlpha():
            surface.setRGB(0, 0, surface.width, surface.height, data, 0, surface.width)
        else:
            surf = Surface((w,h), BufferedImage.TYPE_INT_RGB)
            surf.setRGB(0, 0, surface.width, surface.height, data, 0, surface.width)
            g2d = surface.createGraphics()
            g2d.drawImage(surf, 0, 0, None)
            g2d.dispose()
        return None

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.use_arraytype = lambda *arg: None

