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

from PyGeoPortail.Image import ImageLoader
from PyGeoPortail.ImageProcessing.Core.ImageFilter import ImageFilter

####################################################################################################

class ImageLoaderFilter(ImageFilter):

    __filter_name__ = 'Image Loader Filter'
    __input_names__ = ()
    __output_names__ = ('image',)

    ##############################################

    def __init__(self, path):

        super(ImageLoaderFilter, self).__init__()

        output = self.get_primary_output()
        output.image = ImageLoader.load_image(path)
        output._image_format = output.image.image_format

####################################################################################################
#
# End
#
####################################################################################################
