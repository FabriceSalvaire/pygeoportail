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

import logging
import math

import numpy as np

####################################################################################################

from .GraphicScene2 import GraphicItem
from PyGeoPortail.Math.Interval import IntervalInt2D, Interval2D

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def segment_intersection(point0, vector10, point2, point3):

    """ Return the intersection between two segments. """

    # p + t*r = q + u*s    x s
    #   t * (r x s) = (q - p) x s
    #   t = (q − p) × s / (r × s)
    # p + t*r = q + u*s    x r
    #   u = (q − p) × r / (r × s)

    vector32 = point3 - point2
    denominator = np.cross(vector10, vector32)
    if denominator == 0: # parallel
        # if np.cross(vector20, vector10) == 0:
        # check if overlapping
        #  0 ≤ (q − p) · r ≤ r · r or 0 ≤ (p − q) · s ≤ s · s
        return None
    else:
        vector20 = point2 - point0
        t = np.cross(vector20, vector32) / denominator
        u = np.cross(vector20, vector10) / denominator
        if 0 <= t <= 1 and 0 <= u <= 1:
            return point0 + vector10 * t
        else:
            return None

####################################################################################################

class PathGraphicItem(GraphicItem):

    __path_id__ = 0

    ##############################################

    def __init__(self, colour, pencil_size):

        super(PathGraphicItem, self).__init__()
        self._colour = colour
        self._pencil_size = pencil_size

    ##############################################

    def __repr__(self):
        return "Path {}".format(self._id)

    ##############################################

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, colour):
        self._colour = colour

    @property
    def pencil_size(self):
        return self._pencil_size

    @pencil_size.setter
    def pencil_size(self, pencil_size):
        self._pencil_size = pencil_size

####################################################################################################

