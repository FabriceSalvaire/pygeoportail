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

from PyGeoPortail.Math.Interval import Interval2D
from PyGeoPortail.Tools.RangeTracker import MinMaxFilter

####################################################################################################

def interval_of_set_of_points(points):

    """ Return the enclosing :class:`PyGeoPortail.Math.Interval.Interval2D` of a set of points. The
    argument *points* must be an iterable and the point instance must have the :attr:`x` and
    :attr:`y` (cf. :class:`PyGeoPortail.Geometry.Vector2D`).
    """

    x = MinMaxFilter()
    y = MinMaxFilter()
    for point in points:
        x.filter(point.x)
        y.filter(point.y)

    return Interval2D((x.min, x.max), (y.min, y.max))

####################################################################################################
#
# End
#
####################################################################################################
