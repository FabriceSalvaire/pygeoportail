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

# Fixme: Purpose ?

####################################################################################################

import logging
import os

####################################################################################################

from PyOpenGLng.HighLevelApi.ImageTexture import ImageTexture
from PyOpenGLng.HighLevelApi.TextVertexArray import TextVertexArray
from PyOpenGLng.HighLevelApi.TextureFont import TextureFont

from .Painter import RegisteredPainter

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class TextPainter(RegisteredPainter):

    __painter_name__ = 'text'

    _logger = _module_logger.getChild('TextPainter')

    ##############################################

    def __init__(self, painter_manager):

        super(TextPainter, self).__init__(painter_manager)
        
        self._glwidget = self._painter_manager.glwidget
        self._text_shader_program = self._glwidget.shader_manager.text_shader_program
        # self.reset()
        
        # font_path = os.path.join(ConfigInstall.Path.share_directory, 'fonts', 'Vera.ttf')
        font_path = os.path.join(os.path.dirname(__file__), 'Vera.ttf')
        self._font = TextureFont(font_path)
        self._font_size = self._font[25]
        self._font_size.load_all_glyphs()
        
        self._font_atlas_texture = ImageTexture(self._font.atlas.data)
        
        self._text_vertex_array = None

    ##############################################

    def set_text(self, interval):

        self._glwidget.makeCurrent()
        self._text_vertex_array = TextVertexArray(self._font_atlas_texture)
        for i in range(8):
            self._text_vertex_array.add(text=str(i+1),
                                        font_size=self._font_size,
                                        colour=(1., 1., 1., 1.),
                                        x=interval.x.inf + i/8 * interval.x.length() ,
                                        y=interval.y.inf,
                                        anchor_x='left', anchor_y='baseline',
                                        # anchor_x='center', anchor_y='bottom',
                                    )
        self._text_vertex_array.upload()
        self._text_vertex_array.bind_to_shader(self._text_shader_program.interface.attributes)
        self._glwidget.doneCurrent()

    ##############################################

    def paint(self):

        # self._logger.debug("")
        if self._text_vertex_array is not None:
            shader_program = self._text_shader_program
            # shader_program.bind()
            # shader_program.uniforms. ...
            self._text_vertex_array.draw(shader_program)
            # shader_program.unbind()

####################################################################################################
#
# End
#
####################################################################################################
