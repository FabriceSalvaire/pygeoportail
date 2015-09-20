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

from cffi import FFI

####################################################################################################

from ctypes.util import find_library

####################################################################################################

ffi = FFI()

api_path = os.path.join(os.path.dirname(__file__), 'proj4_api.h')
with open(api_path, 'r') as f:
    definitions = f.read()
ffi.cdef(definitions)

api_path = os.path.join(os.path.dirname(__file__), 'proj4.c')
with open(api_path, 'r') as f:
    source = f.read()
ffi.set_source('_proj4', source, libraries=['proj'],)

####################################################################################################

if __name__ == "__main__":
    ffi.compile()

####################################################################################################
#
# End
#
####################################################################################################
