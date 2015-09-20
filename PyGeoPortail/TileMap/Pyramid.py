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

import math

####################################################################################################

from PyGeoPortail.Math.Functions import rint
from PyGeoPortail.Math.Interval import IntervalInt2D
from .Projection import GeoCoordinate

_mercator_half_perimeter = math.pi * GeoCoordinate.equatorial_radius
_mercator_perimeter = 2 * _mercator_half_perimeter

####################################################################################################

class Pyramid(object):

    __area__ = None # longitude, latitude
    __projection__ = 'epsg:3857'
    __offset__ = (-_mercator_half_perimeter, _mercator_half_perimeter) # m
    __number_of_levels__ = None
    __tile_size__ = 256 # px

    ##############################################

    def __init__(self):

        # root_resolution = 156543.033928041 m / px
        self._root_resolution = _mercator_perimeter / self.__tile_size__

        self._levels = [PyramidLevel(self, level) for level in range(self.__number_of_levels__)]

    ##############################################

    def __iter__(self):

        return iter(self._levels)

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
        return self._root_resolution

    ##############################################

    @property
    def tile_size(self):
        return self.__tile_size__

    ##############################################

    def level_resolution(self, level):

        return self._root_resolution / 2**level

    ##############################################

    def smallest_resolution(self):

        return self.level_resolution(self.__number_of_levels__ -1)

    ##############################################

    def closest_level(self, resolution):

        return rint(math.log(self._root_resolution / resolution) / math.log(2))

    ##############################################

    def coordinate_to_projection(self, geo_coordinate):

        # Fixme: to numpy ?
        x0, y0 = self.__offset__
        xm, ym = geo_coordinate.mercator
        x = xm - x0
        y = y0 - ym
        
        return (x, y)

    ##############################################

    def coordinate_to_projection_normalised(self, geo_coordinate):

        x = float(geo_coordinate.longitude) / 360 + .5
        y = .5*(math.log(math.tan(math.radians(float(geo_coordinate.latitude))/2 + math.pi/4)) / math.pi - 1)
        # (x, y) * 2**level = (col, row))
        
        return (x, y)

####################################################################################################

class PyramidLevel(object):

    ##############################################

    def __init__(self, pyramid, level):

        self._pyramid = pyramid
        self._level = level
        self._tile_size = pyramid.tile_size
        self._mosaic_size = 2**level # Fixme: name ?
        self._resolution = pyramid.level_resolution(level)
        # self._resolution = pyramid.root_resolution / self.mosaic_size

    ##############################################

    @property
    def level(self):
        return self._level

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

    def projection_to_mosaic(self, coordinate):

        x, y = coordinate
        column = int(x / self.tile_length_m)
        row = int(y / self.tile_length_m)
        if row < self._mosaic_size or column < self._mosaic_size:
            return row, column
        else:
            raise ValueError('Out of region')

    ##############################################

    def coordinate_to_projection(self, geo_coordinate):

        x, y = self._pyramid.coordinate_to_projection(geo_coordinate)
        
        return (x, y)

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