class Path(PathGraphicItem):

    _logger = _module_logger.getChild('Path')

    ##############################################

    def __init__(self, colour, pencil_size, points):

        super(Path, self).__init__(colour, pencil_size)
        
        if points.shape[1] <= 1:
            raise ValueError("Require at least two points")
        
        self._points = points # Fixme: share ?
        self._interval = self._compute_interval()
        self._number_of_points = self._points.shape[0]

    ##############################################

    def subpath(self, lower=0, upper=None):

        if upper is None:
            stop = None
        else:
            stop = upper + 1
        points = self._points[lower:stop]
        
        if points.shape[1] > 1:
            return self.__class__(self._colour, self._pencil_size, points)
        else:
            # raise
            return None

    ##############################################

    @property
    def points(self):
        return self._points

    @property
    def number_of_points(self):
        return self._number_of_points

    @property
    def indexes(self):
        return np.arange(self._number_of_points)

    @property
    def x(self):
        return self._points[:,0]

    @property
    def y(self):
        return self._points[:,1]

    @property
    def p0(self):
        return self._points[0]

    @property
    def p1(self):
        return self._points[-1]

    @property
    def p10(self):
        return self.p1 - self.p0

    @property
    def p10_norm(self):
        p10 = self.p10
        return np.sqrt(p10[0]**2 + p10[1]**2) # srqt(x.x) # np.sum(p10**2, axis=1)

    @property
    def u10(self):
        p10 = self.p10
        u10 = p10 / self.p10_norm # Fixme: recompute p10
        return u10

    @property
    def barycenter(self):
        return np.mean(self._points, axis=0)

    ##############################################

    def _compute_interval(self):

        x = self.x
        lower_x = np.min(x)
        upper_x = np.max(x)
        y = self.y
        lower_y = np.min(y)
        upper_y = np.max(y)
        return Interval2D((lower_x, upper_x), (lower_y, upper_y))

    ##############################################

    def translate(self, vector):

        self._points += vector

    ##############################################

    def scale(self, vector):

        self._points *= vector

    ##############################################

    def rotate(self, angle):

        t = math.radians(angle)
        c = math.cos(t)
        s = math.sin(t)
        x = self.x
        y = self.y
        x = c*x - s*y
        y = s*x + c*y

    ##############################################

    def transform(self, matrix):

        # Fixme: Faster implementation?

        # pi_0 = m_00 * pi_0 + m_01 * pi_1 + m_02
        # pi_1 = m_10 * pi_0 + m_11 * pi_1 + m_12
        x = self.x
        y = self.y
        x *= matrix[0, 0]
        x += matrix[0, 1] * y
        x += matrix[0, 2]
        y *= matrix[1, 0]
        y += matrix[1, 1] * y
        y += matrix[2, 2]

    ##############################################

    def pair_iterator(self):

        for i in range(self._number_of_points -1):
            yield self._points[i], self._points[i+1]

    ##############################################

    def find_self_intersection(self):

        intersections = []
        for i, points01 in enumerate(self.pair_iterator()):
            for j, points23 in enumerate(self.pair_iterator()):
                if i != j and j > i + 1:
                    point0, point1 = points01
                    point2, point3 = points23
                    vector10 = point1 - point0
                    intersection = segment_intersection(point0, vector10, point2, point3)
                    if intersection is not None:
                        # print(i, j, intersection)
                        intersections.append((i, j, intersection))
        return intersections

    ##############################################

    def _farthest_point(self, slice_=None, tolerance=1):

        """ Return the farthest point to the chord P0 - P1. """

        # distance to chord
        # A x B = sin * |A| * |B|
        # A x u = sin * |A|
        # sin = d / |A|
        # d = (P - P0) x u
        delta = self._points[slice_] - self.p0
        distance = np.abs(np.cross(delta, self.u10))
        i_max = np.argmax(distance)
        distance_max = distance[i_max]
        if distance_max > tolerance:
            if slice_ is not None:
                i_max += slice_.start
            return i_max
        else:
            return None

    ##############################################

    def simplify(self, tolerance=1):

        # Fixme: check interval

        queue = [None]
        farthest_points = [0] # First point index
        while queue:
            slice_ = queue.pop()
            farthest_point = self._farthest_point(slice_, tolerance)
            if farthest_point is not None:
                farthest_points.append(farthest_point)
                queue.append(slice(slice_.start, farthest_point))
                queue.append(slice(farthest_point, slice_.stop))
        farthest_points.append(self._number_of_points -1) # last point index
        farthest_points.sort() # due to algorithm
        points = self._points[farthest_points]
        
        return self.__class__(self._colour, self._pencil_size, points)

    ##############################################

    def smooth_window(self, radius=2):

        window_size = 2*radius + 1
        if window_size >= self._number_of_points:
            raise ValueError()

        if radius > 0:
            points = np.array(self._points, dtype=np.float)
            view = points[radius:-radius]
            for i in range(1, radius +1):
                upper = -radius + i
                if upper == 0:
                    upper = None
                view += self._points[radius-i:-radius-i]
                view += self._points[radius+i:upper]
            view /= window_size
            # for i in range(1, radius +1):
            #     points[:radius] += self._points[i:radius+i]
            #     points[-radius:] += self._points[-radius-i:-i]
            # points[:radius] /= radius + 1
            # points[-radius:] /= radius + 1
            # points[radius-1] = np.mean(self._points[:radius], axis=0)
            # points[-radius] = np.mean(self._points[-radius:], axis=0)
            # return self.__class__(points[radius-1:-radius+1])
            return self.__class__(self._colour, self._pencil_size, view)
        elif radius < 0:
            raise ValueError()
        else:
            return self

    ##############################################

    def backward_smooth_window(self, radius=2):

        # limite the rate of points: average last N points

        window_size = radius + 1
        if window_size >= self._number_of_points:
            raise ValueError()
        
        if radius > 0:
            points = np.array(self._points, dtype=np.float)
            view = points[radius:]
            for i in range(1, radius +1):
                view += self._points[radius-i:-i]
            view /= window_size
            return self.__class__(self._colour, self._pencil_size, view)
        elif radius < 0:
            raise ValueError()
        else:
            return self

    ##############################################

    def nearest_point(self, point):

        """ Return the nearest point and the distance to the given point. """

        p0 = self._points[:-1]
        p1 = self._points[1:]
        p10 = p1 - p0
        u10 = p10 / np.sqrt(np.sum(p10**2, axis=0))
        
        delta = point - p0
        # projection = np.dot(delta, u10)
        projection = delta[:,0]*u10[:,0] + delta[:,1]*u10[:,1]
        # Fixme: [0, 1] ok?
        indexes = np.where(np.logical_and(0 <= projection, projection < 1))[0]
        # print(indexes)
        if indexes.shape[0]:
            distance = np.abs(np.cross(delta[indexes], u10[indexes]))
            i_min = np.argmin(distance)
            # print(indexes, projection[indexes], distance)
            # print(i_min, indexes[i_min], distance[i_min])
            return indexes[i_min], distance[i_min]
        else:
            return None, None

        # distance = np.sum((self._points - point)**2, axis=1)
        # i_min = np.argmin(distance)
        # return i_min, distance[i_min]

    ##############################################

    def distance(self, point):

        return self.nearest_point(point)[0]

    ##############################################

    def erase(self, point, radius):

        # Fixme: should erase segments
        #  - compute distances to point and get points within the eraser area |Pi - P| <= r
        #  - erase segments corresponding to these points
        #  - cut the previous and next segment

        point_index, distance = self.nearest_point(point)
        # print(distance)
        # Fixme: check distance, path removed (only a point)
        if point_index is not None and distance <= radius:
            if point_index == 0:
                return (self.subpath(lower=1),)
            elif point_index == self._number_of_points -1:
                return (self.subpath(upper=point_index -1),)
            else:
                # Fixme: check before
                return [subpath for subpath in (self.subpath(upper=point_index-1),
                                                self.subpath(lower=point_index+1))
                        if subpath is not None]
        else:
            return self

