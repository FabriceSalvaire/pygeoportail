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
        
        from PyGeoPortail.TileMap.GeoPortail import (GeoPortailPyramid,
                                                     GeoPortailWTMS,
                                                     GeoPortailMapProvider,
                                                     GeoPortailOthorPhotoProvider)
        from PyGeoPortail.TileMap.LruCache import LruCache
        from PyGeoPortail.TileMap.Projection import GeoAngle, GeoCoordinate
        from PyGeoPortail.TileMap.TileCache import CachedPyramid
        
        self._geoportail_wtms = GeoPortailWTMS(user='fabrice.salvaire@orange.fr',
                                               password='fA77Sal(!',
                                               api_key='qd58byg78dg3nloou4ksa0pz')
        
        self._geoportail_map_provider = GeoPortailMapProvider(self._geoportail_wtms)
        self._lru_cache = LruCache(constraint=1024**3)
        self._cached_pyramid = CachedPyramid(self._geoportail_map_provider, self._lru_cache)
        
        from PyGeoPortail.GraphicEngine.MosaicPainter import MosaicPainter
        self._mosaic_painter = MosaicPainter(self.painter_manager, self._cached_pyramid)
        
        level = 16
        longitude = GeoAngle(6, 7, 0)
        latitude = GeoAngle(44, 41, 0)
        location = GeoCoordinate(longitude, latitude)
        x, y = self._cached_pyramid._pyramid[level].coordinate_to_projection(location)
        glwidget.zoom_at(x, y)
        
        glwidget.init_tools() # Fixme: for shader
        glwidget._ready = True
        glwidget.display_all()

####################################################################################################
#
# End
#
####################################################################################################
