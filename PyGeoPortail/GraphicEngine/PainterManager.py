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

from .Painter import PainterMetaClass

####################################################################################################

# Fixme:
class BasicPainterManager(object):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, glwidget):
        
        self.glwidget = glwidget

        # Fixme: register self
        self.glwidget._painter_manager = self

        self._painters = {}
        self._sorted_painters = []
        self._create_registered_painters()

    ##############################################

    def register_painter(self, painter, painter_name=None):

        # Fixme: useful ?
        if painter_name is None:
            painter_name = painter.name
        
        if painter_name not in self._painters:
            self._painters[painter_name] = painter
            self._sorted_painters.append(painter)
            self.resort()
        else:
            raise NameError("Painter %s already registered" % (painter_name))

    ##############################################

    def _create_registered_painters(self):

        for painter_name, cls in PainterMetaClass.classes.items():
            self._logger.debug("Add painter %s", painter_name)
            painter = cls(self)

    ##############################################

    def resort(self):

        self._sorted_painters = sorted([painter for painter in self._painters.values()
                                        if bool(painter)])
    
    ##############################################

    def __getitem__(self, name):

        return self._painters[name]

    ##############################################

    def __iter___(self):

        return self._painters.values()

    ##############################################

    def sorted_iterator(self):

        return iter(self._sorted_painters)
    
    ##############################################

    def paint(self):

        # self._logger.info(str(self._sorted_painters))
        for painter in self._sorted_painters:
            painter.paint()

####################################################################################################

class PainterManager(object):

    # Fixme: useful ?
    
    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, glwidget):
        
        super(PainterManager, self).__init__()

        self.glwidget = glwidget

        # Fixme: register self
        self.glwidget._painter_manager = self

        self._background_painter = None
        self.create_background_painter()
        
        self._create_registered_painters()

    ##############################################

    def create_background_painter(self):

        raise NotImplementedError

    ##############################################

    def register_foreground_painter(self, painter, painter_name=None):

        # Fixme: useful ?
        if painter_name is None:
            painter_name = painter.name
        
        if painter_name != 'background' and painter_name not in self._foreground_painters:
            self._foreground_painters[painter_name] = painter
        else:
            raise NameError("Painter %s already registered" % (painter_name))

    ##############################################

    def _create_registered_painters(self):

        self._foreground_painters = {} # enabled/disabled ?
        for painter_name, cls in PainterMetaClass.classes.items():
            self._logger.debug("Add Foreground painter %s", painter_name)
            painter = cls(self)
            self.register_foreground_painter(painter)

    ##############################################

    @property
    def background_painter(self):
        return self._background_painter

    ##############################################

    def foreground_painter(self, name):

        return self._foreground_painters[name]

    ##############################################

    def __getitem__(self, name):

        if name == 'background':
            return self._background_painter
        else:
            return self._foreground_painters[name]
    
    ##############################################

    def painter_iterator(self):

        return iter([self._background_painter] + list(self._foreground_painters.values()))

    ##############################################

    def enabled_painter_iterator(self):

        return iter([painter for painter in self.painter_iterator() if bool(painter)])

    ##############################################

    def paint(self):

        self._logger.info("")
        for painter in self.enabled_painter_iterator():
            painter.paint()

####################################################################################################
#
# End
#
####################################################################################################
