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

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

####################################################################################################

from PyGeoPortail.GUI.Base.MainWindowBase import MainWindowBase
from PyGeoPortail.GUI.Base.IconLoader import IconLoader
from .GlWidget import GlWidget

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ViewerMainWindow(MainWindowBase):

    _logger = _module_logger.getChild('ViewerMainWindow')

    ##############################################

    def __init__(self, parent=None):

        super(ViewerMainWindow, self).__init__(title='PyGeoPortail Viewer', parent=parent)

        self._init_ui()
        self._create_actions()
        self._create_toolbar()

        from .StatusBar import StatusBar
        self.status_bar = StatusBar(self)

    ##############################################

    def _create_actions(self):

        icon_loader = IconLoader()

        self._refresh_action = \
                QtWidgets.QAction(# icon_loader[''],
                    'Refresh',
                    self,
                    toolTip='Refresh',
                    triggered=self.glwidget.update,
                    shortcut='Ctrl+R',
                    shortcutContext=Qt.ApplicationShortcut,
                )

        self._display_all_action = \
                QtWidgets.QAction(# icon_loader[''],
                    'Display All',
                    self,
                    toolTip='Display All',
                    triggered=self.glwidget.display_all,
                    shortcut='Ctrl+A',
                    shortcutContext=Qt.ApplicationShortcut,
                )

    ##############################################

    def _create_toolbar(self):

        self._image_tool_bar = self.addToolBar('Main')
        for item in (self._refresh_action,
                     self._display_all_action,
                    ):
            if isinstance(item,QtWidgets.QAction):
                self._image_tool_bar.addAction(item)
            else:
                self._image_tool_bar.addWidget(item)

        from .ToolBar import ToolBar
        self.tool_bar = ToolBar(self)

    ##############################################

    def init_menu(self):

        super(ViewerMainWindow, self).init_menu()

    ##############################################

    def _init_ui(self):

        # self._central_widget = QtWidgets.QWidget(self)
        # self._horizontal_layout = QtWidgets.QHBoxLayout(self._central_widget)

        self.glwidget = GlWidget(self) # ._central_widget
        self.glwidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self._central_widget = self.glwidget

        # self._horizontal_layout.addWidget(self.glwidget)
        self.setCentralWidget(self._central_widget)

        self._translate_ui()

    ##############################################

    def _translate_ui(self):

        pass

####################################################################################################
#
# End
#
####################################################################################################
