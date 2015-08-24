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

import numpy as np

import PIL.Image as PIL_Image

try:
    import cv2
except:
    cv2 = None

try:
    import tifffile
except:
    tifffile = None
    
####################################################################################################

from .Image import ImageFormat, Image

####################################################################################################

def load_image(path):

    if cv2 is not None:
        cv_array = cv2.imread(path)
        # CV uses BGR format
        image = Image(cv_array, share=True, channels=ImageFormat.BGR)
        image = image.swap_channels(ImageFormat.RGB)
    else:
        array = np.array(PIL_Image.open(path))
        image = Image(array, channels=ImageFormat.RGB)

    # array = tifffile.imread(path)
    # image = Image(cv_array, share=True, channels=ImageFormat.RGB)

    return image

####################################################################################################
# 
# End
# 
####################################################################################################
