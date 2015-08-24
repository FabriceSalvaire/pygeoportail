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

import numpy as np

import cv2

####################################################################################################

def cv_threshold(image_src, image_dst, threshold, threshold_type, max_value=255):
    # Source array (single-channel, 8-bit or 32-bit floating point)
    # max_value is used for THRESH_BINARY
    image_float = np.array(image_src, dtype=np.float32)
    cv2.threshold(image_float, threshold, max_value, threshold_type, image_float)
    image_dst[...] = image_float[...]

####################################################################################################

def cv_threshold_to_zero(image_src, image_dst, threshold):
    cv_threshold(image_src, image_dst, threshold, cv2.THRESH_TOZERO)

####################################################################################################

def cv_threshold_to_binary(image_src, image_dst, threshold, max_value=255):
    cv_threshold(image_src, image_dst, threshold, cv2.THRESH_BINARY, max_value)

####################################################################################################

def ball_structuring_element(horizontal_radius, vertical_radius):

    number_of_rows = 2*vertical_radius +1
    number_of_columns = 2*horizontal_radius +1
    kernel = np.ones((number_of_rows, number_of_columns))
    anchor = (horizontal_radius, vertical_radius)
    
    return kernel, anchor

####################################################################################################

def _unit_ball():
    radius = 1
    return ball_structuring_element(radius, radius)
unit_ball = _unit_ball()

####################################################################################################

def horizontal_structuring_element(radius):
    return ball_structuring_element(horizontal_radius=radius, vertical_radius=0)

def vertical_structuring_element(radius):
    return ball_structuring_element(horizontal_radius=0, vertical_radius=radius)

####################################################################################################

def circular_structuring_element(radius):

    size = 2*radius +1
    kernel = np.ones((size, size), dtype=np.uint8)
    for i in range(1, radius +1):
        for j in range(1, radius +1):
            if i**2 + j**2 > radius**2:
                kernel[radius+i, radius+j] = 0
                kernel[radius-i, radius+j] = 0
                kernel[radius+i, radius-j] = 0
                kernel[radius-i, radius-j] = 0
    anchor = (radius, radius)
    
    return kernel, anchor

####################################################################################################

def diagonal_structuring_element(radius):

    size = 2*radius +1
    kernel = np.ones((size, size), dtype=np.uint8)
    anchor = (radius, radius)
    
    return kernel, anchor

####################################################################################################

def anti_diagonal_structuring_element(radius):

    size = 2*radius +1
    kernel = np.transpose(np.ones((size, size), dtype=np.uint8))
    anchor = (radius, radius)
    return kernel, anchor

####################################################################################################

def morphology_erode(image_src, image_dst, structuring_element):
    kernel, anchor = structuring_element
    cv2.erode(image_src, kernel, image_dst, anchor)

####################################################################################################

def morphology_dilate(image_src, image_dst, structuring_element):
    kernel, anchor = structuring_element
    cv2.dilate(image_src, kernel, image_dst, anchor)

####################################################################################################

def morphology_close(image_src, image_dst, structuring_element):
    kernel, anchor = structuring_element
    cv2.morphologyEx(image_src, cv2.MORPH_CLOSE, kernel, image_dst, anchor)

####################################################################################################

def morphology_open(image_src, image_dst, structuring_element):
    kernel, anchor = structuring_element
    cv2.morphologyEx(image_src, cv2.MORPH_OPEN, kernel, image_dst, anchor)

####################################################################################################

def morphology_gradient(image_src, image_dst, structuring_element):
    kernel, anchor = structuring_element
    cv2.morphologyEx(image_src, cv2.MORPH_GRADIENT, kernel, image_dst, anchor)

####################################################################################################

def alternate_sequential_filter(image_src, image_dst, radius_max, structuring_element, open_first=True):
    for radius in range(1, radius_max +1):
        kernel, anchor = structuring_element(radius)
        if open_first:
            cv2.morphologyEx(image_src, cv2.MORPH_OPEN, kernel, image_dst, anchor)
            cv2.morphologyEx(image_dst, cv2.MORPH_CLOSE, kernel, image_dst, anchor)
        else:
            cv2.morphologyEx(image_src, cv2.MORPH_CLOSE, kernel, image_dst, anchor)
            cv2.morphologyEx(image_dst, cv2.MORPH_OPEN, kernel, image_dst, anchor)
        image_src = image_dst

####################################################################################################
#
# End
#
####################################################################################################
