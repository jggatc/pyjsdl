#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
from surface import Surface, Surf
import env
import pyjsdl
import os.path

__docformat__ = 'restructuredtext'


class Image(object):
    """
    **pyjsdl.image**
    
    * pyjsdl.image.load
    * pyjsdl.image.get_image
    * pyjsdl.image.convert_image
    """

    def __init__(self):
        """
        Initialize Image module.
        
        Module initialization creates pyjsdl.image instance.
        """
        self.images = None

    def load(self, img_file, namehint=None):
        """
        Load image from file.
        Return the image as a Surface.
        """
        image = self.get_image(img_file)
        surface = self.convert_image(image)
        return surface

    def get_image(self, img_file):
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

    def convert_image(self, image):
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

