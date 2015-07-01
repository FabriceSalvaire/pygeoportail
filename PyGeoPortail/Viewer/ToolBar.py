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

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt

####################################################################################################

from PyGeoPortail.GUI.Base.IconLoader import IconLoader

####################################################################################################

class ToolBar(object):

    icon_size = 22

    ##############################################

    def __init__(self, main_window):

        self._application = QtWidgets.QApplication.instance()
        self._main_window = main_window
        self._tool_bar = main_window.addToolBar('Main')

        self._create_actions()
        self._init_tool_bar()

    ##############################################

    def _create_actions(self):

        icon_loader = IconLoader()

        self.clear_tool_action = \
            QtWidgets.QAction('Clear',
                          self._application,
                          toolTip='Clear Tool',
                          triggered=self.clear_tool,
                          )

        self.position_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('position-tool', self.icon_size),
                          'Position Tool',
                          self._application,
                          checkable=True,
                          )

        self.crop_tool_action = \
            QtWidgets.QAction(icon_loader.get_icon('crop-tool', self.icon_size),
                          'Crop Tool',
                          self._application,
                          checkable=True,
                          )

        self._action_group = QtWidgets.QActionGroup(self._application)
        for action in (self.position_tool_action,
                       self.crop_tool_action,
                       ):
            self._action_group.addAction(action)

    ##############################################

    def _init_tool_bar(self):

        self.position_tool_action.setChecked(True)

        self._tool_bar.addAction(self.clear_tool_action)
        items = (self.position_tool_action,
                 self.crop_tool_action,
        )
        for item in items:
            if isinstance(item, QtWidgets.QAction):
                self._tool_bar.addAction(item)
            else:
                self._tool_bar.addWidget(item)

    ##############################################

    def current_tool(self):

        return self._action_group.checkedAction()

    ##############################################

    def clear_tool(self):

        current_tool = self.current_tool()

        if current_tool is self.crop_tool_action:
            self._application.main_window.glwidget.cropper.reset()

####################################################################################################
#
# End
#
####################################################################################################
