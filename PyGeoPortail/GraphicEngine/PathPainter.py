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

from .Painter import Painter
from .PrimitiveVertexArray import (LineVertexArray, LineStripVertexArray,
                                   DynamicLineVertexArray, DynamicLineStripVertexArray)

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PrimitivePainter(Painter):

    __primitive_class__ = None

    _logger = _module_logger.getChild('PrimitivePainter')

    ##############################################

    def __init__(self, painter_manager, **kwargs):

        super(PrimitivePainter, self).__init__(painter_manager, **kwargs)

        self._glwidget = self._painter_manager.glwidget
        self._current_path = None
        self._items = {}

    ##############################################

    def reset(self):

        pass
        # self.disable()

    ##############################################

    def add_item(self, path):

        # Fixme: upload_path ?

        self._logger.debug('Add path {}'.format(path.id))
        # Fixme: move to glwidget
        self._glwidget.makeCurrent()
        vao = self.__primitive_class__(path)
        # Fimme: add attributes
        vao.id = path.id
        vao.colour = path.colour
        vao.line_width = path.pencil_size
        vao.z_value = path.z_value
        vao.bind_to_shader(self._shader_program.interface.attributes.position)
        self._items[vao.id] = vao
        self._glwidget.doneCurrent()

    ##############################################

    def update_item(self, path):

        vao = self._items[path.id]
        vao.colour = path.colour
        vao.line_width = path.pencil_size

    ##############################################

    def remove_item(self, path):

        del self._items[path.id]

    ##############################################

    def paint(self):

        # GL.glEnable(GL.GL_BLEND)
        # # Blending: O = Sf*S + Df*D
        # # alpha: 0: complete transparency, 1: complete opacity
        # # Set (Sf, Df) for transparency: O = Sa*S + (1-Sa)*D
        # GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        self._shader_program.bind()
        # self._shader_program.uniforms.antialias_diameter = 1
        for vao in self._items.values():
            self._paint_vao(vao)
        if self._current_path is not None:
            self._paint_vao(self._current_path)

        # GL.glDisable(GL.GL_BLEND)

    ##############################################

    def _paint_vao(self, vao):

        self._shader_program.uniforms.colour = vao.colour
        self._shader_program.uniforms.line_width = vao.line_width
        self._shader_program.uniforms.z_value = vao.z_value
        vao.draw()

####################################################################################################

class PathPainter(PrimitivePainter):

    __painter_name__ = 'path'
    __primitive_class__ = LineStripVertexArray

    ##############################################

    def __init__(self, painter_manager, **kwargs):

        super(PathPainter, self).__init__(painter_manager, **kwargs)
        self._shader_program = self._glwidget.shader_manager.path_shader_program
        
        self._glwidget.makeCurrent()
        self._current_path = DynamicLineStripVertexArray(size=100, upscale_factor=3)
        self._current_path.bind_to_shader(self._shader_program.interface.attributes.position)
        self._current_path.colour = (1, 1, 1) # Fixme:
        self._current_path.line_width = 1
        self._current_path.z_value = 0
        # self._glwidget.doneCurrent()

    ##############################################

    def reset_current_path(self):

        self._current_path.reset()

    ##############################################

    def update_current_item(self, path):

        self._logger.debug('Update current path')
        
        # Fixme: move to glwidget
        self._glwidget.makeCurrent()
        
        current_path = self._current_path
        if not current_path.number_of_points:
            self._current_path.colour = path.colour
            self._current_path.line_width = path.pencil_size
        
        self._current_path.add_vertex(path.p1)

        # self._glwidget.doneCurrent()

####################################################################################################
#
# End
#
####################################################################################################
