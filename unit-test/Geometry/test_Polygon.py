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

from PyGeoPortail.Geometry.Polygon import *
from PyGeoPortail.Geometry.Vector2D import *

####################################################################################################

class TestPolygon(unittest.TestCase):

    ##############################################

    def test(self):

        # Square of diagonal 2*size and centered on the origin
        size = 10
        v0 = Vector2D(-size, -size)
        v1 = Vector2D(-size,  size)
        v2 = Vector2D( size,  size)
        v3 = Vector2D( size, -size)
        polygon = Polygon(v0, v1, v2, v3)

        # Point on the bounding
        p0 = Vector2D(0, size)
        self.assertTrue(p0 in polygon)

        # Point inside
        p0 = Vector2D(1,1)
        self.assertTrue(p0 in polygon)

        # Point outside
        p0 = Vector2D(20,20)
        self.assertFalse(p0 in polygon)

        # Rotated square included in a circle of radius size and centered on the origin
        size = 10
        v0 = Vector2D(    0, -size)
        v1 = Vector2D(-size,     0)
        v2 = Vector2D(    0,  size)
        v3 = Vector2D( size,     0)
        polygon = Polygon(v0, v1, v2, v3)

        # Point on the bounding
        p0 = Vector2D(0, -size)
        self.assertTrue(p0 in polygon)

        p0 = Vector2D.middle(v0, v1)
        self.assertTrue(p0 in polygon)

        # Point included
        p0 = Vector2D(1,1)
        self.assertTrue(p0 in polygon)

        # Point outside
        p0 = Vector2D(20,20)
        self.assertFalse(p0 in polygon)

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
