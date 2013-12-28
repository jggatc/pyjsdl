#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
from surface import Surface, Surf   ###0.18
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
        image = self.get_image(img_file)    ###0.18
        surface = self.convert_image(image)
        return surface

    def get_image(self, img_file):      ###0.18
        """
        Return the original image.
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
        return image

    def convert_image(self, image):      ###0.18
        """
        Return the image as a Surface.
        """
        if env.canvas._isCanvas:
            img = image.getElement()
            surface = Surface((img.width,img.height))
            surface.drawImage(image, 0, 0)
        else:
            surface = Surf(image)
        return surface

