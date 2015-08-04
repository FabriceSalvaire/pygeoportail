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

####################################################################################################

from PyGeoPortail.TileMap.GeoPortail import (GeoPortailPyramid,
                                             GeoPortailWTMS,
                                             GeoPortailMapProvider,
                                             GeoPortailOthorPhotoProvider)
from PyGeoPortail.TileMap.LruCache import LruCache
from PyGeoPortail.TileMap.Projection import GeoAngle, GeoCoordinate
from PyGeoPortail.TileMap.TileCache import CachedPyramid

####################################################################################################

geoportail_wtms = GeoPortailWTMS(user='fabrice.salvaire@orange.fr',
                                 password='fA77Sal(!',
                                 api_key='qd58byg78dg3nloou4ksa0pz')

geoportail_pyramid = GeoPortailPyramid()

level = 16
longitude = GeoAngle(6, 7, 0)
latitude = GeoAngle(44, 41, 0)
location = GeoCoordinate(longitude, latitude)
row, column = geoportail_pyramid[level].coordinate_to_mosaic(location)
print(level, row, column)

geoportail_map_provider = GeoPortailMapProvider(geoportail_wtms)
lru_cache = LruCache(constraint=1024**3)
cached_pyramid = CachedPyramid(geoportail_map_provider, lru_cache)

loop = asyncio.get_event_loop()

def done_callback(future):
    # logger.info
    print('done ' + str(future.result()))

tasks = [asyncio.async(cached_pyramid.acquire(level, row, column + i)) for i in range(50)]
for task in tasks:
    task.add_done_callback(done_callback)
loop.run_until_complete(asyncio.wait(tasks))

loop.close()

####################################################################################################
#
# End
#
####################################################################################################
