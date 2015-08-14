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

from collections import OrderedDict
import logging

from rtree import Rtree

####################################################################################################

from PyGeoPortail.Math.Interval import IntervalInt2D

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class GraphicItem(object):

    __last_id__ = 0

    ##############################################

    @staticmethod
    def _get_new_id():

        # Fixme: should be atomic
        GraphicItem.__last_id__ += 1

        return GraphicItem.__last_id__

    ##############################################

    def __init__(self, position=None):

        self._id = GraphicItem._get_new_id()
        
        self._position = position
        self._scale = 1 # (x, y)
        self._rotation = 0
        
        self._interval = None
        
        self._z_value = - self._id / 2**16 # 65535 objects
        
        self._scene = None
        self._is_selected = False

    ##############################################

    def __repr__(self):
        return "GraphicItem {}".format(self._id)

    ##############################################

    @property
    def id(self):
        return self._id

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def scale_factor(self):
        return self._scale

    @scale_factor.setter
    def scale_factor(self, value):
        self._scale = value

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value

    @property
    def z_value(self):
        return self._z_value

    @z_value.setter
    def z_value(self, value):
        self._z_value = value

    @property
    def interval(self):
        return self._interval

    @property
    def bounding_box(self):

        return self._interval.bounding_box()

    @property
    def scene(self):
        return self._scene

    ##############################################

    def __lt__(self, other):

        return self._z_value < other.z_value

    ##############################################

    def __hash__(self):

        return self._id

    ##############################################

    def select(self):

        if self._scene is not None:
            self._is_selected = True
            self._scene._select_item(self)

    ##############################################

    def deselect(self):

        if self._is_selected and self._scene is not None:
            self._is_selected = False
            self._scene._deselect_item(self)

    ##############################################

    def distance(self, point):
        raise NotImplementedError

    ##############################################

    # mouse and keyboards events

####################################################################################################

def point_interval(x, y):
    return IntervalInt2D((x, x), (y, y))

def centred_interval(x, y, radius):
    return point_interval(x, y).enlarge(radius)

####################################################################################################

class GraphicScene(object):

    ITEM_SELECTION_RADIUS = 2 # px

    _logger = _module_logger.getChild('GraphicScene')

    ##############################################

    def __init__(self):

        self._items = OrderedDict()
        self._rtree = Rtree()
        self._selected_items = OrderedDict()

    ##############################################

    def add_item(self, item):

        item_id = item._id
        self._items[item_id] = item
        self._rtree.add(item_id, item.bounding_box)
        item._scene = self

    ##############################################

    def remove_item(self, item):

        if item in self._selected_items:
            item.deselect()
        
        item_id = item._id
        del self._items[item_id]
        self._rtree.delete(item_id, item.bounding_box)
        item._scene = None

    ##############################################

    def add_items(self, items):

        for item in items:
            self.add_item(item)

    ##############################################

    def remove_items(self, items):

        for item in items:
            self.remove_item(item)

    ##############################################

    def items_in(self, interval):

        items = [self._items[x] for x in self._rtree.intersection(interval.bounding_box())]
        items.sort() # accordind to z value

        return items

    ##############################################

    def items_at(self, x, y):

        # Fixme: vector or x, y
        return self.items_in(point_interval(x, y))

    ##############################################

    def items_around(self, x, y, radius):

        return self.items_in(centred_interval(x, y, radius))

    ##############################################

    def __iter__(self):

        return iter(self._items.values())

    ##############################################

    def _select_item(self, item):

        self._selected_items[item._id] = self

    ##############################################

    def _deselect_item(self, item):

        del self._selected_items[item._id]

    ##############################################

    def iter_on_selected_items(self):

        return self._selected_items.values()

    ##############################################

    def erase(self, position, radius):

        removed_items = []
        new_items = []
        for item in self:
        # for path in self.items_around(position.x, position.y, radius):
            # erase return None, the item or an iterable of new items
            items = item.erase(position, radius)
            if items is not item:
                self._logger.info("Erase item {}".format(item.id))
                removed_items.append(item)
                if items is not None:
                    new_items.extend(items)
        self.remove_items(removed_items)
        self.add_items(new_items)
        
        return removed_items, new_items

####################################################################################################
#
# End
#
####################################################################################################
