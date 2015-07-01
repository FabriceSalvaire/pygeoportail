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

# Note: we use functions (e.g. sin) from math module because they are faster

####################################################################################################

import math
import numpy as np

####################################################################################################

def identity():
    return np.identity(3, dtype=np.float32)

####################################################################################################

def translate(matrix, x, y):

    """ in-place translation """

    T = np.array([[1, 0, x],
                  [0, 1, y],
                  [0, 0, 1]],
                 dtype=matrix.dtype)

    matrix[...] = np.dot(T, matrix)
    return matrix

####################################################################################################

def scale(matrix, x, y):

    S = np.array([[x, 0, 0],
                  [0, y, 0],
                  [0, 0, 1]],
                 dtype=matrix.dtype)

    matrix[...] = np.dot(S, matrix)
    return matrix

####################################################################################################

def rotate(matrix, angle):

    t = math.radians(angle)
    c = math.cos(t)
    s = math.sin(t)
    R = np.array([[c, -s, 0],
                  [s,  c, 0],
                  [0,  0, 1]],
                 dtype=matrix.dtype)

    matrix[...] = np.dot(R, matrix)
    return matrix

####################################################################################################
# 
# End
# 
####################################################################################################
