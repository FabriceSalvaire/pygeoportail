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

import asyncio
import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from quamash import QEventLoop, QThreadExecutor

####################################################################################################

from PyOpenGLng.HighLevelApi import GL
from PyOpenGLng.HighLevelApi.GlWidgetBase import GlWidgetBase
from PyOpenGLng.HighLevelApi.TextureVertexArray import GlTextureVertexArray
from PyOpenGLng.Math.Geometry import Point, Offset

####################################################################################################

from .Painter import Painter
from PyGeoPortail.GraphicEngine.ShaderProgrames import texture_shader_program_interface
from PyGeoPortail.TileMap.LruCache import LruCache
from PyGeoPortail.TileMap.TileCache import Tile
from PyGeoPortail.Tools.ListArithmetic import split_list

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Texture(GlTextureVertexArray):

    _logger = _module_logger.getChild('Texture')

    ##############################################

    def __init__(self, key, position, dimension, image):

        GlTextureVertexArray.__init__(self, position, dimension, image)
        
        self._key = key
        self._size = image.nbytes

    ##############################################

    def free(self):

        # self._logger.debug('')
        pass

    ##############################################

    def __repr__(self):

        return 'TextureCache {}'.format(self._key)

    ##############################################

    def key(self):

        return self._key

    ##############################################

    def size(self):

        return self._size

####################################################################################################

class MosaicPainter(Painter):

    __painter_name__ = 'mosaic'

    _logger = _module_logger.getChild('MosaicPainter')

    ##############################################

    def __init__(self, painter_manager, cached_pyramid, z_value=0, status=True, name=None):

        super(MosaicPainter, self).__init__(painter_manager, z_value, status, name)
        
        self._cached_pyramid = cached_pyramid # Fixme: mosaic / pyramid ?
        self._texture_cache = LruCache(constraint=1024**2) # Fixme
        
        self._viewport_area = self._glwidget.glortho2d.viewport_area
        self._shader_program = self._glwidget.shader_manager.texture_shader_program
        
        self._level = 16
        self._tile_list = []
        self._textures = []
        self._texture_dict = {}
        
        application = QtWidgets.QApplication.instance()
        self._loop = asyncio.get_event_loop()
        # self._loop = QEventLoop(application)
        # asyncio.set_event_loop(self._loop)

        # self._loop.close()

    ##############################################

    @property
    def texture_cache(self):

        return self._texture_cache

    ##############################################

    def reset(self):

        self._texture_cache.reset()

    ##############################################

    def recycle(self):

        # self._logger.debug('Recycle Mosaic Cache')
        # self._mosaic_cache.recycle()

        # self._logger.debug('Recycle OpenGL Cache')
        line = '-'*50 + '\n'
        text = """
Texture Cache: recycle
  before
"""
        text += str(self._texture_cache)
        self._texture_cache.recycle()
        text += '\n  after\n' + str(self._texture_cache) + '\n' + line
        self._logger.debug(text)

    ##############################################

    # def zoom_layer_changed(self, zoom_layer):
    #
    #     pass

    ##############################################

    def update(self):

        self._logger.debug('Update Mosaic Painter')
        
        texture_cache = self._texture_cache
        cached_pyramid = self._cached_pyramid
        
        # always compute tile list
        old_tile_list = self._tile_list
        pyramid_level = self._cached_pyramid._pyramid[self._level] # Fixme: zoom -> level
        mosaic_interval = pyramid_level.projection_interval_to_mosaic(self._viewport_area.area)
        self._tile_list = list(mosaic_interval.iter())
        self._logger.debug('Viewport\n' + str(self._tile_list))
        (tiles_to_release,
         tiles_to_keep,
         tiles_to_acquire) = split_list(old_tile_list, self._tile_list)
        
        # Reset
        self._textures = []
        print(self._texture_dict)
        for tile_index in tiles_to_keep:
            row, column = tile_index
            key = Tile.tile_key(0, self._level, row, column)
            self._textures.append(self._texture_dict[key])
        self._glwidget.update()
        
        # Get new tiles
        if tiles_to_acquire:
            tasks = [asyncio.async(cached_pyramid.acquire(self._level, row, column))
                     for row, column in tiles_to_acquire]
            # for task in tasks:
            #     task.add_done_callback(self._task_callback)
            self._logger.debug('Run loop')
            #!# with self._loop:
            self._loop.run_until_complete(asyncio.wait(tasks))
            self._logger.debug('loop done')
            for task in tasks:
                self._task_callback(task)
        
        # Recycle the cache
        for tile_index in tiles_to_release:
            # Fixme: key
            row, column = tile_index
            cached_pyramid.release(self._level, row, column)
            key = Tile.tile_key(0, self._level, row, column)
            texture_cache.release(key)
        self.recycle()
        
        self._texture_dict = {texture.key():texture for texture in self._textures}
        
        self._logger.debug('Update Mosaic Painter Done')

    ##############################################

    def _task_callback(self, task):

        tile = task.result()
        
        key = Tile.tile_key(0, self._level, tile.row, tile.column)
        texture = self._texture_cache.acquire(key)
        if texture is None:
            texture = self._create_texture(tile, key)
        self._textures.append(texture)
        self._glwidget.update()

    ##############################################

    def _create_texture(self, tile, key):

        self._logger.debug('Create Texture ' + str(key))
        position = Point(tile.x, tile.y+tile.length)
        image_dimension = Offset(tile.length, -tile.length)
        self._glwidget.makeCurrent() #?
        with GL.error_checker():
            texture = Texture(key, position, image_dimension, tile.image)
            texture.bind_to_shader(texture_shader_program_interface.attributes)
        self._texture_cache.add(texture, acquire=True)
        
        return texture

    ##############################################

    def paint(self):

        self._logger.debug('Paint')
        self._shader_program.bind()
        for texture in self._textures:
            texture.draw()

####################################################################################################
#
# End
#
####################################################################################################
