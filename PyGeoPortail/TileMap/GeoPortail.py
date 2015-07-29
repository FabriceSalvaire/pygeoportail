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

import asyncio
import logging

# import requests
from yieldfrom import requests

import numpy as np

####################################################################################################

from .Pyramid import Pyramid
from PyGeoPortail.Image.Image import ImageFormat, Image

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GeoPortailPyramid(Pyramid):

    __area__ = None # longitude, latitude
    __projection__ = 'epsg:3857'
    __offset__ = (-20037508, 20037508)
    __root_resolution__ = 156543.033928041
    __number_of_levels__ = 22
    __tile_size__ = 256 # px

####################################################################################################

class GeoPortailTile(object):

    ##############################################

    def __init__(self, layer, level, row, column, data):

        self._layer = layer
        self._level = level
        self._row = row
        self._column = column
        self._data = data

    ##############################################

    def to_bytes_io(self):

        from io import BytesIO
        
        return BytesIO(self._data)

    ##############################################

    def to_pil_image(self):

        from PIL import Image
        
        return Image.open(self.to_bytes_io())

    ##############################################

    def to_image(self):

        array = np.array(self.to_pil_image())
        image = Image(array, channels=ImageFormat.RGB)
        
        return image

    ##############################################

    def filename(self, with_layer=False, with_level=False, extension='.jpg'):

        filename= str(self._row) + '-' + str(self._column) + extension
        if with_level:
            filename = str(self._level) + '-' + filename
        if with_layer:
            filename = self._layer + '-' + filename
        
        return filename

####################################################################################################

class GeoPortailWTMS(object):

    _logger = _module_logger.getChild('GeoPortailWTMS')

    __url_template__ = 'http://wxs.ign.fr/{}/geoportail/wmts?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&LAYER={}&STYLE=normal&FORMAT={}&TILEMATRIXSET=PM&TILEMATRIX={}&TILEROW={}&TILECOL={}&'

    ##############################################

    def __init__(self, user, password, api_key):

        self._user = user
        self._password = password
        self._api_key = api_key

    ##############################################

    @asyncio.coroutine
    def _download_layer(self, layer, level, row, column):

        image_format = 'image/jpeg'
        url = self.__url_template__.format(self._api_key, layer, image_format, level, row, column)
        self._logger.info('GET ' + url)
        
        request = yield from requests.get(url, auth=(self._user, self._password))
        request.raise_for_status()
        content = yield from request.content
        
        return GeoPortailTile(layer, level, row, column, content)

    ##############################################

    @asyncio.coroutine
    def download_map(self, *args, **kwargs):

        tile = yield from self._download_layer('GEOGRAPHICALGRIDSYSTEMS.MAPS', *args, **kwargs)
        return tile

    ##############################################

    @asyncio.coroutine
    def download_ortho_photo(self, *args, **kwargs):

        tile = yield from self._download_layer('ORTHOIMAGERY.ORTHOPHOTOS', *args, **kwargs)
        return tile

####################################################################################################

class GeoPortailProvider(object):

    ##############################################

    def __init__(self, geoportail_wtms):

        self._wtms = geoportail_wtms
        self._pyramid = GeoPortailPyramid()

    ##############################################

    @property
    def pyramid(self):
        return self._pyramid

####################################################################################################

class GeoPortailOthorPhotoProvider(GeoPortailProvider):

    ##############################################

    @asyncio.coroutine
    def get_tile(self, level, row, column):

        tile = yield from self._wtms.download_ortho_photo(level, row, column)
        return tile.to_image()

####################################################################################################

class GeoPortailMapProvider(GeoPortailProvider):

    ##############################################

    @asyncio.coroutine
    def get_tile(self, level, row, column):

        tile = yield from self._wtms.download_map(level, row, column)
        return tile.to_image()

####################################################################################################
#
# End
#
####################################################################################################
