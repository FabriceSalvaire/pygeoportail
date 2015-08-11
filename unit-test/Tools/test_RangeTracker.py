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

import unittest

####################################################################################################

from PyGeoPortail.Tools.RangeTracker import *

####################################################################################################

class TestMinMaxFilter(unittest.TestCase):

    ##############################################

    def test(self):

        min_max_filter = MinMaxFilter()

        test_list = (353,453,1,6,4,92,4,618,31,42)

        for x in test_list:
            min_max_filter.filter(x)

        self.assertEqual(min_max_filter.min, min(test_list))
        self.assertEqual(min_max_filter.max, max(test_list))

####################################################################################################

class TestRangeAggregator(unittest.TestCase):

    ##############################################

    def test(self):

        interval_aggregator = IntervalAggregator()

        infs = (0, 10, -6, 100, -5000)
        offsets = (10, 100, 20, 1000, 10)
        sups = [inf + offset for inf, offset in zip(infs, offsets)]

        for inf, sup in zip(infs, sups):
            interval_aggregator.union(inf, sup)

        interval = interval_aggregator()
        self.assertEqual(interval.inf, min(infs))
        self.assertEqual(interval.sup, max(sups))

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
