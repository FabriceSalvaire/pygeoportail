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

from PyGeoPortail.Math.Interval import IntervalInt2D

####################################################################################################

class Pyramid(object):

    __area__ = None # longitude, latitude
    __projection__ = 'epsg:3857'
    __offset__ = None
    __root_resolution__ = None
    __number_of_levels__ = None
    __tile_size__ = 256 # px

    ##############################################

    def __init__(self):

        self._levels = [PyramidLevel(self, level) for level in range(self.__number_of_levels__)]

    ##############################################

    def __getitem__(self, level):

        return self._levels[level]

    ##############################################

    @property
    def area(self):
        return self.__area__

    ##############################################

    @property
    def projection(self):
        return self.__projection__

    ##############################################

    @property
    def offset(self):
        return self.__offset__

    ##############################################

    @property
    def root_resolution(self):
        return self.__root_resolution__

    ##############################################

    @property
    def tile_size(self):
        return self.__tile_size__

####################################################################################################

class PyramidLevel(object):

    ##############################################

    def __init__(self, pyramid, level):

        self._pyramid = pyramid
        self._level = level
        self._tile_size = pyramid.tile_size
        self._mosaic_size = 2**level
        self._resolution = pyramid.root_resolution / self.mosaic_size

    ##############################################

    @property
    def tile_size(self):
        return self._tile_size

    ##############################################

    @property
    def mosaic_size(self):
        return self._mosaic_size

    ##############################################

    @property
    def resolution(self):
        return self._resolution

    ##############################################

    @property
    def tile_length_m(self):
        return self._tile_size * self._resolution

    ##############################################

    def coordinate_to_projection(self, geo_coordinate):

        x0, y0 = self._pyramid.offset
        xm, ym = geo_coordinate.mercator
        x = xm - x0
        y = y0 - ym

        return (x, y)

    ##############################################

    def projection_to_mosaic(self, coordinate):

        x, y = coordinate
        column = int(x / self.tile_length_m)
        row = int(y / self.tile_length_m)
        if row < self._mosaic_size or column < self._mosaic_size:
            return row, column
        else:
            raise ValueError('Out of region')

    ##############################################

    def coordinate_to_mosaic(self, geo_coordinate):

        return self.projection_to_mosaic(self.coordinate_to_projection(geo_coordinate))

    ##############################################

    def coordinate_interval_to_projection(self, interval):

        longitude = interval.x
        latitude = interval.y
        x_inf, y_inf = self.coordinate_to_projection((longitude.inf, latitude.inf))
        x_sup, y_sup = self.coordinate_to_projection((longitude.sup, latitude.sup))

        return IntervalInt2D((x_inf, x_sup), (y_inf, y_sup))

    ##############################################

    def projection_interval_to_mosaic(self, interval):

        x = interval.x
        y = interval.y
        row_inf, col_inf = self.projection_to_mosaic((x.inf, y.inf))
        row_sup, col_sup = self.projection_to_mosaic((x.sup, y.sup))

        return IntervalInt2D((row_inf, row_sup), (col_inf, col_sup))

####################################################################################################
#
# End
#
####################################################################################################
