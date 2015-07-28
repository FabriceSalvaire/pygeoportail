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


""" This modules provides tools to draw segments and rectangles primitives.

The aim of these classes has to be used by a Geometry Shader.
"""

####################################################################################################

import logging
import numpy as np

####################################################################################################

from PyOpenGLng.HighLevelApi import GL
from PyOpenGLng.HighLevelApi.Buffer import GlArrayBuffer
from PyOpenGLng.HighLevelApi.VertexArrayObject import GlVertexArrayObject

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class LineVertexArray(GlVertexArrayObject):

    """ Base class to draw segments primitives as lines. """

    _logger = _module_logger.getChild('LineVertexArray')

    ##############################################

    def __init__(self, path=None):

        super(LineVertexArray, self).__init__()

        self._number_of_objects = 0
        self._vertex_array_buffer = GlArrayBuffer()

        if path is not None:
            self.set(path)

    ##############################################

    @property
    def number_of_points(self):
        return self._number_of_objects

    ##############################################

    def reset(self):

        self._number_of_objects = 0
        # Fixme: only for dynamic ?

    ##############################################

    def bind_to_shader(self, shader_program_interface_attribute):

        """ Bind the vertex array to the shader program interface attribute.
        """

        self.bind()
        shader_program_interface_attribute.bind_to_buffer(self._vertex_array_buffer)
        self.unbind()

    ##############################################

    def draw(self):

        """ Draw the vertex array as lines. """

        if self._number_of_objects >= 2:
            self.bind()
            GL.glDrawArrays(GL.GL_LINES, 0, self._number_of_objects)
            self.unbind()

    ##############################################

    def set(self, path):

        """ Set the vertex array from an iterable of segments. """

        # Fixme: make no sense, must be a list of paths

        self._number_of_objects = path.number_of_points # Right ?
        vertexes = np.zeros((self._number_of_objects, 2), dtype=np.float32)
        vertexes[...] = path.points
        # vertexes += .5 # Fixme: to shader
        self._vertex_array_buffer.set(vertexes)

####################################################################################################

class LineStripVertexArray(LineVertexArray):

    """ Base class to draw segments primitives as line strips. """

    _logger = _module_logger.getChild('LineStripVertexArray')

    ##############################################

    def draw(self):

        """ Draw the vertex array as lines. """

        if self._number_of_objects >= 2:
            self.bind()
            GL.glDrawArrays(GL.GL_LINE_STRIP_ADJACENCY, 0, self._number_of_objects +2)
            self.unbind()

    ##############################################

    def set(self, path):

        """ Set the vertex array from an iterable of segments. """

        self._number_of_objects = path.number_of_points # Right ?
        vertexes = np.zeros((self._number_of_objects + 2, 2), dtype=np.float32)
        vertexes[1:-1] = path.points
        vertexes[0] = vertexes[1]
        vertexes[-1] = vertexes[-2]
        # vertex += .5
        self._vertex_array_buffer.set(vertexes)

####################################################################################################

class DynamicLineStripVertexArray(LineStripVertexArray):

    _logger = _module_logger.getChild('DynamicLineStripVertexArray')

    ##############################################

    def __init__(self, size=1000, upscale_factor=3):

        super(DynamicLineStripVertexArray, self).__init__()

        self._upscale_factor = upscale_factor
        self._allocate(size)
        
        self._update_vertex = np.zeros((2, 2), dtype=np.float32)

    ##############################################

    def _allocate(self, size):

        self._size = size
        self._number_of_objects_max = self._size / 2 -2
        array = np.zeros((size, 2), dtype=np.float32)
        self._vertex_array_buffer.set(array, usage=GL.GL_DYNAMIC_DRAW)

    ##############################################

    def add_vertex(self, point):

        """ Set the vertex array from an iterable of segments. """

        self._number_of_objects += 1

        if self._number_of_objects > self._number_of_objects_max:
            # Reallocate buffer and copy data
            data = self._vertex_array_buffer.read_sub_data(0, size=2*self._size)
            # data.shape = self._size, 2
            size = self._size * self._upscale_factor
            self._logger.debug("upscale buffer to size {}".format(size))
            self._allocate(size)
            self._vertex_array_buffer.set_sub_data(data, 0)
        
        vertex = self._update_vertex
        vertex[:] = point
        # vertex += .5
        if self._number_of_objects > 1:
            offset = self._number_of_objects
        else:
            offset = 0
        self._vertex_array_buffer.set_sub_data(vertex, 2*offset)

####################################################################################################

class DynamicLineVertexArray(LineVertexArray):

    _logger = _module_logger.getChild('DynamicLineVertexArray')

    ##############################################

    def __init__(self):

        super(DynamicLineVertexArray, self).__init__()
        
        array = np.zeros((2, 2), dtype=np.float32)
        self._vertex_array_buffer.set(array)
        
        self._update_vertex = np.zeros((2,), dtype=np.float32)

    ##############################################

    def _set_vertex(self, point, offset):

        # Fixme: to ensure compatible type ?
        vertex = self._update_vertex
        vertex[:] = point
        # vertex += .5
        self._vertex_array_buffer.set_sub_data(vertex, offset)

    ##############################################

    def set_first_vertex(self, point):

        self._number_of_objects = 1
        self._set_vertex(point, 0)

    ##############################################

    def set_second_vertex(self, point):

        self._number_of_objects = 2
        self._set_vertex(point, 2)

####################################################################################################
#
# End
#
####################################################################################################
