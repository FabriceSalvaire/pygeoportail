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

class AutoConf(JsonAble):

    ##############################################

    def __init__(self):

        self.general = General()
        self.layer_list = []

####################################################################################################

class General(JsonAble):

    ##############################################

    def __init__(self):

        self.window = None
        self.bounding_box = None
        self.title = None
        self.extension = Extension()

####################################################################################################

class Extension(JsonAble):

    ##############################################

    def __init__(self):

        self.theme = None
        self.defaultGMLGFIStyleUrl = None
        self.territories = []
        self.tile_matrix_sets = []
        self.resolutions = None
        self.services = []

####################################################################################################

class Territory(JsonAble):

    ##############################################

    def __init__(self):

        self.default = None
        self.id = None
        self.name = None
        self.default_crs = None
        self.additional_crs = []
        self.bounding_box = None
        self.min_scale_denominator = None
        self.max_scale_denominator = None
        self.resolution = None
        self.center = None
        self.default_layers = []

####################################################################################################

class TileMatrixSet(JsonAble):

    ##############################################

    def __init__(self):

        self.identifier = None
        self.supported_crs = None
        self.tile_matrices = []

####################################################################################################

class TileMatrix(JsonAble):

    ##############################################

    def __init__(self):

        self.identifier = None
        self.scale_denominator = None
        self.top_left_corner = None
        self.tile_width = None
        self.tile_height = None
        self.matrix_width = None
        self.matrix_height = None

####################################################################################################

class Server(JsonAble):

    ##############################################

    def __init__(self):

        self.service = None
        self.title = None
        self.version = None
        self.href = None

####################################################################################################

class Format(JsonAble):

    ##############################################

    def __init__(self):

        self.current = None
        self.name = None

####################################################################################################

class Style(JsonAble):

    ##############################################

    def __init__(self):

        self.current = None
        self.name = None
        self.title = None

####################################################################################################

class Dimension(JsonAble):

    ##############################################

    def __init__(self):

        self.name = None
        self.unit_symbol = None
        self.units = None
        self.user_value = None
        self.value = None

####################################################################################################

class Legend(JsonAble):

    ##############################################

    def __init__(self):

        self.min_scale_denominator = None
        self.url = None

####################################################################################################

class Constraint(JsonAble):

    ##############################################

    def __init__(self):

        self.crs = None
        self.bounding_box = None
        self.min_scale_denominator = None
        self.max_scale_denominator = None

####################################################################################################

class Originator(JsonAble):

    ##############################################

    def __init__(self):

        self.name = None
        self.attribution = None
        self.url = None
        self.constraints = []

####################################################################################################

class Key(JsonAble):

    ##############################################

    def __init__(self):

        self.id = None
        self.url = None

####################################################################################################

class Layer(JsonAble):

    ##############################################

    def __init__(self):

        self.hidden = None
        self.queryable = None
        self.server = None
        self.name = None
        self.title = None
        self.abstract = None
        self.min_scale_denominator = None
        self.max_scale_denominator = None
        self.format_list = []
        self.style_list = []
        self.dimension_list = []
        self.extension = None
        self.srs = None

####################################################################################################

class TileMatrixSetLink(JsonAble):

    ##############################################

    def __init__(self):

        self.name = None
        self.limits = []

####################################################################################################

class TileMatrixLimits(JsonAble):

    ##############################################

    def __init__(self):

        self.level = None
        self.min_tile_row = None
        self.max_tile_row = None
        self.min_tile_col = None
        self.max_tile_col = None

####################################################################################################

class ExtensionLayer(JsonAble):

    ##############################################

    def __init__(self):

        self.id = None
        self.constraints = []
        self.thematics = []
        self.inspire_thematics = []
        self.bounding_box = None
        self.additional_crs = []
        self.originators = []
        self.legends = []
        self.quicklook = None
        self.tile_matrix_set_link = None
        self.metadata_url = None
        self.keys = []

####################################################################################################
#
# End
#
####################################################################################################
