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
#
# Logging
#

import PyGeoPortail.Logging.Logging as Logging

logger = Logging.setup_logging('pygeoportail')

####################################################################################################

from PyGeoPortail.TileMap.GeoPortail import (GeoPortailPyramid,
                                             GeoPortailWTMS,
                                             GeoPortailMapProvider,
                                             GeoPortailOthorPhotoProvider)

####################################################################################################

geoportail_pyramid = GeoPortailPyramid()

geoportail_wtms = GeoPortailWTMS(user='fabrice.salvaire@orange.fr',
                                 password='fA77Sal(!',
                                 api_key='qd58byg78dg3nloou4ksa0pz')
geoportail_map_provider = GeoPortailMapProvider(geoportail_wtms)

media_dpi = 100
media_resolution_mm = 25.4 / media_dpi # mm/px
number_of_pixels_per_m = 1000 / media_resolution_mm
# top25_resolution = 1 : 25 000
for level in geoportail_pyramid:
    print('Level[{}] {:.1f} m  {:.2f} m/px  scale: 1 cm : {:.1f} m / 00 cm'.format(
        level.level, level.tile_length_m, level.resolution,
        level.resolution * number_of_pixels_per_m / 100))

####################################################################################################
#
# End
#
####################################################################################################
