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

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtOpenGL import QGLWidget as QOpenGLWidget

import numpy as np

####################################################################################################

#!# from PyOpenGLng.HighLevelApi.GlOrtho2D import ZoomManagerAbc

from PyOpenGLng.HighLevelApi import GL
from PyOpenGLng.HighLevelApi.Buffer import GlUniformBuffer
from PyOpenGLng.HighLevelApi.GlWidgetBase import GlWidgetBase
from PyOpenGLng.Math.Interval import IntervalInt2D # duplicated

from PyOpenGLng.Math.Geometry import Vector
from PyOpenGLng.HighLevelApi.Ortho2D import ZoomManagerAbc, XAXIS, YAXIS, XYAXIS

from PyGeoPortail.GraphicEngine.GraphicScene import GraphicScene

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ZoomManager(ZoomManagerAbc):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self):

        self.zoom_factor = 1
        self.pyramid = None
        self.level = None

    ##############################################

    def check_zoom(self, zoom_factor):

        # Fixme:
        resolution = 1 / zoom_factor
        self._logger.debug("{} {}".format(self.pyramid, zoom_factor))
        if self.pyramid is None:
            self.zoom_factor = zoom_factor
            return True, zoom_factor
        elif resolution >= self.pyramid.smallest_resolution():
            self.zoom_factor = zoom_factor
            self.level = self.pyramid.closest_level(resolution)
            return True, zoom_factor
        else:
            return False, self.zoom_factor

####################################################################################################

