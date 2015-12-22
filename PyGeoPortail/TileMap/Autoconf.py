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

from PyQt5.QtCore import QXmlStreamReader

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

class AutoConfParser(object):

    ##############################################

    def __init__(self):

        self._xml_parser = None

    ##############################################

    def _raise(self):

        xml_parser = self._xml_parser
        raise NameError('@{} {} {}'.format(xml_parser.lineNumber(), xml_parser.tokenString(), xml_parser.name()))

    ##############################################

    def _read_match_start_element(self, name):

        xml_parser = self._xml_parser
        return (xml_parser.readNext() == QXmlStreamReader.StartElement
                and xml_parser.name() == name)

    ##############################################

    def _read_match_end_element(self, name):

        xml_parser = self._xml_parser
        return (xml_parser.readNext() == QXmlStreamReader.EndElement
                and xml_parser.name() == name)

    ##############################################

    def _match_start_element(self, name):

        xml_parser = self._xml_parser
        return (xml_parser.tokenType() == QXmlStreamReader.StartElement
                and xml_parser.name() == name)

    ##############################################

    def _match_end_element(self, name):

        xml_parser = self._xml_parser
        return (xml_parser.tokenType() == QXmlStreamReader.EndElement
                and xml_parser.name() == name)

    ##############################################

    def _read_match_empty(self):

        xml_parser = self._xml_parser
        return (xml_parser.readNext() == QXmlStreamReader.Characters
                and xml_parser.isWhitespace())

    ##############################################

    def _match_empty(self):

        xml_parser = self._xml_parser
        return (xml_parser.tokenType() == QXmlStreamReader.Characters
                and xml_parser.isWhitespace())

    ##############################################

    def _read_until_start_of(self, name):

        xml_parser = self._xml_parser
        while not (xml_parser.readNext() == QXmlStreamReader.StartElement
                   and xml_parser.name() == name):
            pass

    ##############################################

    def _read_until_end_of(self, name):

        xml_parser = self._xml_parser
        while not (xml_parser.readNext() == QXmlStreamReader.EndElement
                   and xml_parser.name() == name):
            pass

    ##############################################

    def _read_until_empty(self):

        xml_parser = self._xml_parser
        while (xml_parser.readNext() == QXmlStreamReader.Characters
               and xml_parser.isWhitespace()):
            pass

    ##############################################

    def _attribute_to_dict(self, *keys):

        attributes = self._xml_parser.attributes()
        return {key:attributes.value(key) for key in keys}

    ##############################################

    def _read_text(self, name):

        # start must be read
        xml_parser = self._xml_parser
        if self._xml_parser.readNext() == QXmlStreamReader.Characters:
            text = xml_parser.text()
        else:
            self._raise()
        if self._read_match_end_element(name):
            return text
        else:
            self._raise()

    ##############################################

    def _read_int(self, name):

        return int(self._read_text(name))

    ##############################################

    def _read_float(self, name):

        return float(self._read_text(name))

    ##############################################

    def _read_int_list(self, name, sep=','):

        return [int(x) for x in self._read_text(name).split(sep)]

    ##############################################

    def _read_float_list(self, name, sep=','):

        return [float(x) for x in self._read_text(name).split(sep)]

    ##############################################

    def parse_document(self, xml_document):

        # <?xml version="1.0" encoding="UTF-8"?>
        # <ViewContext
        #     xmlns="http://www.opengis.net/context"
        #     xmlns:gpp="http://api.ign.fr/geoportail"
        #     xmlns:ows="http://www.opengis.net/ows/1.1"
        #     xmlns:sld="http://www.opengis.net/sld"
        #     xmlns:wmts="http://www.opengis.net/wmts/1.0"
        #     xmlns:xlink="http://www.w3.org/1999/xlink"
        #     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        #     id="autoConf"
        #     version="1.1.0"
        #     xsi:schemaLocation="http://www.opengis.net/context
        #                         http://gpp3-wxs.ign.fr/schemas/extContext.xsd
        #                         http://api.ign.fr/geoportail
        #                         http://wxs.ign.fr/schemas/autoconf/autoconf.xsd">
        #   <General> ...  </General>
        #   <LayerList> ...  </LayerList>
        # </ViewContext>

        self._xml_parser = QXmlStreamReader(xml_document)
        # xml_parser.setDevice(xml_document)
        
        autoconf = AutoConf()
        if self._xml_parser.readNext() != QXmlStreamReader.StartDocument:
            self._raise()
        if not self._read_match_start_element('ViewContext'):
            self._raise()
        while not self._read_match_end_element('ViewContext'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'General':
                    self._parse_General(autoconf.general)
                elif name == 'LayerList':
                    self._parse_LayerList(autoconf.layer_list)
                else:
                    self._raise()
            # else
            # or match end and
            # elif not self._match_empty():
            #     self._raise()
        if self._xml_parser.readNext() != QXmlStreamReader.EndDocument:
            self._raise()
        
        self._xml_parser = None
        
        return autoconf

    ##############################################

    def _parse_General(self, general):

        # <General>
        #   <Window height="300" width="500"/>
        #   <BoundingBox SRS="EPSG:4326" maxx="180.0" maxy="90.0" minx="-90.0" miny="-180.0"/>
        #   <Title>Service d'autoconfiguration des API</Title>
        #   <Extension>
        # </General>

        # dispatched
        while not self._read_match_end_element('General'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Window':
                    self._parse_Window(general)
                elif name == 'BoundingBox':
                    self._parse_BoundingBox(general)
                elif name == 'Title':
                    self._parse_Title(general)
                elif name == 'Extension':
                    self._parse_Extension(general.extension)
                else:
                    self._raise()
            # else

    ##############################################

    def _parse_Window(self, general):

        # <Window height="300" width="500"/>

        # dispatched
        attr = self._attribute_to_dict('height', 'width')
        general.window = {key:int(value) for key, value in attr.items()}

    ##############################################

    def _parse_BoundingBox(self, general):

        # <BoundingBox SRS="EPSG:4326" maxx="180.0" maxy="90.0" minx="-90.0" miny="-180.0"/>

        # dispatched
        general.bounding_box = self._attribute_to_dict('SRS', 'maxx', 'maxy', 'minx', 'miny')

    ##############################################

    def _parse_Title(self, general):

        # <Title>Service d'autoconfiguration des API</Title>

        # dispatched
        general.title = self._read_text('Title')

    ##############################################

    def _parse_Extension(self, extension):

        # <Extension>
        #   <gpp:General>
        #     <gpp:Theme>default</gpp:Theme>
        #     <gpp:defaultGMLGFIStyleUrl>http://wxs.ign.fr/static/style_wms_getfeatureinfo/default.xsl</gpp:defaultGMLGFIStyleUrl>
        #     <gpp:Territories> ... </gpp:Territories>
        #     <gpp:TileMatrixSets> ... </gpp:TileMatrixSets>
        #     <gpp:Resolutions> ... </gpp:Resolutions>
        #     <gpp:Services>
        #     </gpp:Services>
        #   </gpp:General>
        # </Extension>

        # dispatched
        # gpp:
        self._read_until_empty()
        if not self._match_start_element('General'):
            self._raise()
        
        while not self._read_match_end_element('General'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement:
                name = self._xml_parser.name()
                if name == 'Theme':
                    extension.theme = self._read_text('Theme')
                elif name == 'defaultGMLGFIStyleUrl':
                    extension.defaultGMLGFIStyleUrl = self._read_text('defaultGMLGFIStyleUrl')
                elif name == 'Territories':
                    self._parse_Territories(extension.territories)
                elif name == 'TileMatrixSets':
                    self._parse_TileMatrixSets(extension.tile_matrix_sets)
                elif name == 'Resolutions':
                    extension.resolutions = self._parse_Resolutions()
                elif name == 'Services':
                    self._parse_Services(extension.services)
                else:
                    self._raise()
            # else

        self._read_until_empty()
        if not self._match_end_element('Extension'):
            self._raise()

    ##############################################

    def _parse_Territories(self, territories):

        # <gpp:Territories>
	#   <gpp:Territory default="1" id="FXX" name="FXX"> ... </gpp:Territory>
        # </gpp:Territories>

        # dispatched
        while not self._read_match_end_element('Territories'):
            if self._match_empty():
                continue
            territories.append(self._parse_Territory())

    ##############################################

    def _parse_Territory(self):

	# <gpp:Territory default="1" id="FXX" name="FXX">
	#   <gpp:defaultCRS>EPSG:3857</gpp:defaultCRS>
	#   <gpp:AdditionalCRS>CRS:84</gpp:AdditionalCRS>
	#   <gpp:AdditionalCRS>IGNF:RGF93G</gpp:AdditionalCRS>
        #   ...
        #   <gpp:BoundingBox>-31.17,27.33,69.03,80.83</gpp:BoundingBox>
	#   <sld:MinScaleDenominator>533</sld:MinScaleDenominator>
	#   <sld:MaxScaleDenominator>128209039</sld:MaxScaleDenominator>
	#   <gpp:Resolution>2445.984905</gpp:Resolution>
	#   <gpp:Center> ... </gpp:Center>
	#   <gpp:DefaultLayers> ... </gpp:DefaultLayers>
	# </gpp:Territory>

        if not self._match_start_element('Territory'):
            self._raise()
        
        territory = Territory()
        attr = self._attribute_to_dict('default', 'id', 'name')
        territory.default = attr['default']
        territory.id = attr['id']
        territory.name = attr['name']
        
        while not self._read_match_end_element('Territory'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'defaultCRS':
                    territory.default_crs = self._read_text('defaultCRS')
                elif name == 'AdditionalCRS':
                    territory.additional_crs.append(self._read_text('AdditionalCRS'))
                elif name == 'BoundingBox':
                    territory.bounding_box = self._read_float_list('BoundingBox', sep=',')
                elif name == 'MinScaleDenominator':
                    territory.min_scale_denominator = self._read_float('MinScaleDenominator')
                elif name == 'MaxScaleDenominator':
                    territory.max_scale_denominator = self._read_float('MaxScaleDenominator')
                elif name == 'Resolution':
                    territory.resolution = self._read_float('Resolution')
                elif name == 'Center':
                    territory.center = self._parse_Center()
                elif name == 'DefaultLayers':
                    self._parse_DefaultLayers(territory.default_layers)
                else:
                    self._raise()
            # else
        
        return territory

    ##############################################

    def _parse_Center(self):

	#   <gpp:Center>
	#     <gpp:x>2.345274398</gpp:x>
	#     <gpp:y>48.860832558</gpp:y>
	#   </gpp:Center>

        # dispatched
        while not self._read_match_end_element('Center'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'x':
                    x = self._read_float('x')
                elif name == 'y':
                    y = self._read_float('y')
                else:
                    self._raise()
            # else
        
        return x, y

    ##############################################

    def _parse_DefaultLayers(self, default_layers):

	#   <gpp:DefaultLayers>
	#     <gpp:DefaultLayer layerId="ORTHOIMAGERY.ORTHOPHOTOS$GEOPORTAIL:OGC:WMTS"/>
	#     <gpp:DefaultLayer layerId="GEOGRAPHICALGRIDSYSTEMS.MAPS$GEOPORTAIL:OGC:WMTS"/>
        #     ...
	#   </gpp:DefaultLayers>

        while not self._read_match_end_element('DefaultLayers'):
            if self._match_empty():
                continue
            # if self._xml_parser.isStartElement():
            #     default_layers.append(self._parse_DefaultLayer())
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'DefaultLayer':
                    default_layers.append(self._attribute_to_dict('layerId'))
                else:
                    self._raise()
            # else

    ##############################################

    # def _parse_DefaultLayer(self):

    #     # dispatched
    #     if not self._match_start_element('DefaultLayer'):
    #         self._raise()
    #     default_layer = self._attribute_to_dict('layerId')
    #     if not self._read_match_end_element('DefaultLayer'):
    #         self._raise()
    #     return default_layer

    ##############################################

    def _parse_TileMatrixSets(self, tile_matrix_sets):

	# <gpp:TileMatrixSets>
	#   <wmts:TileMatrixSet> ... </wmts:TileMatrixSet>
        #   ...
        # </gpp:TileMatrixSets>

        while not self._read_match_end_element('TileMatrixSets'):
            if self._match_empty():
                continue
            tile_matrix_sets.append(self._parse_TileMatrixSet())

    ##############################################

    def _parse_TileMatrixSet(self):

	# <wmts:TileMatrixSet>
	#   <ows:Identifier>PM</ows:Identifier>
	#   <ows:SupportedCRS>EPSG:3857</ows:SupportedCRS>
	#   <wmts:TileMatrix> ... </wmts:TileMatrix>
        # ...
        # </wmts:TileMatrixSet>

        if not self._match_start_element('TileMatrixSet'):
            self._raise()
        tile_matrix_set = TileMatrixSet()
        while not self._read_match_end_element('TileMatrixSet'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Identifier':
                    tile_matrix_set.identifier = self._read_text('Identifier')
                elif name == 'SupportedCRS':
                    tile_matrix_set.supported_crs = self._read_text('SupportedCRS')
                elif name == 'TileMatrix':
                    tile_matrix_set.tile_matrices.append(self._parse_TileMatrix())
                else:
                    self._raise()
            # else
        return tile_matrix_set

    ##############################################

    def _parse_TileMatrix(self):

        # <wmts:TileMatrix>
	#   <ows:Identifier>0</ows:Identifier>
	#   <wmts:ScaleDenominator>559082264.0287178958533332</wmts:ScaleDenominator>
	#   <wmts:TopLeftCorner>-20037508 20037508</wmts:TopLeftCorner>
	#   <wmts:TileWidth>256</wmts:TileWidth>
	#   <wmts:TileHeight>256</wmts:TileHeight>
	#   <wmts:MatrixWidth>1</wmts:MatrixWidth>
	#   <wmts:MatrixHeight>1</wmts:MatrixHeight>
	# </wmts:TileMatrix>

        tile_matrix = TileMatrix()
        while not self._read_match_end_element('TileMatrix'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Identifier':
                    tile_matrix.identifier = self._read_int('Identifier')
                elif name == 'ScaleDenominator':
                    tile_matrix.scale_denominator = self._read_float('ScaleDenominator')
                elif name == 'TopLeftCorner':
                    tile_matrix.top_left_corner = self._read_int_list('TopLeftCorner', sep=' ')
                elif name == 'TileWidth':
                    tile_matrix.tile_width = self._read_int('TileWidth')
                elif name == 'TileHeight':
                    tile_matrix.tile_height = self._read_int('TileHeight')
                elif name == 'MatrixWidth':
                    tile_matrix.matrix_width = self._read_int('MatrixWidth')
                elif name == 'MatrixHeight':
                    tile_matrix.matrix_height = self._read_int('MatrixHeight')
                else:
                    self._raise()
            # else
        return tile_matrix

    ##############################################

    def _parse_Resolutions(self):

        return self._read_float_list('Resolutions', sep=',')

    ##############################################

    def _parse_Services(self, services):

	# <gpp:Services>
	#   <Server service="OGC:OPENLS;Geocode" title="Service de Geocodage" version="1.2"> ... </Server>
        #   ...
        # <gpp:Services>

        while not self._read_match_end_element('Services'):
            if self._match_empty():
                continue
            services.append(self._parse_Server())

    ##############################################

    def _parse_Server(self):

	#   <Server service="OGC:OPENLS;Geocode" title="Service de Geocodage" version="1.2">
	#     <OnlineResource xlink:href="http://wxs.ign.fr/geoportail/ols" xlink:type="simple"/>
	#   </Server>

        if not self._match_start_element('Server'):
            self._raise()
        server = Server()
        attr = self._attribute_to_dict('service', 'title', 'version')
        server.service = attr['service']
        server.title = attr['title']
        server.version = attr['version']
        while not self._read_match_end_element('Server'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'OnlineResource':
                    server.href = self._attribute_to_dict('xlink:href')
                else:
                    self._raise()
            # else
        return server

    ##############################################

    def _parse_LayerList(self, layer_list):

        # <LayerList>
        #   <Layer hidden="1" queryable="1"> ... </Layer>
        #   ...
        # </LayerList>

        while not self._read_match_end_element('LayerList'):
            if self._match_empty():
                continue
            layer_list.append(self._parse_Layer())

    ##############################################

    def _parse_Layer(self):

        # <Layer hidden="1" queryable="1">
        #   <Server service="OGC:WMS" title="Monuments nationaux" version="1.3.0"> ... </Server>
        #   <Name>POI.MONUMENTS_BDD_WLD_WM</Name>
        #   <Title>Monuments nationaux</Title>
        #   <Abstract><![CDATA[Le Centre des monuments nationaux ...]]></Abstract>
        #   <sld:MinScaleDenominator>0</sld:MinScaleDenominator>
        #   <sld:MaxScaleDenominator>62236752975597</sld:MaxScaleDenominator>
        #   <SRS>EPSG:4326</SRS>
        #   <FormatList> ... </FormatList>
        #   <StyleList> ... </StyleList>
        #   <DimensionList> ... </DimensionList>
        #   <Extension> ... </Extension>
        # </Layer>

        if not self._match_start_element('Layer'):
            self._raise()
        layer = Layer()
        attr = self._attribute_to_dict('hidden', 'queryable')
        layer.hidden = bool(attr['hidden'])
        layer.queryable = bool(attr['queryable'])
        while not self._read_match_end_element('Layer'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Server':
                    layer.server = self._parse_Server()
                elif name == 'Name':
                    layer.name = self._read_text('Name')
                elif name == 'Title':
                    layer.title = self._read_text('Title')
                elif name == 'Abstract':
                    layer.abstract = self._read_text('Abstract')
                elif name == 'MinScaleDenominator':
                    layer.min_scale_denominator = self._read_float('MinScaleDenominator')
                elif name == 'MaxScaleDenominator':
                    layer.max_scale_denominator = self._read_float('MaxScaleDenominator')
                elif name == 'SRS':
                    layer.srs = self._read_text('SRS')
                elif name == 'FormatList':
                    self._parse_FormatList(layer.format_list)
                elif name == 'StyleList':
                    self._parse_StyleList(layer.style_list)
                elif name == 'DimensionList':
                    self._parse_DimensionList(layer.dimension_list)
                elif name == 'Extension':
                    layer.extension = self._parse_Layer_Extension()
                else:
                    self._raise()
            # else
        return layer

    ##############################################

    def _parse_FormatList(self, format_list):

        # <FormatList>
        #   <Format current="1">text/xml</Format>
        #   ...
        # </FormatList>

        while not self._read_match_end_element('FormatList'):
            if self._match_empty():
                continue
            format_list.append(self._parse_Format())

    ##############################################

    def _parse_Format(self):

        if not self._match_start_element('Format'):
            self._raise()
        format_ = Format()
        attr = self._attribute_to_dict('current')
        format_.current = attr['current']
        format_.name = self._read_text('Format')
        return format_

    ##############################################

    def _parse_StyleList(self, style_list):

        # <StyleList>
        #   <Style current="1"> ... </Style>
        #   ...
        # <StyleList>

        while not self._read_match_end_element('StyleList'):
            if self._match_empty():
                continue
            style_list.append(self._parse_Style())

    ##############################################

    def _parse_Style(self):

        #   <Style current="1">
        #     <Name>normal</Name>
        #     <Title>Données Brutes</Title>
        #   </Style>

        if not self._match_start_element('Style'):
            self._raise()
        style = Style()
        attr = self._attribute_to_dict('current')
        style.current = attr['current']
        while not self._read_match_end_element('Style'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Name':
                    style.name = self._read_text('Name')
                elif name == 'Title':
                    style.title = self._read_text('Title')
                else:
                    self._raise()
            # else
        return style

    ##############################################

    def _parse_DimensionList(self, dimension_list):

      # <DimensionList>
      #   <Dimension name="GeometricType" unitSymbol="" units="" userValue="">-</Dimension>
      # </DimensionList>

        while not self._read_match_end_element('DimensionList'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Dimension':
                    dimension_list.append(self._parse_Dimension())
                else:
                    self._raise()
            # else

    ##############################################

    def _parse_Dimension(self):

        # <Dimension name="GeometricType" unitSymbol="" units="" userValue="">-</Dimension>

        if not self._match_start_element('Dimension'):
            self._raise()
        dimension = Dimension()
        attr = self._attribute_to_dict('name', 'unitSymbol', 'units', 'userValue')
        dimension.name = attr['name']
        dimension.unit_symbol = attr['unitSymbol']
        dimension.units = attr['units']
        dimension.user_value = attr['userValue']
        dimension.value = self._read_text('Dimension')
        return dimension

    ##############################################

    def _parse_Layer_Extension(self):


        # <Extension>
        #   <gpp:Layer id="BDPARCEL_PYR-PNG_WLD$GEOPORTAIL:OGC:WMS">
        #     <gpp:Constraints> ... </gpp:Constraints>
        #     <gpp:Thematics> ... </gpp:Thematics>
        #     <gpp:InspireThematics> ... </gpp:InspireThematics>
        #     <gpp:BoundingBox maxT="2015-08-24" minT="2015-08-24">-63.160706,-21.39223,55.84643,51.090965</gpp:BoundingBox>
        #     <gpp:AdditionalCRS>EPSG:2975</gpp:AdditionalCRS>
        #     <gpp:AdditionalCRS>EPSG:3727</gpp:AdditionalCRS>
        #     ...
        #     <gpp:Originators> ... </gpp:Originators>
        #     <gpp:Legends> ... </gpp:Legends>
        #     <gpp:QuickLook> ... </gpp:QuickLook>
        #     <wmts:TileMatrixSetLink> ... </wmts:TileMatrixSetLink>
        #     <gpp:MetadataURL format="xml"> ... </gpp:MetadataURL>
        #     <gpp:Keys> ... </gpp:Keys>
        #   </gpp:Layer>
        # </Extension>

        if not self._match_start_element('Extension'):
            self._raise()
        self._read_until_empty()
        if not self._match_start_element('Layer'):
            self._raise()
        layer = ExtensionLayer()
        attr = self._attribute_to_dict('id')
        layer.id = bool(attr['id'])
        while not self._read_match_end_element('Layer'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Constraints':
                    self._parse_Constraints(layer.constraints)
                elif name == 'Thematics':
                   self._parse_Thematics(layer.thematics)
                elif name == 'InspireThematics':
                    self._parse_InspireThematics(layer.inspire_thematics)
                elif name == 'BoundingBox':
                    layer.bounding_box = self._parse_LayerBoundingBox()
                elif name == 'AdditionalCRS':
                    layer.additional_crs.append(self._read_text('AdditionalCRS'))
                elif name == 'Originators':
                    self._parse_Originators(layer.originators)
                elif name == 'Legends':
                    self._parse_Legends(layer.legends)
                elif name == 'QuickLook':
                    layer.quicklook = self._parse_Quicklook()
                elif name == 'TileMatrixSetLink':
                    layer.tile_matrix_set_link = self._parse_TileMatrixSetLink()
                elif name == 'MetadataURL':
                    layer.metadata_url = self._parse_OnlineResource() # MetadataURL
                elif name == 'Keys':
                    self._parse_Keys(layer.keys)
                else:
                    self._raise()
            # else
        self._read_until_empty()
        if not self._match_end_element('Extension'):
            self._raise()
        return layer

    ##############################################

    def _parse_Thematics(self, thematics):

        # <gpp:Thematics>
        #   <gpp:Thematic>Parcelles cadastrales</gpp:Thematic>
        # </gpp:Thematics>

        while not self._read_match_end_element('Thematics'):
            if self._match_empty():
                continue
            thematics.append(self._read_text('Thematic'))

    ##############################################

    def _parse_InspireThematics(self, inspire_thematics):

        # <gpp:InspireThematics>
        #   <gpp:InspireThematic>Parcelles cadastrales</gpp:InspireThematic>
        # </gpp:InspireThematics>

        while not self._read_match_end_element('InspireThematics'):
            if self._match_empty():
                continue
            inspire_thematics.append(self._read_text('InspireThematic'))

    ##############################################

    def _parse_LayerBoundingBox(self):

        attr = self._attribute_to_dict('maxT', 'minT')
        max_time = attr['maxT']
        min_time = attr['minT']
        bounding_box = self._read_float_list('BoundingBox', sep=',')
        return bounding_box

    ##############################################

    def _parse_Originators(self, originators):

        # <gpp:Originators>
        #   <gpp:Originator name="IGN"> ... </gpp:Originator>
        # </gpp:Originators>

        while not self._read_match_end_element('Originators'):
            if self._match_empty():
                continue
            originators.append(self._parse_Originator())

    ##############################################

    def _parse_Originator(self):

        # <gpp:Originator name="IGN">
        #   <gpp:Attribution>Institut national de l'information géographique et forestière</gpp:Attribution>
        #   <gpp:Logo>http://wxs.ign.fr/static/logos/IGN/IGN.gif</gpp:Logo>
        #   <gpp:URL>http://www.ign.fr</gpp:URL>
        #   <gpp:Constraints> ... </gpp:Constraints>
        # </gpp:Originator>

        if not self._match_start_element('Originator'):
            self._raise()
        originator = Originator()
        attr = self._attribute_to_dict('name')
        originator.name = attr['name']
        while not self._read_match_end_element('Originator'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Attribution':
                    originator.attribution = self._read_text('Attribution')
                elif name == 'Logo':
                    originator.logo = self._read_text('Logo')
                elif name == 'URL':
                    originator.url = self._read_text('URL')
                elif name == 'Constraints':
                    self._parse_Constraints(originator.constraints)
                else:
                    self._raise()
            # else
        return originator

    ##############################################

    def _parse_Constraints(self, constraints):

        # <gpp:Constraints>
        #   <gpp:Constraint> ... </gpp:Constraint>
        # </gpp:Constraints>

        while not self._read_match_end_element('Constraints'):
            if self._match_empty():
                continue
            constraints.append(self._parse_Constraint())

    ##############################################

    def _parse_Constraint(self):

        # <gpp:Constraint>
        #   <gpp:CRS>EPSG:4326</gpp:CRS>
        #   <gpp:BoundingBox maxT="2015-08-24" minT="2015-08-24">-63.160706,-21.39223,55.84643,51.090965</gpp:BoundingBox>
        #   <sld:MinScaleDenominator>69885284</sld:MinScaleDenominator>
        #   <sld:MaxScaleDenominator>69885284</sld:MaxScaleDenominator>
        # </gpp:Constraint>

        if not self._match_start_element('Constraint'):
            self._raise()
        constraint = Constraint()
        while not self._read_match_end_element('Constraint'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'CRS':
                    constraint.crs = self._read_text('CRS')
                elif name == 'BoundingBox':
                    constraint.bounding_box = self._parse_LayerBoundingBox()
                elif name == 'MinScaleDenominator':
                    constraint.min_scale_denominator = self._read_int('MinScaleDenominator')
                elif name == 'MaxScaleDenominator':
                    constraint.min_scale_denominator = self._read_int('MaxScaleDenominator')
                else:
                    self._raise()
            # else
        return constraint

    ##############################################

    def _parse_Legends(self, legends):

        # <gpp:Legends>
        #   <gpp:Legend> ... </gpp:Legend>
        # </gpp:Legends>

        while not self._read_match_end_element('Legends'):
            if self._match_empty():
                continue
            legends.append(self._parse_Legend())

    ##############################################

    def _parse_Legend(self):

        #   <gpp:Legend>
        #     <sld:MinScaleDenominator>534</sld:MinScaleDenominator>
        #     <gpp:LegendURL format="format">
        #       <OnlineResource xlink:href="http://wxs.ign.fr/static/legends/NOLEGEND.JPG" xlink:type="simple"/>
        #     </gpp:LegendURL>
        #   </gpp:Legend>

        if not self._match_start_element('Legend'):
            self._raise()
        legend = Legend()
        while not self._read_match_end_element('Legend'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'MinScaleDenominator':
                    legend.min_scale_denominator = self._read_int('MinScaleDenominator')
                elif name == 'LegendURL':
                    legend.url = self._parse_OnlineResource()
                else:
                    self._raise()
            # else
        return legend

    ##############################################

    def _parse_Quicklook(self):

        # <gpp:QuickLook>
        #   <OnlineResource xlink:href="http://wxs.ign.fr/static/pictures/BDPARCELLAIRE.png" xlink:type="simple"/>
        # </gpp:QuickLook>

        self._read_until_empty()
        if not self._match_start_element('OnlineResource'):
            self._raise()
        attr = self._attribute_to_dict('href', 'type')
        return attr['href'] # type

    ##############################################

    def _parse_OnlineResource(self):

        # MetadataURL
        # LegendURL

        # <gpp:MetadataURL format="xml">
        #   <OnlineResource xlink:href="http://wxs.ign.fr/geoportail/csw?service=CSW&amp;version=2.0.2&amp;request=GetRecordById&amp;Id=IGNF_BDPARCELLAIREr_1-2_image.xml" xlink:type="simple"/>
        # </gpp:MetadataURL>

        attr = self._attribute_to_dict('format')
        self._read_until_empty()
        if not self._match_start_element('OnlineResource'):
            self._raise()
        attr = self._attribute_to_dict('href', 'type')
        return attr['href'] # format type

    ##############################################

    def _parse_Keys(self, keys):

        # <gpp:Keys>
        #   <gpp:Key id="algzhye2iogn8fvb0nkgf0zx">http://wxs.ign.fr/algzhye2iogn8fvb0nkgf0zx/geoportail/r/wms</gpp:Key>
        # </gpp:Keys>

        while not self._read_match_end_element('Keys'):
            if self._match_empty():
                continue
            key = Key()
            url = self._read_text('Key')
            attr = self._attribute_to_dict('id')
            key.url = url
            key.attr = attr['id']
            keys.append(key)

    ##############################################

    def _parse_TileMatrixSetLink(self):

        # <wmts:TileMatrixSetLink>
        #   <wmts:TileMatrixSet>PM</wmts:TileMatrixSet>
        #   <wmts:TileMatrixSetLimits> ... </wmts:TileMatrixLimits>
        #     ...
        #   </wmts:TileMatrixSetLimits>
        # </wmts:TileMatrixSetLink>

        if not self._match_start_element('TileMatrixSetLink'):
            self._raise()
        tile_matrix_set_link = TileMatrixSetLink()
        while not self._read_match_end_element('TileMatrixSetLink'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'TileMatrixSet':
                    tile_matrix_set_link.name = self._read_text('TileMatrixSet')
                elif name == 'TileMatrixSetLimits':
                    self._parse_TileMatrixSetLimits(tile_matrix_set_link.limits)
                else:
                    self._raise()
            # else
        return tile_matrix_set_link

    ##############################################

    def _parse_TileMatrixSetLimits(self, limits):

        while not self._read_match_end_element('TileMatrixSetLimits'):
            if self._match_empty():
                continue
            limits.append(self._parse_TileMatrixLimits())

    ##############################################

    def _parse_TileMatrixLimits(self):

        # <wmts:TileMatrixLimits>
        #   <wmts:TileMatrix>10</wmts:TileMatrix>
        #   <wmts:MinTileRow>342</wmts:MinTileRow>
        #   <wmts:MaxTileRow>574</wmts:MaxTileRow>
        #   <wmts:MinTileCol>332</wmts:MinTileCol>
        #   <wmts:MaxTileCol>670</wmts:MaxTileCol>
        # </wmts:TileMatrixLimits>

        if not self._match_start_element('TileMatrixLimits'):
            self._raise()
        tile_matrix_limits = TileMatrixLimits()
        while not self._read_match_end_element('TileMatrixLimits'):
            if self._match_empty():
                continue
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'TileMatrix':
                    tile_matrix_limits.level = self._read_int('TileMatrix')
                elif name == 'MinTileRow':
                    tile_matrix_limits.min_tile_row = self._read_int('MinTileRow')
                elif name == 'MaxTileRow':
                    tile_matrix_limits.max_tile_row = self._read_int('MaxTileRow')
                elif name == 'MinTileCol':
                    tile_matrix_limits.min_tile_col = self._read_int('MinTileCol')
                elif name == 'MaxTileCol':
                    tile_matrix_limits.max_tile_col = self._read_int('MaxTileCol')
                else:
                    self._raise()
            # else
        return tile_matrix_limits

####################################################################################################
#
# End
#
####################################################################################################
