####################################################################################################
#
# PyGeoPortail - A IGN GeoPortail Map Viewer
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import logging

import numpy as np

####################################################################################################

from PyGeoPortail.ImageProcessing.Core.ImageFilter import ImageFilter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class NormalisedFloatFilter(ImageFilter):

    __filter_name__ = 'Float Filter'
    __input_names__ = ('input',)
    __output_names__ = ('float_image',)

    _logger = _module_logger.getChild('HlsFilter')

    ##############################################

    def generate_image_format(self, output):

        image_format = self.get_primary_input().image_format
        return image_format.clone(data_type=np.float32, normalised=True)

    ##############################################

    def generate_data(self):

        self._logger.info(self.name)
        
        input_ = self.get_primary_input()
        output = self.get_primary_output()
        input_.image.to_normalised_float(output.image)

####################################################################################################
#
# End
#
####################################################################################################
