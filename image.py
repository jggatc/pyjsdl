#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
from surface import Surface
import env
import pyjsdl       ###0.16
import os.path      ###0.16

__docformat__ = 'restructuredtext'


class Image(object):
    """
    **pyjsdl.image**
    
    * pyjsdl.image.load
    """

    def __init__(self):
        """
        Initialize Image module.
        
        Module initialization creates pyjsdl.image instance.
        """
        self.images = None         ###0.16

    def load(self, img_file, namehint=None):    ###0.16
        """
        Load image from file.
        Return the image as a Surface.
        """
        if self.images is None:
            self.images = {}
            for img in env.canvas.images:
                self.images[os.path.normpath(img)] = env.canvas.images[img]
        img_file = os.path.normpath(img_file)
        try:
            image = self.images[img_file]
        except KeyError:
            raise pyjsdl.error("Failed to retrieve image file %s" % img_file)
        img = image.getElement()
        surface = Surface((img.width,img.height))
        surface.drawImage(image, 0, 0)
        return surface

