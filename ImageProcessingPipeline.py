####################################################################################################
#
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
#
####################################################################################################

####################################################################################################

import logging
from importlib import reload

import numpy as np

####################################################################################################

from PyGeoPortail.Image.Image import ImageFormat
from PyGeoPortail.ImageProcessing.Core.ImageFilter import ImageFilter
from PyGeoPortail.ImageProcessing.Filtering.Colour import HlsFilter
from PyGeoPortail.ImageProcessing.Filtering.DataTypeConverter import NormalisedFloatFilter
from PyGeoPortail.ImageProcessing.Filtering.IO.ImageLoader import ImageLoaderFilter

from . import UserFilterFunctions

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class UserFilter(ImageFilter):

    __filter_name__ = 'User Filter'
    __input_names__ = ('input',)
    __output_names__ = ('user_image',)

    _logger = _module_logger.getChild('UserFilter')

    ##############################################

    def generate_image_format(self, output):

        image_format = self.get_primary_input().image_format
        # return image_format.clone(height=image_format.height, width=image_format.width,
        #                           number_of_channels=1,
        #                           data_type=np.uint8,
        #                           channels=ImageFormat.Label)
        return image_format.clone(height=image_format.height, width=image_format.width,
                                  number_of_channels=3,
                                  data_type=np.uint8,
                                  channels=ImageFormat.RGB)

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)
        
        input_ = self.get_primary_input()
        output = self.get_primary_output()
        
        reload(UserFilterFunctions)
        UserFilterFunctions.user_filter(input_.image, output.image)

        # uuid
        # cv2.imwrite(self.name + '.tiff', output.image)

####################################################################################################

class ImageProcessingPipeline(object):

    ##############################################

    def __init__(self, image_path):

        self.input_filter = ImageLoaderFilter(image_path)
        self.float_filter = NormalisedFloatFilter()
        self.hls_filter = HlsFilter()
        self.user_filter = UserFilter()
        
        self.float_filter.connect_input('input', self.input_filter.get_primary_output())
        self.hls_filter.connect_input('input', self.float_filter.get_primary_output())
        self.hls_filter.update()
        # self.user_filter.connect_input('input', self.hls_filter.get_primary_output())
        # self.user_filter.update()

####################################################################################################
# 
# End
# 
####################################################################################################
