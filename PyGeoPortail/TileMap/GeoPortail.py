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

from io import BytesIO
from urllib.parse import urlencode, quote
import asyncio
import json
import logging
import os

import requests
from yieldfrom import requests as async_requests

import numpy as np

from PIL import Image as PilImage

####################################################################################################

from .Pyramid import Pyramid
from PyGeoPortail.Image.Image import ImageFormat, Image
import PyGeoPortail.Config.Config as Config

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GeoPortailPyramid(Pyramid):

    __area__ = None # longitude, latitude
    __number_of_levels__ = 22
    __tile_size__ = 256 # px

####################################################################################################

class GeoPortailTile(object):

    ##############################################

    def __init__(self, layer, level, row, column, image=None):

        self._layer = layer
        self._level = level
        self._row = row
        self._column = column
        self._image = image

    ##############################################

    @property
    def layer(self):
        return self._layer

    @property
    def level(self):
        return self._level

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image

    ##############################################

    def filename(self, with_layer=False, with_level=False, extension='.jpg'):

        filename= str(self._row) + '-' + str(self._column) + extension
        if with_level:
            filename = str(self._level) + '-' + filename
        if with_layer:
            filename = self._layer + '-' + filename
        
        return filename

    ##############################################

    def save(self, path=Config.DiskCache.path):

        filename = os.path.join(path, self.filename(with_layer=True, with_level=True))
        PilImage.fromarray(self._image).save(filename)

    ##############################################

    def on_cache(self, path=Config.DiskCache.path):

        filename = os.path.join(path, self.filename(with_layer=True, with_level=True))
        return os.path.exists(filename)

    ##############################################

    def load(self, path=Config.DiskCache.path):

        filename = os.path.join(path, self.filename(with_layer=True, with_level=True))
        array = np.array(PilImage.open(filename))
        self._image = Image(array, channels=ImageFormat.RGB)

####################################################################################################

class GeoPortailWTMSLicence(object):

    ##############################################

    @staticmethod
    def load_from_json(json_path, name='default'):

        with open(json_path, 'r') as f:
            kwargs = json.load(f)
        return GeoPortailWTMSLicence(**kwargs[name])

    ##############################################

    def __init__(self, user, password, api_key, offline_cache_limit=1000):

        self.user = user
        self.password = password
        self.api_key = api_key
        self.offline_cache_limit = offline_cache_limit

####################################################################################################

class GeoPortailWTMS(object):

    _logger = _module_logger.getChild('GeoPortailWTMS')

    __protocol__ = 'https'
    __server__ = 'wxs.ign.fr'

    ##############################################

    def __init__(self, licence, timeout=30):

        self._licence = licence
        self._timeout = timeout

    ##############################################

    def make_url(self, *args, **kwargs):

        # urlencode: '&'.join()
        #
        # '&'.join(['{}={}'.format(key.upper(), quote(value))
        #           for key, value in kwargs.items()])

        return '{}://{}/{}/{}?{}'.format(self.__protocol__, self.__server__,
                                         self._licence.api_key,
                                         '/'.join(args),
                                         urlencode(kwargs))

    ##############################################

    def get(self, *args, **kwargs):

        url = self.make_url(*args, **kwargs)
        self._logger.info('GET ' + url)
        request = requests.get(url, auth=(self._licence.user, self._licence.password), timeout=self._timeout)
        content = request.text
        
        return content, url

    ##############################################

    @asyncio.coroutine
    def async_get(self, *args, **kwargs):

        url = self.make_url(*args, **kwargs)
        self._logger.info('GET ' + url)
        request = yield from async_requests.get(url, auth=(self._licence.user, self._licence.password), timeout=self._timeout)
        request.raise_for_status()
        content = yield from request.content
        
        return content, url

    ##############################################

    def autoconf(self, *keys):

        return self.get('autoconf', keys=','.join(keys))

    @asyncio.coroutine
    ##############################################

    def async_autoconf(self, *keys):

        # Timeout !
        return self.async_get('autoconf', keys=','.join(keys))

    ##############################################

    @staticmethod
    def to_image(data):

        # Fixme: directly save using f.write()
        array = np.array(PilImage.open(BytesIO(data)))
        image = Image(array, channels=ImageFormat.RGB)
        
        return image

    ##############################################

    @asyncio.coroutine
    def _download_layer(self, layer, level, row, column):

        tile = GeoPortailTile(layer, level, row, column)
        if tile.on_cache():
            self._logger.info('Tile on cache ' + tile.filename())
            tile.load()
        else:
            # Fixme: offline
            # ConnectTimeoutError()
            # ReadTimeout()
            content, url = yield from self.async_get('geoportail', 'wmts',
                                                     SERVICE='WMTS',
                                                     VERSION='1.0.0',
                                                     REQUEST='GetTile',
                                                     LAYER=layer,
                                                     STYLE='normal',
                                                     FORMAT='image/jpeg',
                                                     TILEMATRIXSET='PM',
                                                     TILEMATRIX=level,
                                                     TILEROW=row,
                                                     TILECOL=column,
            )
            self._logger.info('Completed GET ' + url)
            tile.image = self.to_image(content)
        
        return tile

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
        return tile

####################################################################################################

class GeoPortailMapProvider(GeoPortailProvider):

    ##############################################

    @asyncio.coroutine
    def get_tile(self, level, row, column):

        tile = yield from self._wtms.download_map(level, row, column)
        return tile

####################################################################################################
#
# End
#
####################################################################################################
