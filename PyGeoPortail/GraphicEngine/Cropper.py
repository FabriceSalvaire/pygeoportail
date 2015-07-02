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

from PyQt5 import QtWidgets

####################################################################################################

from .GraphicScene import GraphicSceneItem
from PyGeoPortail.Math.Interval import IntervalInt2D
from PyGeoPortail.Tools.ConstrainedBox import ConstrainedBox
from PyGeoPortail.Tools.EnumFactory import EnumFactory

####################################################################################################

grip_enum = EnumFactory('GripEnum',
                         ('s',
                          'n',
                          'w',
                          'e',
                          'sw',
                          'nw',
                          'se',
                          'ne',
                          'box', # Fixme: purpose, inner or outer box ?
                          'center',
                          ))

####################################################################################################

class Grip(GraphicSceneItem):

    _logger = logging.getLogger(__name__)

    # Fixme: shader rescale the margin in px, thus this code only works fo zoom 1:1 !
    #   we could test (point + rescaled margin) & inner_box
    margin = 20

    ##############################################

    def __init__(self, cropper, position):

        self._cropper = cropper
        self._position = position
        inner_box = self._cropper._interval
        
        # Fixme: recomputed for each grip
        outer_box = inner_box.copy()
        outer_box.enlarge(self.margin)
        center_box = inner_box.copy()
        center_box.enlarge(-self.margin)
        # Fixme: margin
        # margin_x, margin_y = [int(.05*x) for x in inner_box.size()]
        margin_x = margin_y = self.margin
        
        if position == grip_enum.nw:
            interval = IntervalInt2D((outer_box.x.inf, inner_box.x.inf),
                                     (inner_box.y.sup, outer_box.y.sup))
        elif position == grip_enum.n:
            interval = IntervalInt2D((inner_box.x.inf + margin_x, inner_box.x.sup - margin_x),
                                     (inner_box.y.sup, outer_box.y.sup))
        elif position == grip_enum.ne:
            interval = IntervalInt2D((inner_box.x.sup, outer_box.x.sup),
                                     (inner_box.y.sup, outer_box.y.sup))
        elif position == grip_enum.e:
            interval = IntervalInt2D((inner_box.x.sup, outer_box.x.sup),
                                     (inner_box.y.inf + margin_y, inner_box.y.sup - margin_y))
        elif position == grip_enum.se:
            interval = IntervalInt2D((inner_box.x.sup, outer_box.x.sup),
                                     (outer_box.y.inf, inner_box.y.inf))
        elif position == grip_enum.s:
            interval = IntervalInt2D((inner_box.x.inf + margin_x, inner_box.x.sup - margin_x),
                                     (outer_box.y.inf, inner_box.y.inf))
        elif position == grip_enum.sw:
            interval = IntervalInt2D((outer_box.x.inf, inner_box.x.inf),
                                     (outer_box.y.inf, inner_box.y.inf))
        elif position == grip_enum.w:
            interval = IntervalInt2D((outer_box.x.inf, inner_box.x.inf),
                                     (inner_box.y.inf + margin_y, inner_box.y.sup - margin_y))
        elif position == grip_enum.box:
            interval = inner_box # Fixme: purpose, outer_box ?
        elif position == grip_enum.center:
            interval = center_box
        # self._logger.debug("Grip " + str(position) + " " + str(interval))
        
        if position == grip_enum.box:
            z_value = 0
        else:
            z_value = 1
        
        super(Grip, self).__init__(interval, z_value)

    ##############################################

    @property
    def position(self):

        return self._position

    ##############################################

    def mousePressEvent(self, event):

        self._logger.debug(str(self._position))
        if self._position != grip_enum.box:
            self._cropper.update_from_grip(self, event)

    ##############################################

    def mouseReleaseEvent(self, event):

        self._logger.debug(str(self._position))
        if self._position != grip_enum.box:
            self._cropper.end(event)

####################################################################################################

class MovingBox(object):

    ##############################################

    def __init__(self, interval, point):

        self._interval = interval
        self._point = point
        self._translation = None

    ##############################################

    @property
    def interval(self):

        if self._translation is not None:
            return self._interval + self._translation
        else:
            return self._interval

    ##############################################

    def move(self, point):

        # Fixme: design, return translated interval ?
        self._translation = point - self._point

####################################################################################################

