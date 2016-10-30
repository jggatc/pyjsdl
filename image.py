#Pyjsdl - Copyright (C) 2013 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

#from __future__ import division
import os
from pyjsdl.surface import Surface, Surf
from pyjsdl import env
import pyjsdl

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
        Retrieve image from preloaded images.
        The img_file argument is an image URL, or an image data object whereby namehint argument is used to retrieve the image.
        Return the image as a Surface.
        """
        if not namehint:
            image = self.get_image(img_file)
        else:
            image = self.get_image(namehint)
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
            surface = Surface((image.width,image.height))
            surface.drawImage(image, 0, 0)
        else:
            surface = Surf(image)
        return surface

