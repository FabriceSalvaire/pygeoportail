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

####################################################################################################

from PyQt5 import QtGui, QtNetwork
from PyQt5.QtCore import Qt
from PyQt5.QtNetwork import QNetworkConfiguration

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

    def _check_network_configuration(self):

        self._network_manager = QtNetwork.QNetworkConfigurationManager()
        self._is_online = False # network_manager.isOnline()
        for network_config in self._network_manager.allConfigurations(QNetworkConfiguration.Active):
            if network_config.bearerType() != QNetworkConfiguration.BearerUnknown:
                self._is_online = True

    ##############################################

    def post_init(self):

        super(ViewerApplication, self).post_init()

        self._check_network_configuration()

        glwidget = self._main_window.glwidget
        
        # Fixme: Basic...
        from PyGeoPortail.GraphicEngine.PainterManager import PainterManager
        self.painter_manager = PainterManager(glwidget)
        
        from PyGeoPortail.TileMap.GeoPortail import (GeoPortailPyramid,
                                                     GeoPortailWTMS,
                                                     GeoPortailWTMSLicence,
                                                     GeoPortailMapProvider,
                                                     GeoPortailOthorPhotoProvider)
        from PyGeoPortail.TileMap.LruCache import LruCache
        from PyGeoPortail.TileMap.Projection import GeoAngle, GeoCoordinate
        from PyGeoPortail.TileMap.TileCache import CachedPyramid
        
        geoportail_licence = GeoPortailWTMSLicence(user='fabrice.salvaire@orange.fr',
                                                   password='fA77Sal(!',
                                                   api_key='algzhye2iogn8fvb0nkgf0zx')
        self._geoportail_wtms = GeoPortailWTMS(geoportail_licence)
        
        self._geoportail_map_provider = GeoPortailMapProvider(self._geoportail_wtms)
        self._lru_cache = LruCache(constraint=1024**3)
        self._cached_pyramid = CachedPyramid(self._geoportail_map_provider, self._lru_cache)
        pyramid = self._cached_pyramid._pyramid # Fixme:
        
        from PyGeoPortail.GraphicEngine.MosaicPainter import MosaicPainter
        self._mosaic_painter = MosaicPainter(self.painter_manager, self._cached_pyramid)
        
        from PyGeoPortail.GraphicEngine.PathPainter import PathPainter
        self._path_painter = PathPainter(self.painter_manager)
        
        glwidget.init_tools() # Fixme: for shader
        glwidget._zoom_manager.pyramid = pyramid # Fixme:
        glwidget._ready = True # Fixme:
        
        level = 16
        longitude = GeoAngle(6, 7, 0)
        latitude = GeoAngle(44, 41, 0)
        location = GeoCoordinate(longitude, latitude)
        pyramid_level = pyramid[level]
        x, y = pyramid_level.coordinate_to_projection(location)
        glwidget.zoom_at_with_scale(x, y, zoom_factor=1/pyramid_level.resolution)

        # from PyGeoPortail.GraphicEngine.Path import Path
        # import numpy as np
        # s = 256
        # points = np.array([(x + i*215, y + j*256) for i, j in
        #                    ((0, 0), (1, 1), (1, 2), (3, 4))])
        # colour = QtGui.QColor(Qt.blue)
        # colour = (colour.red(), colour.green(), colour.blue())
        # path = Path(colour, 10, points)
        # self._path_painter.add_item(path)
        # glwidget.update()

####################################################################################################
#
# End
#
####################################################################################################