class Cropper(object):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, glwidget):

        self._glwidget = glwidget
        self._roi_painter = glwidget._painter_manager['roi']
        
        self._locked = False
        self._updating = False
        self._scene_items = []
        # self.reset()

    ##############################################

    @property
    def interval(self):

        return self._interval

    ##############################################

    @interval.setter
    def interval(self, interval):

        self._logger.debug("Set bounding box")
        self._interval = interval.copy()
        self._update_painter()

    ##############################################

    def _update_painter(self):

        self._roi_painter.update_bounding_box(self._interval)
        if self._roi_painter.paint_box:
            self._glwidget.update() # updateGL

    ##############################################

    def disable(self):

        self._logger.debug("Disable")
        self._roi_painter.status = False
        self._roi_painter.paint_box = False
        self._roi_painter.paint_grips = False
        self._glwidget.update() # updateGL

    ##############################################

    def enable(self, paint_grips=True): # False

        self._logger.debug("Enable")
        self._roi_painter.status = True
        self._roi_painter.paint_box = True
        self._roi_painter.paint_grips = paint_grips
        self._glwidget.update() # updateGL

    ##############################################

    def reset(self):

        self._logger.debug("Reset")
        self.disable()
        self._roi_painter.update_bounding_box(None)
        self._constrained_box = None
        self._interval = None
        self._reset_grips()

    ##############################################

    def _reset_grips(self):

        for scene_item in self._scene_items:
            self._glwidget.scene.remove_item(scene_item)
        self._scene_items = []

    ##############################################

    def _set_grips(self):

        self._reset_grips()

        # Fixme: enum iterator
        self._scene_items = [Grip(self, position) for position in (grip_enum.sw,
                                                                   grip_enum.nw,
                                                                   grip_enum.se,
                                                                   grip_enum.ne,
                                                                   grip_enum.s,
                                                                   grip_enum.n,
                                                                   grip_enum.w,
                                                                   grip_enum.e,
                                                                   grip_enum.box,
                                                                   grip_enum.center)]
        
        for scene_item in self._scene_items:
            self._glwidget.scene.add_item(scene_item)

    ##############################################

    def _show_locked_warning_message(self):

        application = QtWidgets.QApplication.instance()
        application.show_message("You can't modify the ROI Box!")

    ##############################################

    def begin(self, event):

        # Fixme: mousePressEvent

        if self._locked:
            self._show_locked_warning_message()
            return
        
        self._logger.debug("Begin Crop")
        self.reset()
        x, y = self._glwidget.window_to_gl_coordinate(event)
        self._constrained_box = ConstrainedBox(x1=x, y1=y)
        self._updating = True

    ##############################################

    def _update_constrained_box(self, event):

        point = self._glwidget.window_to_gl_coordinate(event)
        if isinstance(self._constrained_box, MovingBox):
            self._constrained_box.move(point)
        else:
            self._constrained_box.set_p2(point.x, point.y) # Fixme: pass point ?
        self._interval = self._constrained_box.interval
        self._update_painter()

    ##############################################

    def update(self, event):

        # Fixme: mouseMoveEvent

        if not self._updating:
            return
        
        if self._locked:
            self._show_locked_warning_message()
            return
        
        self._logger.debug("Update Crop")
        self.enable()
        self._update_constrained_box(event)
        self._updating = True

    ##############################################

    def end(self, event):

        # Fixme: mouseReleaseEvent

        if not self._updating:
            return
        
        if self._locked:
            self._show_locked_warning_message()
            return
        
        self._logger.debug("End Crop")
        self._update_constrained_box(event)
        self._updating = False
        
        self.disable()
        self._set_grips()
        self.enable()
        
        self._glwidget.update() # updateGL

    ##############################################

    def update_from_grip(self, grip, event):

        self._logger.debug("Update from grip")

        #    | x.inf | y.inf | x.sup | y.sup |
        # nw |   f   |   c   |   c   |   f   |
        # n  |   c   |   c   |   c   |   f   |
        # ne |   c   |   c   |   f   |   f   |
        # e  |   c   |   c   |   f   |   c   |
        # se |   c   |   f   |   f   |   c   |
        # s  |   c   |   f   |   c   |   c   |
        # sw |   f   |   f   |   c   |   c   |
        # w  |   f   |   c   |   c   |   c   |

        x, y = self._interval.x, self._interval.y
        interval = self._interval
        self.reset() # Fixme: check action
        
        if grip.position == grip_enum.nw:
            self._constrained_box = ConstrainedBox(x1=x.sup, y1=y.inf)
        elif grip.position == grip_enum.n:
            self._constrained_box = ConstrainedBox(x1=x.inf, y1=y.inf, x2=x.sup)
        elif grip.position == grip_enum.ne:
            self._constrained_box = ConstrainedBox(x1=x.inf, y1=y.inf)
        elif grip.position == grip_enum.e:
            self._constrained_box = ConstrainedBox(x1=x.inf, y1=y.inf, y2=y.sup)
        elif grip.position == grip_enum.se:
            self._constrained_box = ConstrainedBox(x1=x.inf, y1=y.sup)
        elif grip.position == grip_enum.s:
            self._constrained_box = ConstrainedBox(x1=x.sup, y1=y.sup, x2=x.inf)
        elif grip.position == grip_enum.sw:
            self._constrained_box = ConstrainedBox(x1=x.sup, y1=y.sup)
        elif grip.position == grip_enum.w:
            self._constrained_box = ConstrainedBox(x1=x.sup, y1=y.sup, y2=y.inf)
        elif grip.position == grip_enum.center:
            # Fixme: overwrite qt event -> gl coordinate
            point = self._glwidget.window_to_gl_coordinate(event)
            self._constrained_box = MovingBox(interval, point)
        
        self._updating = True
        self.update(event)

####################################################################################################
#
# End
#
####################################################################################################
