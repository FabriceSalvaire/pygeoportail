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

def split_set(l1, l2):

    l1_and_l2 = l1 & l2

    l1_only = l1 - l1_and_l2
    l2_only = l2 - l1_and_l2

    return l1_only, l1_and_l2, l2_only

def set2list(s1):

    l1 = list(s1)
    l1.sort()

    return l1

def split_list(l1, l2):

    l1_only, l1_and_l2, l2_only = split_set(set(l1), set(l2))

    return [set2list(x) for x in (l1_only, l1_and_l2, l2_only)]

####################################################################################################
#
# End
#
####################################################################################################
