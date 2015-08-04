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

import asyncio
import os

####################################################################################################

from PyGeoPortail.TileMap.GeoPortail import (GeoPortailPyramid,
                                             GeoPortailWTMS,
                                             GeoPortailMapProvider,
                                             GeoPortailOthorPhotoProvider)
from PyGeoPortail.TileMap.Projection import GeoAngle, GeoCoordinate
from PyGeoPortail.Math.Interval import Interval2D

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

longitude = GeoAngle(6, 7, 0)
latitude = GeoAngle(44, 41, 0)
location = GeoCoordinate(longitude, latitude)
x, y = geoportail_pyramid.coordinate_to_projection(location)
area = Interval2D((x, x), (y, y)).enlarge(20000) # 10 km
print('Area:', area)

loop = asyncio.get_event_loop()
cache_path = os.path.join(os.environ['HOME'], '.cache', 'pygeoportail')
if not os.path.exists(cache_path):
    os.mkdir(cache_path)

def done_callback(future):
    tile = future.result()
    tile.save(cache_path)

if False:
    level_max = 16
    for level in range(level_max +1):
        pyramid_level = geoportail_pyramid[level]
        mosaic_interval = pyramid_level.projection_interval_to_mosaic(area)
        print(level, mosaic_interval)
        for r in mosaic_interval.x.iter():
            tasks = [asyncio.async(geoportail_map_provider.get_tile(level, r, c))
                     for c in mosaic_interval.y.iter()]
            for task in tasks:
                task.add_done_callback(done_callback)
            loop.run_until_complete(asyncio.wait(tasks))

loop.close()

####################################################################################################
#
# End
#
####################################################################################################
