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

# cf. http://jswhit.github.io/pyproj/

# # proj_uv = Proj4._ffi.new('projUV *', {'u':math.radians(2.478917), 'v':math.radians(48.805639)})
# proj_uv = Proj4._ffi.new('projUV *', [math.radians(2.478917), math.radians(48.805639)])
# proj_xy = Proj4._ffi.new('projXY *', [0, 0])
# Proj4.pj_fwd(proj_uv, proj, proj_xy)

####################################################################################################

import math

####################################################################################################

from _proj4 import ffi as _ffi
from _proj4 import lib as _lib

####################################################################################################

release = _ffi.string(_lib.get_pj_release()).decode('ascii')

####################################################################################################

class Proj(object):

    ##############################################

    def __init__(self, definition):

        self._ctx = _lib.pj_ctx_alloc()
        self._proj = _lib.pj_init_plus_ctx(self._ctx, definition.encode('ascii'))
        
        errno = _lib.pj_ctx_get_errno(self._ctx)
        if errno != 0:
            raise RuntimeError(_lib.pj_strerrno(errno))

    ##############################################

    def __del__(self):

        _lib.pj_free(self._proj)
        _lib.pj_ctx_free(self._ctx)

####################################################################################################

def transform(proj1, proj2, x, y, z=None, radians=False):

    # Fixme: implement Numpy array

    if _lib.pj_is_latlong(proj1._proj) and not radians:
        x = math.radians(x)
        y = math.radians(y)
    x_ptr = _ffi.new('double []', [x])
    y_ptr = _ffi.new('double []', [y])
    z_ptr = _ffi.new('double []', [0])
    count = 1
    offset = 0
    
    errno = _lib.pj_transform(proj1._proj, proj2._proj, count, offset, x_ptr, y_ptr, z_ptr)
    if errno != 0:
        raise RuntimeError(_lib.pj_strerrno(errno))
    
    return x_ptr[0], y_ptr[0], z_ptr[0]

####################################################################################################
#
# End
#
####################################################################################################
