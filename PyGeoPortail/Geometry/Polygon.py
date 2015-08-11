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
#                                              Audit
#
# - 12/03/2012 Fabrice
#   - is this algorithm true for concave/convex polygon ?
#
####################################################################################################

####################################################################################################

from PyGeoPortail.Tools.IterTools import closed_pairwise
from PyGeoPortail.Math.Functions import sign
from PyGeoPortail.Geometry.PointSet import interval_of_set_of_points

####################################################################################################

class Polygon(object):

    """ This class implements a Polygon.
    """

    ##############################################

    def __init__(self, *args):

        """ The parameter *args* is an iterable of :class:`PyGeoPortail.Geometry.Vector2D` that defines the
        vertexes.
        """

        array = self._check_arguments(args)
        
        self.vertexes = array[:]
        self.edges = [p1 - p0 for p0, p1 in closed_pairwise(self.vertexes)]

    ##############################################

    def _check_arguments(self, args):

        size = len(args)
        if size == 1:
            array = args[0]
        else:
            array = args

        return array

    ##############################################

    @staticmethod
    def cross_sign(vertex, edge, point):

        """ Compute the cross sign between the edge vector and (point - vertex) vector. """

        cross_sign = sign(edge.cross(point - vertex))
        if round(cross_sign, 7) == 0: # Point on edge
            return True
        else:
            return cross_sign < 0

    ##############################################

    def __contains__(self, point):

        """ Test if the point is inside the polygon. """

        # The point is inside the polygon if it is always on the same edge side.  Thus the cross
        # sign must not change.
        cross_sign = None
        for vertex, edge in zip(self.vertexes, self.edges):
            edge_cross_sign = self.__class__.cross_sign(vertex, edge, point)
            if cross_sign is None:
                cross_sign = edge_cross_sign
            elif edge_cross_sign != cross_sign:
                return False
        else:
            return True

    ##############################################

    def to_interval(self):

        """ Return the enclosing :class:`PyGeoPortail.Math.Interval.Interval2D` of the polygon. """

        return interval_of_set_of_points(self.vertexes)

####################################################################################################
#
# End
#
####################################################################################################
