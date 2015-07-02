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

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Tile(object):

    __key_pattern__ = '{:x}/{:x}/{:x}/{:x}'

    ##############################################

    @staticmethod
    def tile_key(layer, level, row, column):

        return Tile.__key_pattern__.format(layer, level, row, column)

    ##############################################

    def __init__(self, layer, level, row, column, image):

        self._layer = layer
        self._level = level
        self._row = row
        self._column = column
        self._image = image

    ##############################################

    def key(self):

        return self.__key_pattern__.format(self._layer, self._level, self._row, self._column)

    ##############################################

    def size(self):

        # Fixme: AttributeError: type object 'Image' has no attribute 'image_format'
        # return self._image.image_format.number_of_bytes
        return 256*256*8*3

    ##############################################

    @property
    def image(self):

        return self._image

####################################################################################################

class CachedPyramid(object):

    __layer_id__ = 0

    _logger = _module_logger.getChild('CachedPyramid')

    ##############################################

    def __init__(self, data_provider, lru_cache):

        self._data_provider = data_provider
        self._lru_cache = lru_cache

        self._layer_id = self._new_layer_id()
        self._pyramid = self._data_provider.pyramid

    ##############################################

    @staticmethod
    def _new_layer_id():
        layer_id = CachedPyramid.__layer_id__
        CachedPyramid.__layer_id__ += 1
        return layer_id

    ##############################################

    def acquire(self, level, row, column):

        obj = self._lru_cache.acquire(Tile.tile_key(self._layer_id, level, row, column))
        if obj is not None:
            self._logger.info('Tile in cache')
            return obj
        else:
            self._logger.info('Add tile in cache')
            data = self._data_provider.get_tile(level, row, column)
            tile = Tile(self._layer_id, level, row, column, data)
            self._lru_cache.add(tile)
            return tile

    ##############################################

    def release(self, level, row, column):

        self._lru_cache.release(Tile.tile_key(self._layer_id, level, row, column))

    ##############################################

    def acquire_interval(self, level, interval):

        return [self.acquire(level, row, column)for row, column in interval.iter()]

####################################################################################################
#
# End
#
####################################################################################################
