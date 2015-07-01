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

###################################################################################################

import logging
import os

####################################################################################################

from PyGeoPortail.GUI.Base.GuiApplicationBase import GuiApplicationBase

####################################################################################################

class ViewerApplication(GuiApplicationBase):

    _logger = logging.getLogger(__name__)

    ###############################################

    def __init__(self, args):

        super(ViewerApplication, self).__init__(args=args)
        self._logger.debug(str(args))

        from .ViewerMainWindow import ViewerMainWindow
        self._main_window = ViewerMainWindow()
        self._main_window.showMaximized()

        self.post_init()

    ##############################################

    def _init_actions(self):

        super(ViewerApplication, self)._init_actions()

    ##############################################

    def post_init(self):

        super(ViewerApplication, self).post_init()
        
        glwidget = self._main_window.glwidget
        
        # Fixme: Basic...
        from PyGeoPortail.GraphicEngine.PainterManager import BasicPainterManager
        self.painter_manager = BasicPainterManager(glwidget)
        
        from PyGeoPortail.GraphicEngine.TexturePainter import TexturePainter
        texture_painter = TexturePainter(self.painter_manager)
        from PyGeoPortail.Image import ImageLoader
        image = ImageLoader.load_image('big-image.jpg')
        image_format = image.image_format
        from PyOpenGLng.Math.Geometry import Point, Offset
        texture_painter.upload(Point(0, 0), Offset(image_format.width, image_format.height), image)
        
        from PyOpenGLng.Math.Interval import Interval2D
        glwidget._image_interval = Interval2D((0, image_format.height), (0, image_format.width))
        
        glwidget.init_tools() # Fixme: for shader
        glwidget._ready = True
        glwidget.display_all()

####################################################################################################
#
# End
#
####################################################################################################
