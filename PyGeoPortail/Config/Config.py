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

import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

####################################################################################################

class Path(object):

    config_directory = os.path.join(os.environ['HOME'], '.config', 'pygeoportail')

    # data_directory = os.path.join(os.environ['HOME'], '.local', 'share', 'data', 'pygeoportail')
    data_directory = os.path.join(os.environ['HOME'], '.local', 'pygeoportail')

####################################################################################################

class Email(object):

    from_address = 'fabrice.salvaire@orange.fr'
    to_address = ['fabrice.salvaire@orange.fr',]

####################################################################################################

class Help(object):

    host = 'localhost'
    url_scheme = 'http'
    url_path_pattern = '/'

####################################################################################################

class DiskCache(object):

    path = os.path.join(os.environ['HOME'], '.cache', 'pygeoportail')

####################################################################################################
#
# End
#
####################################################################################################