class GlWidget(GlWidgetBase):

    _logger = _module_logger.getChild('GlWidget')

    ##############################################

    def __init__(self, parent):

        self._logger.debug('Initialise GlWidget')
        
        super(GlWidget, self).__init__(parent)
        
        self._application = QtWidgets.QApplication.instance()
        
        self._previous_position = None
        self._previous_position_screen = None
        
        self._painter_manager = None
        
        self.x_step = 1000
        self.y_step = 1000
        self.zoom_step = 2
        
        # Fixme
        self._ready = False

    ##############################################

    def init_tools(self):

        pass
        # from .Cropper import Cropper
        # self.cropper = Cropper(self)

    ##############################################

    def init_glortho2d(self):

        # Set max_area so as to correspond to max_binning zoom centered at the origin
        # Fixme: cf. last level
        area_size = 10**12
        max_area = IntervalInt2D([-area_size, area_size], [-area_size, area_size])

        self._zoom_manager = ZoomManager()
        super(GlWidget, self).init_glortho2d(max_area, zoom_manager=self._zoom_manager, reverse_y_axis=True)
        
        self.scene = GraphicScene(self.glortho2d)

    ##############################################

    def initializeGL(self):

        self._logger.debug('Initialise GL')
        super(GlWidget, self).initializeGL()
        self._init_shader()
        self._ready = False

    ##############################################

    def _init_shader(self):

        self._logger.debug('Initialise Shader')

        from PyGeoPortail.GraphicEngine import ShaderProgrames as ShaderProgrames
        self.shader_manager = ShaderProgrames.shader_manager
        self.position_shader_interface = ShaderProgrames.program_interfaces['position_shader_program_interface']

        # Fixme: share interface
        self._viewport_uniform_buffer = GlUniformBuffer()
        viewport_uniform_block = self.position_shader_interface.uniform_blocks.viewport
        self._viewport_uniform_buffer.bind_buffer_base(viewport_uniform_block.binding_point)

    ##############################################

    def update_model_view_projection_matrix(self):

        # from PyOpenGLng.Math.Transforms import identity, translate, rotate_z, rotate
        # center = self.viewport_area.center()
        # model_matrix = translate(rotate_z(translate(identity(), -center[0], -center[1], 0), 10) , center[0], center[1], 0)
        # matrix = np.dot(matrix, model_matrix)

        self._logger.debug(str(self.glortho2d))
        viewport_uniform_buffer_data = self.glortho2d.viewport_uniform_buffer_data(self.size())
        self._viewport_uniform_buffer.set(viewport_uniform_buffer_data)

    ##############################################

    def zoom_one(self):

        self.glortho2d.zoom_at_center(1.)
        self.update_painter_manager()

    ##############################################

    def zoom_at_with_scale(self, x, y, zoom_factor):

        location = Vector(x, y)
        self.glortho2d.zoom_at_with_scale(location, zoom_factor)
        self.update_painter_manager()

    ##############################################

    def zoom_at(self, x, y):

        location = Vector(x, y)
        self.glortho2d.zoom_at(location)
        self.update_painter_manager()

    ##############################################

    def zoom_interval(self, interval):

        self.glortho2d.zoom_interval(interval)
        self.update_painter_manager()

    ##############################################

    def translate_x(self, dx):

        self.glortho2d.translate(dx, XAXIS)
        self.update_painter_manager()

    ##############################################

    def translate_y(self, dy):

        self.glortho2d.translate(dy, YAXIS)
        self.update_painter_manager()

    ##############################################

    def translate_xy(self, dxy):

        self.glortho2d.translate(dxy, XYAXIS)
        self.update_painter_manager()

    ##############################################

    def wheel_zoom(self, event):

        self._logger.debug('Wheel Zoom')
        
        position = self.window_to_gl_coordinate(event)
        zoom_factor = self.glortho2d.zoom_manager.zoom_factor
        
        delta = event.angleDelta().y()
        if delta == 120:
            zoom_factor *= self.zoom_step
        else:
            zoom_factor /= self.zoom_step
        
        self.glortho2d.zoom_at_with_scale(position, zoom_factor)
        self.update_painter_manager()

    ##############################################

    def update_painter_manager(self):

        self._logger.debug('')
        if self._ready:
            with GL.error_checker():
                self._painter_manager.update()

    ##############################################

    # @opengl_context
    def update(self):

        self._logger.debug('')
        self.makeCurrent()
        self.update_model_view_projection_matrix()
        QOpenGLWidget.update(self)

        # self.emit(QtCore.SIGNAL('update()'))
        # if self._ready:
        #     self._update_zoom_status()

    ##############################################

    def paint(self):

        if self._ready:
            with GL.error_checker():
                self._painter_manager.paint()

    ##############################################

    def event_position(self, event):

        """ Convert mouse coordinate
        """

        self._logger.info("{} {}".format(event.x(), event.y()))
        return np.array((event.x(), event.y()), dtype=np.int) # int for subtraction

    ##############################################

    def _set_previous_position(self, position, position_screen):

        self._previous_position = position
        self._previous_position_screen = position_screen

    ##############################################

    def mousePressEvent(self, event):

        self._logger.info("")

        if not (event.buttons() & QtCore.Qt.LeftButton):
            return

        tool_bar = self._application.main_window.tool_bar
        current_tool = tool_bar.current_tool()
        if current_tool in (tool_bar.crop_tool_action,):
            scene_match = self.scene.mousePressEvent(event)
            if not scene_match:
                if current_tool is tool_bar.crop_tool_action:
                    self.cropper.begin(event) # Fixme: call mousePressEvent
        else:
            if current_tool is tool_bar.position_tool_action:
                position = self.window_to_gl_coordinate(event, round_to_integer=False)
                self.show_coordinate(position)
                self._set_previous_position(position, self.event_position(event))

    ##############################################

    def mouseReleaseEvent(self, event):

        self._logger.info("")

        button = event.button()
        if button & QtCore.Qt.RightButton:
            self.contextual_menu.exec_(event.globalPos())
        elif button & QtCore.Qt.LeftButton:
            tool_bar = self._application.main_window.tool_bar
            current_tool = tool_bar.current_tool()
            # if current_tool is tool_bar.position_tool_action:
            #     position = self.window_to_gl_coordinate(event, round_to_integer=False)
            #     dxy = self._previous_position - position
            #     self.translate_xy(dxy)
            #     self._set_previous_position(position)
            if current_tool is tool_bar.crop_tool_action:
                self.cropper.end(event) # Fixme: call mouseReleaseEvent
                self._logger.info(str(self.cropper.interval))

    ##############################################

    def wheelEvent(self, event):

        return self.wheel_zoom(event)

    ##############################################

    def mouseMoveEvent(self, event):

        self._logger.info("")

        if not (event.buttons() & QtCore.Qt.LeftButton):
            return

        tool_bar = self._application.main_window.tool_bar
        current_tool = tool_bar.current_tool()
        if current_tool is tool_bar.position_tool_action:
            position_screen = self.event_position(event)
            dxy_screen = self._previous_position_screen - position_screen
            # Fixme: if out of viewer position = -1exxx
            position = self.window_to_gl_coordinate(event, round_to_integer=False)
            dxy = self._previous_position - position
            # dxy *= [1, -1]
            self._logger.info("{} {} / {} {}".format(dxy_screen[0], dxy_screen[1], int(dxy[0]), int(dxy[0])))
            dxy_screen *= self.glortho2d.parity_display_scale
            self.translate_xy(dxy_screen)
            self._set_previous_position(position, position_screen)
            self.show_coordinate(position)
        elif current_tool is tool_bar.crop_tool_action:
            self.cropper.update(event) # Fixme: call mouseMoveEvent

    ##############################################

    def show_coordinate(self, position):

        x, y = position
        self._application.main_window.status_bar.update_coordinate_status(x, y)
        # self._set_previous_position(position)

####################################################################################################
#
# End
#
####################################################################################################
