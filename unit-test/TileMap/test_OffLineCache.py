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

import os
import shutil
import subprocess
import tempfile
import unittest

####################################################################################################

from PyGeoPortail.TileMap.OffLineCache import MapLevel, TileIndex, Run, Region, OffLineCache
from PyGeoPortail.Math.Interval import IntervalInt

####################################################################################################

class TestOffLineCache(unittest.TestCase):

    ##############################################

    def setUp(self):

        self.tmp_directory = tempfile.mkdtemp()
        print('Temporay directory {} created'.format(self.tmp_directory))

        self.sqlite_path = os.path.join(self.tmp_directory, 'offline-cache.sqlite3')
        self.offline_cache = OffLineCache(self.sqlite_path)

    ##############################################

    def tearDown(self):

        # subprocess.call(('sqlite3', self.sqlite_path, '.dump'))
        shutil.rmtree(self.tmp_directory)

    ##############################################

    @unittest.skip('')
    def test_map_level(self):

        offline_cache = self.offline_cache
        
        map_level1 = MapLevel(provider_id=1, map_id=1, version=1, level=1)
        map_level_id1 = offline_cache._get_map_level_id(map_level1)
        self.assertEqual(map_level_id1, 1)
        
        map_level2 = MapLevel(provider_id=2, map_id=2, version=2, level=2)
        map_level_id2 = offline_cache._get_map_level_id(map_level2)
        self.assertEqual(map_level_id2, 2)
        map_level_id1 = offline_cache._get_map_level_id(map_level1)
        self.assertEqual(map_level_id1, 1)
        
        offline_cache.load_map_levels()
        self.assertEqual(len(offline_cache._map_level_id_cache), 2)

        map_level3 = MapLevel(provider_id=3, map_id=3, version=3, level=3)
        map_level_id3 = offline_cache._get_map_level_id(map_level3)
        self.offline_cache.delete_map_level(map_level1)
        offline_cache.commit()
        offline_cache.load_map_levels()
        self.assertListEqual(list(offline_cache._map_level_id_cache.keys()), [2, 3])
        
        # vacuum_map_level

        # offline_cache._query().exec_('DELETE * from map_level')
        # offline_cache.commit()

    ##############################################

    @unittest.skip('')
    def test_tile(self):

        offline_cache = self.offline_cache
        
        map_level1 = MapLevel(provider_id=1, map_id=1, version=1, level=1)
        tile1 = TileIndex(map_level1, row=1, column=1)
        offline_cache.insert_tile(tile1, offline=1) # Fixme: bool
        offline_cache.commit()
        # Fixme:
        print(offline_cache.get_tile(tile1))
        # Fixme: has_tile return 0
        self.assertEqual(offline_cache.has_tile(tile1), 1)
        offline_cache.update_tile_offline_count(tile1, 2)
        offline_cache.commit()
        self.assertEqual(offline_cache.has_tile(tile1), 2)
        offline_cache.delete_tile(tile1)
        offline_cache.commit()
        self.assertEqual(offline_cache.has_tile(tile1), 1)
        offline_cache.delete_tile(tile1)
        offline_cache.commit()
        self.assertEqual(offline_cache.has_tile(tile1), 0)

        # with self.assertRaises():
        # print(offline_cache.get_tile(tile1))

        # offline_cache._query().exec_('DELETE * from map_level')
        # offline_cache._query().exec_('DELETE * from tile')
        # offline_cache.commit()

    ##############################################

    # @unittest.skip('')
    def test_region(self):

        offline_cache = self.offline_cache

        tile_provider = None

        map_level = MapLevel(provider_id=1, map_id=1, version=1, level=1)

        column_interval1 = IntervalInt(1, 3)
        column_interval2 = IntervalInt(3, 6)
        
        region1 = Region('region1',
                         map_level,
                         runs=(Run(1, column_interval1),
                               Run(2, column_interval1),
                               Run(3, column_interval1),
                         ))
        offline_cache.insert_region(region1, tile_provider)
        # offline_cache.commit()
        
        region2 = Region('region2',
                         map_level,
                         runs=(Run(1, column_interval2),
                               Run(2, column_interval2),
                               Run(3, column_interval2),
                         ))
        offline_cache.insert_region(region2, tile_provider)
        offline_cache.commit()
        
        for row in range(1, 3 +1):
            for i in column_interval1.iter()[:-1]:
                self.assertEqual(offline_cache.has_tile(TileIndex(map_level, row, column=i)), 1)
            self.assertEqual(offline_cache.has_tile(TileIndex(map_level, row, column=3)), 2)
            for i in column_interval2.iter()[1:]:
                self.assertEqual(offline_cache.has_tile(TileIndex(map_level, row, column=i)), 1)
        
        offline_cache.delete_region('region1')
        offline_cache.commit()
        for row in range(1, 3 +1):
            for i in column_interval1.iter()[:-1]:
                self.assertEqual(offline_cache.has_tile(TileIndex(map_level, row, column=i)), 0)
            for i in column_interval2.iter():
                self.assertEqual(offline_cache.has_tile(TileIndex(map_level, row, column=i)), 1)
        
        region = offline_cache.get_region('region2')
        self.assertEqual(len(region.runs), 3)
        self.assertEqual(region.number_of_tiles, 3*column_interval2.length())
        
        print(offline_cache.tile_count_for_provider_id(1))

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
