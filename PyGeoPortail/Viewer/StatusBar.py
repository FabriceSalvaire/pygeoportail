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

from PyQt5 import QtWidgets, QtCore

####################################################################################################

class StatusBar(object):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, main_window):

        self._main_window = main_window
        self._status_bar = self._main_window.statusBar()

        self._application = QtWidgets.QApplication.instance()

        label_definitions = (('coordinate_label', 'Coordinate of the pointer'),
                             ('message_label', 'Message'),
                             )

        for attribute_name, tool_tip in label_definitions:
            widget = QtWidgets.QLabel(toolTip=tool_tip)
            setattr(self, attribute_name, widget)

        coordinate_max = 10**5
        self.update_coordinate_status(coordinate_max, coordinate_max)
        self.update_status_message('W'*30)

        for widget in (self.coordinate_label,
                       self.message_label,
                       ):
            # Permanently means that the widget may not be obscured by temporary messages. It is is
            # located at the far right of the status bar.
            self._status_bar.addPermanentWidget(widget)
            widget.setMinimumSize(widget.sizeHint())
            widget.clear()

        self.update_coordinate_status(0, 0)

    ##############################################

    def update_status_message(self, message):

        self.message_label.setText(message)

    ##############################################

    def update_coordinate_status(self, x, y):

        text = '(%6u, %6u) px' % (x, y)
        self.coordinate_label.setText(text)


####################################################################################################
#
# End
#
####################################################################################################
