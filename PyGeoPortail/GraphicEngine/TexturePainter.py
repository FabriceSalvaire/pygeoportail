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

####################################################################################################

from PyOpenGLng.HighLevelApi import GL
from PyOpenGLng.HighLevelApi.TextureVertexArray import GlTextureVertexArray

####################################################################################################

from .Painter import Painter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class TexturePainter(Painter):

    __painter_name__ = 'texture'

    _logger = _module_logger.getChild('TexturePainter')

    ##############################################

    def __init__(self, *args, **kwargs):

        super(TexturePainter, self).__init__(*args, **kwargs)

        self._shader_program = self._glwidget.shader_manager.texture_shader_program
        self._texture_vertex_array = None

    ##############################################

    def upload(self, position, dimension, image):

        self._glwidget.makeCurrent() #?
        with GL.error_checker():
            self._texture_vertex_array = GlTextureVertexArray(position, dimension, image)
            shader_program_interface = self._shader_program.interface.attributes
            self._texture_vertex_array.bind_to_shader(shader_program_interface)

    ##############################################

    def paint_texture(self, texture_vertex_array):

        # Fixme: efficiency, design
        shader_program = self._shader_program
        shader_program.bind()
        texture_vertex_array.draw()
        shader_program.unbind()

    ##############################################

    def paint(self):

        # Fixme: status, done in manager ?
        if (self._status and self._texture_vertex_array is not None):
            self.paint_texture(self._texture_vertex_array)

####################################################################################################
#
# End
#
####################################################################################################
