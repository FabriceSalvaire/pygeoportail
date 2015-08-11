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

from .Line2D import Line2D
from .PointSet import interval_of_set_of_points
from PyGeoPortail.Math.Functions import sign
from PyGeoPortail.Math.Interval import IntervalInt2D
from PyGeoPortail.Tools.IterTools import closed_pairwise

####################################################################################################

class OpenInterval(object):

    ##############################################

    def __init__(self, x, direction):

        self.x = x
        self.direction = direction

    ##############################################

    def __lt__(a, b):

        if a == b:
            return b.direction < a.direction
        else:
            return a.x < b.x

    ##############################################

    def __str__(self):

        if self.direction > 0:
            return '[{}'.format(self.x)
        else:
            return '{}]'.format(self.x)

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

    ##############################################

    @staticmethod
    def _to_grid(x, grid_step):
        return int(x // grid_step)

    ##############################################

    def intersec_with_grid(self, grid_step):

        interval = self.to_interval()
        interval_on_grid = IntervalInt2D((self._to_grid(interval.x.inf, grid_step),
                                          self._to_grid(interval.x.sup, grid_step)),
                                         (self._to_grid(interval.y.inf, grid_step),
                                          self._to_grid(interval.y.sup, grid_step)))
        print(interval, interval_on_grid)

        Y_min = interval_on_grid.y.inf
        rows = [[] for i in range(interval_on_grid.y.length())]
        for p0, p1 in closed_pairwise(self.vertexes):
            print('\nEdge', p0, p1)
            X0, Y0 = self._to_grid(p0.x, grid_step), self._to_grid(p0.y, grid_step)
            X1, Y1 = self._to_grid(p1.x, grid_step), self._to_grid(p1.y, grid_step)
            print('({}, {}) -> ({}, {})'.format(X0, Y0, X1, Y1))

            line = Line2D.from_two_points(p0, p1)

            if Y0 == Y1:
                pass
            elif Y1 > Y0:
                rows[Y0 - Y_min].append(OpenInterval(X0, 1))
                for Y in range(Y0 +1, Y1 +1):
                    y = Y * grid_step
                    x = line.get_x_from_y(y)
                    X = self._to_grid(x, grid_step)
                    YY = Y - Y_min
                    if X1 < X0:
                        YY -= 1
                    open_interval = OpenInterval(X, 1)
                    print(Y, x, y, X, YY, open_interval)
                    rows[YY].append(open_interval)
                rows[Y1 - Y_min].append(OpenInterval(X1, 1))
            elif Y1 < Y0:
                rows[Y1 - Y_min].append(OpenInterval(X1, -1))
                for Y in range(Y1 +1, Y0 +1):
                    y = Y * grid_step
                    x = line.get_x_from_y(y)
                    X = self._to_grid(x, grid_step)
                    YY = Y - Y_min
                    if X1 < X0:
                        YY -= 1
                    open_interval = OpenInterval(X, -1)
                    print(Y, x, y, X, YY, open_interval)
                    rows[YY].append(open_interval)
                rows[Y0 - Y_min].append(OpenInterval(X0, -1))

        h_lines = []
        for i, row in enumerate(rows):
            row.sort()
            Y = Y_min + i
            print('{}: {}'.format(Y, ' '.join([str(x) for x in row])))
            # Fixme: state machine ???
            # previous_open_interval = row[0]
            # simplified_row = [previous_open_interval]
            # for open_interval in row[1:]:
            #     if ((open_interval.x - previous_open_interval.x > 1)
            #         and (open_interval.direction != previous_open_interval.direction)):
            #         simplified_row.append(open_interval)
            #         previous_open_interval = open_interval
            # if simplified_row[-1].x != row[-1].x:
            #     simplified_row.append(row[-1])
            # print('    ' + ' '.join([str(x) for x in simplified_row]))
            h_lines.append((Y, row[0].x, row[-1].x))
        
        return h_lines

####################################################################################################
#
# End
#
####################################################################################################
