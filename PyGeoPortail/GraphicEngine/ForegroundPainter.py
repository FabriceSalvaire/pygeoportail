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

from PyOpenGLng.HighLevelApi import GL
from PyOpenGLng.HighLevelApi.ImageTexture import ImageTexture
from PyOpenGLng.HighLevelApi.PrimitiveVertexArray import GlSegmentVertexArray
from PyOpenGLng.HighLevelApi.TextVertexArray import TextVertexArray
from PyOpenGLng.HighLevelApi.TextureFont import TextureFont
from PyOpenGLng.HighLevelApi.TextureVertexArray import GlTextureVertexArray
from PyOpenGLng.Math.Geometry import Point, Offset, Segment

from .Painter import RegisteredPainter, Painter
from PyGeoPortail.Tools.TimeStamp import ObjectWithTimeStamp

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class RoiPainter(RegisteredPainter):

    __painter_name__ = 'roi'

    _logger = _module_logger.getChild('RoiPainter')

    ##############################################
    
    def __init__(self, painter_manager):

        super(RoiPainter, self).__init__(painter_manager)

        self._glwidget = self._painter_manager.glwidget
        self._shader_program = self._glwidget.shader_manager.roi_shader_program
        self.reset()

    ##############################################

    @property
    def paint_box(self):
        return self._paint_box

    @paint_box.setter
    def paint_box(self, paint_box):
        self._paint_box = paint_box

    @property
    def paint_grips(self):
        return self._paint_grips

    @paint_grips.setter
    def paint_grips(self, paint_grips):
        self._paint_grips = paint_grips

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, margin):
        self._margin = margin

    ##############################################

    def reset(self):

        # self._logger.debug('Reset ROI Box Painter')
        self._bounding_box = None
        self._segment_vertex_array = None
        self._margin = 0
        self.disable()

    ##############################################

    def disable(self):

        # self._logger.debug('Disable ROI Box Painting')
        super(RoiPainter, self).disable()
        self._paint_box = False
        self._paint_grips = False

    ##############################################

    def enable(self, paint_grips=False):

        # self._logger.debug('Enable ROI Box Painting')
        self._paint_box = True
        self._paint_grips = paint_grips
        # super(RoiPainter, self).enable()

    ##############################################

    def update_bounding_box(self, interval):

        # self._logger.debug('Update ROI Box')
        # Fixme: move to glwidget
        self._glwidget.makeCurrent()
        if interval is not None:
            segments = []
            x_min, y_min, x_max, y_max = interval.bounding_box()
            segment = Segment(Point(x_min, y_min), Point(x_max, y_max))
            segments.append(segment)
            self._segment_vertex_array = GlSegmentVertexArray(segments)
            self._segment_vertex_array.bind_to_shader(self._shader_program.interface.attributes.position)
        self._glwidget.doneCurrent()

    ##############################################

    def paint(self):

        if self._paint_box and self._segment_vertex_array is not None:
            # self._logger.debug('Paint ROI Box')
            self._shader_program.bind()
            self._shader_program.uniforms.colour = (0., 0., 0.) # Fixme:
            self._shader_program.uniforms.margin = self._margin
            #!# Fixme: self._shader_program.uniforms.paint_grips = self._paint_grips # Fixme: always on, check Cropper
            self._segment_vertex_array.draw()

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

class SketcherPainter(Painter, ObjectWithTimeStamp):

    """ Paint a dynamic image. """

    # Fixme: similar to texture painter
    
    __painter_name__ = 'sketcher inner-painter'
    
    _logger = _module_logger.getChild('SketcherPainter')

    ##############################################
    
    def __init__(self, painter_manager):

        ObjectWithTimeStamp.__init__(self)
        Painter.__init__(self, painter_manager)

        self._glwidget = self._painter_manager.glwidget
        self._sketcher = None
        self._shader_program = self._glwidget.shader_manager.texture_shader_program
        # self._shader_program = None
        self._texture_vertex_array = None
        self._uploaded = False
        
    ##############################################

    @property
    def shader_program(self):
        return self._shader_program
    
    @shader_program.setter
    def shader_program(self, shader_program):
        self._shader_program = shader_program

    ##############################################

    def create_texture(self, sketcher):

        # self._logger.info("")
        self._sketcher = sketcher
        image_format = sketcher.image.image_format
        self._glwidget.makeCurrent() #?
        dimension = Offset(image_format.width, image_format.height)
        with GL.error_checker():
            self._texture_vertex_array = GlTextureVertexArray(position=Point(0, 0), dimension=dimension)
            shader_program_interface = self._shader_program.interface.attributes
            self._texture_vertex_array.bind_to_shader(shader_program_interface)
        self._uploaded = False

    ##############################################

    def upload_data(self):

        # self._glwidget.makeCurrent()
        # self._glwidget.doneCurrent()

        # self._logger.info("")
        # should check image_format
        self._texture_vertex_array.set(self._sketcher.image)
        self.modified()
        self._uploaded = True

    ##############################################

    def paint(self):

        if (self._status
            and self._texture_vertex_array is not None
            and self._shader_program is not None):

            # self._logger.info("uploaded {}".format(self._uploaded))

            # if self.source > self: # timestamp
            print(self._uploaded, self._sketcher.modified_time, self._modified_time)
            if not self._uploaded or self._sketcher._modified_time > self._modified_time:
                self.upload_data()

            GL.glEnable(GL.GL_BLEND)
            # Blending: O = Sf*S + Df*D
            # alpha: 0: complete transparency, 1: complete opacity
            # Set (Sf, Df) for transparency: O = Sa*S + (1-Sa)*D 
            GL.glBlendEquation(GL.GL_FUNC_ADD)
            GL.glBlendFunc(1, 1)
            # GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
                
            shader_program = self._shader_program
            shader_program.bind()
            self._texture_vertex_array.draw()
            shader_program.unbind()

            GL.glDisable(GL.GL_BLEND)

####################################################################################################

class ObjectPainter(RegisteredPainter):

    __painter_name__ = 'object'

    _logger = _module_logger.getChild('ObjectPainter')

    ##############################################
    
    def __init__(self, painter_manager):

        super(ObjectPainter, self).__init__(painter_manager)

        self._glwidget = self._painter_manager.glwidget
        self._shader_program = self._glwidget.shader_manager.object_shader_program
        self.reset()

    ##############################################

    def reset(self):

        self._vertex_array = None
        self.disable()

    ##############################################

    def update(self, interval):

        self._glwidget.makeCurrent()
        if interval is not None:
            segments = []
            x_min, y_min, x_max, y_max = interval.bounding_box()
            segment = Segment(Point(x_min, y_min), Point(x_max, y_max))
            segments.append(segment)
            self._vertex_array = GlSegmentVertexArray(segments)
            self._vertex_array.bind_to_shader(self._shader_program.interface.attributes.position)
        self._glwidget.doneCurrent()

    ##############################################

    def paint(self):

        if self._vertex_array is not None:
            self._shader_program.bind()
            self._shader_program.uniforms.colour = (0, 0, 0)
            self._vertex_array.draw()
            
####################################################################################################
#
# End
#
####################################################################################################
