####################################################################################################

from PyGeoPortail.TileMap.OffLineCache import MapLevel, Tile, Run, Region, OffLineCache
from PyGeoPortail.Math.Interval import IntervalInt

####################################################################################################

offline_cache = OffLineCache('offline-cache.sqlite3')

tile_provider = None

map_level = MapLevel(provider_id=1, map_id=1, version=1, level=1)

region = Region('region1',
                map_level,
                runs=(Run(1, IntervalInt(2, 3)),
                      Run(2, IntervalInt(2, 6)),
                ))
offline_cache.insert_region(region, tile_provider)

region = Region('region2',
                map_level,
                runs=(Run(1, IntervalInt(3, 3)),
                      Run(2, IntervalInt(5, 6)),
                      Run(3, IntervalInt(4, 6)),
                ))
offline_cache.insert_region(region, tile_provider)

offline_cache.delete_region(1)

# test on-line cache

# for column in range(5):
#     tile = Tile(map_level, row=1, column=column)
#     offline_cache.insert_tile(tile, offline=1)
# print(offline_cache.has_tile(tile))
# offline_cache.update_tile_offline_count(tile, 10)
# print(offline_cache.has_tile(tile))
# offline_cache.delete_region(1)
# offline_cache._delete('map_level')

####################################################################################################
#
# End
#
####################################################################################################
