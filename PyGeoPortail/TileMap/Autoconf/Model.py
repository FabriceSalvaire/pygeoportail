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

import json

####################################################################################################

class JsonEncoder(json.JSONEncoder):

    ##############################################

    def default(self, obj):

        if isinstance(obj, JsonAble):
            return obj.__json_interface__

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

####################################################################################################

class JsonAble(object):

    """This class implements a mixin for object which wan be converted to JSON."""

    ##############################################

    # def _jsonify(self, value):

    #     if isinstance(value, list):
    #         return [self._jsonify(x) for x in value]
    #     elif isinstance(value, JsonAble):
    #         return value.to_dict()
    #     else:
    #         return value

    ##############################################

    # def to_dict(self):

    #     d = {}
    #     for key, value in self.__dict__.items():
    #         d[key] = self._jsonify(value)
    #     return d

    ##############################################

    @property
    def __json_interface__(self):
        return self.__dict__

    ##############################################

    def to_json(self):

        kwargs = dict(cls=JsonEncoder, indent=2, ensure_ascii=False, sort_keys=True)
        return json.dumps(self, **kwargs)

####################################################################################################

class Autoconf(JsonAble):

    ##############################################

    def __init__(self, general, layer_list):

        self.general = general
        self.layer_list = layer_list

####################################################################################################

class General(JsonAble):

    ##############################################

    def __init__(self, window, bounding_box, title, extension):

        self.window = window
        self.bounding_box = bounding_box
        self.title = title
        self.extension = extension

####################################################################################################

class Extension(JsonAble):

    ##############################################

    def __init__(self,
                 theme, default_GMLGFI_style_url, territories, tile_matrix_sets, resolutions, services):

        self.theme = theme
        self.default_GMLGFI_style_url = default_GMLGFI_style_url
        self.territories = territories
        self.tile_matrix_sets = tile_matrix_sets
        self.resolutions = resolutions
        self.services = services

####################################################################################################

class Territory(JsonAble):

    ##############################################

    def __init__(self,
                 default, id_, name,
                 default_crs, additional_crs,
                 bounding_box,
                 min_scale_denominator, max_scale_denominator,
                 resolution,
                 center,
                 default_layers):

        self.default = default
        self.id = id_
        self.name = name
        self.default_crs = default_crs
        self.additional_crs = additional_crs
        self.bounding_box = bounding_box
        self.min_scale_denominator = min_scale_denominator
        self.max_scale_denominator = max_scale_denominator
        self.resolution = resolution
        self.center = center
        self.default_layers = default_layers

####################################################################################################

class TileMatrixSet(JsonAble):

    ##############################################

    def __init__(self, identifier, supported_crs, tile_matrices):

        self.identifier = identifier
        self.supported_crs = supported_crs
        self.tile_matrices = tile_matrices

####################################################################################################

class TileMatrix(JsonAble):

    ##############################################

    def __init__(self,
                 identifier, scale_denominator, top_left_corner,
                 tile_width, tile_height, matrix_width, matrix_height):

        self.identifier = identifier
        self.scale_denominator = scale_denominator
        self.top_left_corner = top_left_corner
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.matrix_width = matrix_width
        self.matrix_height = matrix_height

####################################################################################################

class Server(JsonAble):

    ##############################################

    def __init__(self, service, title, version, href):

        self.service = service
        self.title = title
        self.version = version
        self.href = href

####################################################################################################

class Format(JsonAble):

    ##############################################

    def __init__(self, current, name):

        self.current = current
        self.name = name

####################################################################################################

class Style(JsonAble):

    ##############################################

    def __init__(self, current, name, title):

        self.current = current
        self.name = name
        self.title = title

####################################################################################################

class Dimension(JsonAble):

    ##############################################

    def __init__(self,
                 name, unit_symbol, units, user_value,
                 value):

        self.name = name
        self.unit_symbol = unit_symbol
        self.units = units
        self.user_value = user_value
        self.value = value

####################################################################################################

class Legend(JsonAble):

    ##############################################

    def __init__(self, min_scale_denominator, url):

        self.min_scale_denominator = min_scale_denominator
        self.url = url

####################################################################################################

class Constraint(JsonAble):

    ##############################################

    def __init__(self, crs, bounding_box, min_scale_denominator, max_scale_denominator):

        self.crs = crs
        self.bounding_box = bounding_box
        self.min_scale_denominator = min_scale_denominator
        self.max_scale_denominator = max_scale_denominator

####################################################################################################

class Originator(JsonAble):

    ##############################################

    def __init__(self,
                 name,
                 attribution, logo, url, constraints):

        self.name = name
        self.attribution = attribution
        self.logo = logo
        self.url = url
        self.constraints = constraints

####################################################################################################

class Key(JsonAble):

    ##############################################

    def __init__(self, id_, url):

        self.id = id_
        self.url = url

####################################################################################################

class Layer(JsonAble):

    ##############################################

    def __init__(self,
                 hidden, queryable,
                 server, name, title, abstract,
                 min_scale_denominator, max_scale_denominator,
                 srs,
                 format_list, style_list, dimension_list, extension):

        self.hidden = hidden
        self.queryable = queryable
        self.server = server
        self.name = name
        self.title = title
        self.abstract = abstract
        self.min_scale_denominator = min_scale_denominator
        self.max_scale_denominator = max_scale_denominator
        self.format_list = format_list
        self.style_list = style_list
        self.dimension_list = dimension_list
        self.extension = extension
        self.srs = srs

####################################################################################################

class TileMatrixSetLink(JsonAble):

    ##############################################

    def __init__(self, name, limits):

        self.name = name
        self.limits = limits

####################################################################################################

class TileMatrixLimits(JsonAble):

    ##############################################

    def __init__(self, level, min_tile_row, max_tile_row, min_tile_col, max_tile_col):

        self.level = level
        self.min_tile_row = min_tile_row
        self.max_tile_row = max_tile_row
        self.min_tile_col = min_tile_col
        self.max_tile_col = max_tile_col

####################################################################################################

class ExtensionLayer(JsonAble):

    ##############################################

    def __init__(self,
                 id_,
                 constraints, thematics, inspire_thematics,
                 bounding_box, additional_crs, originators, legends,
                 quicklook, tile_matrix_set_link, metadata_url, keys):

        self.id = id_
        self.constraints = constraints
        self.thematics = thematics
        self.inspire_thematics = inspire_thematics
        self.bounding_box = bounding_box
        self.additional_crs = additional_crs
        self.originators = originators
        self.legends = legends
        self.quicklook = quicklook
        self.tile_matrix_set_link = tile_matrix_set_link
        self.metadata_url = metadata_url
        self.keys = keys

####################################################################################################

class Window(JsonAble):

    ##############################################

    def __init__(self, width, height):

        self.width = width
        self.height = height

####################################################################################################

class BoundingBox(JsonAble):

    ##############################################

    def __init__(self, srs, x_min, y_min, x_max, y_max):

        self.srs = srs
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

####################################################################################################

class Center(JsonAble):

    ##############################################

    def __init__(self, x, y):

        self.x = x
        self.y = y

####################################################################################################
#
# End
#
####################################################################################################