####################################################################################################

class Segment(Path):

    # _logger = _module_logger.getChild('Segment')

    ##############################################

    def __init__(self, colour, pencil_size, first_point=None, second_point=None, points=None):

        # Fixme: make_array
        points_ = np.zeros((2, 2), dtype=np.float)
        if points is None:
            points_[0] = first_point
            if second_point is not None:
                points_[1] = second_point
        else:
            points_[...] = points
        
        super(Segment, self).__init__(colour, pencil_size, points_)

    ##############################################

    def __repr__(self):
        return "Segment {}".format(self._id)

    ##############################################

    def update_second_point(self, point):

        self._points[1] = point
        self._compute_interval()

    ##############################################

    def distance(self, point):

        u10 = self.u10
        delta = point - self.p0
        projection = np.dot(delta, u10)
        distance = np.abs(np.cross(delta, u10))
        return projection, distance

    ##############################################

    def point_at_abscissa(self, t):
        return (1 - t)*self.p0 + t * self.p1

    ##############################################

    def erase(self, point, radius):

        # self._logger.info(str(self))
        projection, distance = self.distance(point)
        if distance <= radius:
            # compute line - circle intersection
            r = math.sqrt(radius**2 - distance**2)
            lower_projection = (projection - r) / self.p10_norm # Fixme: recompute
            upper_projection = (projection + r) / self.p10_norm
            if lower_projection <= 0 and upper_projection >= 1:
                return None # segment is deleted
            elif lower_projection > 0 and upper_projection < 1:
                # middle is deleted
                return (Segment(self._colour, self._pencil_size,
                                self.p0, self.point_at_abscissa(lower_projection)),
                        Segment(self._colour, self._pencil_size,
                                self.point_at_abscissa(upper_projection), self.p1))
            elif lower_projection <= 0 and upper_projection >= 0:
                # head is deleted
                return (Segment(self._colour, self._pencil_size,
                                self.point_at_abscissa(upper_projection), self.p1),)
            elif lower_projection <= 1 and upper_projection >= 1:
                # tail is deleted
                return (Segment(self._colour, self._pencil_size,
                                self.p0, self.point_at_abscissa(lower_projection)),)
        return self

####################################################################################################

class DynamicPath(PathGraphicItem):

    ##############################################

    def __init__(self, colour, pencil_size, array_size=500):

        super(DynamicPath, self).__init__(colour, pencil_size)
        
        self._arrays = []
        self._array_size = array_size
        self._number_of_points = 0
        self._capacity = 0
        self._index = 0

    ##############################################

    def _make_array(self, size):

        return np.zeros((size, 2), dtype=np.float)

    ##############################################

    def _extend(self):

        self._arrays.append(self._make_array(self._array_size))
        self._capacity += self._array_size
        self._index = 0

    ##############################################

    def flatten(self):

        points = self._make_array(self._number_of_points)
        lower_index = 0
        for array in self._arrays[:-1]:
            array_size = array.shape[0]
            upper_index = lower_index + array_size
            points[lower_index:upper_index] = array
            lower_index = upper_index
        last_array = self._arrays[-1]
        points[lower_index:self._number_of_points] = last_array[:self._number_of_points-lower_index]
        return points

    ##############################################

    def add_point(self, point):

        self._number_of_points += 1
        if self._number_of_points > self._capacity:
            self._extend()
        current_array = self._arrays[-1]
        current_array[self._index] = point
        self._index += 1

        point_interval = IntervalInt2D([point[0], point[0]], [point[1], point[1]])
        if self._interval is None:
            self._interval = point_interval
        else:
            self._interval |= point_interval

    ##############################################

    def to_path(self):

        # Fixme: will recompute interval
        return Path(self._colour, self._pencil_size, self.flatten())

####################################################################################################
#
# End
#
####################################################################################################
