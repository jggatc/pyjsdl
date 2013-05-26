#Pyjsdl - Copyright (C) 2013 James Garnon

#from __future__ import division
from surface import Surface
import env

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
        pass

    def load(self, img_file, namehint=None):
        """
        Load image from file.
        Return the image as a Surface.
        """
        try:
            image = env.canvas.images[img_file]
        except KeyError:
            print "Failed to retrieve image file %s" % img_file
            return None
        img = image.getElement()
        surface = Surface((img.width,img.height))
        surface.drawImage(image, 0, 0)
        return surface

