#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Image module**

The module provides function to load images and convert them to surface objects.
"""

import os
import base64
from pyjsdl.surface import Surface, Surf
from pyjsdl.pyjsobj import loadImages
from pyjsdl import constants as Const
from pyjsdl import env
import pyjsdl


class Image(object):
    """
    Image object.
    """

    def __init__(self):
        """
        Initialize Image module.

        Module initialization creates pyjsdl.image instance.
        """
        self.images = {}

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
        surface = Surface((image.width,image.height), Const.SRCALPHA)
        surface.drawImage(image, 0, 0)
        return surface

    def preload_images(self, images, callback_obj=None):
        """
        Preload images list.

        Images retrieved with image.load, until loaded the method throws a pyjsdl.error.
        Provide a callback_obj with _images_loaded method to be notified of preloading completion.
        """
        loader = ImageLoader(self, callback_obj)
        loader.load_images(images[:])

    def _register_images(self, images):
        for img in images:
            self.images[os.path.normpath(img)] = images[img]


class ImageLoader:

    def __init__(self, image_obj, callback_obj):
        self.image_obj = image_obj
        self.callback_obj = callback_obj
        self.images = {}
        self.image_list = []

    def load_images(self, images):
        image_list = []
        for image in images:
            if isinstance(image, str):
                image_list.append(image)
                self.image_list.append(image)
            else:
                name = image[0]
                if isinstance(image[1], str):
                    data = image[1]
                else:
                    data = base64.b64encode(image[1].getvalue())
                if not data.startswith('data:'):
                    ext = name.strip().split('.')[-1]
                    data = "data:%s;base64,%s" %(ext, data)
                    #data:[<mediatype>][;base64],<data>
                image_list.append(data)
                self.image_list.append(name)
        loadImages(image_list, self)

    def onImagesLoaded(self, images):
        for i, image in enumerate(self.image_list):
            self.images[image] = images[i].getElement()
        self.image_obj._register_images(self.images)
        if self.callback_obj:
            self.callback_obj._images_loaded()

