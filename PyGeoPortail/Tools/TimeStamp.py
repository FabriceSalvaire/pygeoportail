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

from atomiclong import AtomicLong

####################################################################################################

class TimeStamp(object):

    _time_stamp = AtomicLong(0)

    ##############################################

    def __init__(self):

        self._modified_time = 0

    ##############################################

    def __repr__(self):
        return 'TS ' + str(self._modified_time)

    ##############################################

    def __lt__(self, other):
        return self._modified_time < other._modified_time

    ##############################################

    def __gt__(self, other):
        return self._modified_time > other._modified_time

    ##############################################

    def __int__(self):
        return self._modified_time

    ##############################################

    def modified(self):

        # Should be atomic
        TimeStamp._time_stamp += 1
        self._modified_time = TimeStamp._time_stamp.value

####################################################################################################

class ObjectWithTimeStamp(object):

     ##############################################

    def __init__(self):

        self._modified_time = TimeStamp()

    ##############################################

    @property
    def modified_time(self):
        return int(self._modified_time)

    ##############################################

    def modified(self):

        self._modified_time.modified()

####################################################################################################
# 
# End
# 
####################################################################################################
