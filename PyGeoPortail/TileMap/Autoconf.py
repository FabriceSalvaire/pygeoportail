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

class JsonAble(object):

    ##############################################

    def _jsonify(self, value):

        if isinstance(value, list):
            return [self._jsonify(x) for x in value]
        elif isinstance(value, JsonAble):
            return value.to_json()
        else:
            return value

    ##############################################

    def to_json(self):

        d = {}
        for key, value in self.__dict__.items():
                d[key] = self._jsonify(value)
        return d

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
        self.defaultGMLGFIStyleUr = None
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
        self.tile_matrixs = []

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

class Service(JsonAble):

    ##############################################

    def __init__(self):

        self.service = None
        self.title = None
        self.version = None
        self.href = None

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
        self.format_list = None
        self.style_list = None
        self.dimension_list = None
        self.extension = None
        self.srs = None

####################################################################################################

class AutoConfParser(object):

    ##############################################

    def __init__(self, xml_document):

        self._xml_parser = QXmlStreamReader(xml_document)
        # xml_parser.setDevice(xml_document)
        self._parse_document()

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

    def _attribute_to_dict(self, *keys):

        attributes = self._xml_parser.attributes()
        return {key:attributes.value(key) for key in keys}

    ##############################################

    def _read_text(self, name):

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

    def _parse_document(self):

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
        if self._xml_parser.readNext() != QXmlStreamReader.EndDocument:
            self._raise()
        print(json.dumps(autoconf.to_json(), indent=2))

    ##############################################

    def _parse_General(self, general):

        while not self._read_match_end_element('General'):
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

    ##############################################

    def _parse_Window(self, general):

        # <Window height="300" width="500"/>
        attr = self._attribute_to_dict('height', 'width')
        general.window = {key:int(value) for key, value in attr.items()}

    ##############################################

    def _parse_BoundingBox(self, general):

        # <BoundingBox SRS="EPSG:4326" maxx="180.0" maxy="90.0" minx="-90.0" miny="-180.0"/>
        general.bounding_box = self._attribute_to_dict('SRS', 'maxx', 'maxy', 'minx', 'miny')

    ##############################################

    def _parse_Title(self, general):

        # <Title>Service d'autoconfiguration des API</Title>
        general.title = self._read_text('Title')

    ##############################################

    def _parse_Extension(self, extension):

        # <Extension>
        #   <gpp:General>

        # gpp:
        if not self._read_match_start_element('General'):
            self._raise()
        
        while not self._read_match_end_element('General'):
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
        
        if not self._read_match_end_element('Extension'):
            self._raise()

    ##############################################

    def _parse_Territories(self, territories):

        # <gpp:Territories>
	#   <gpp:Territory default="1" id="FXX" name="FXX">

        while not self._read_match_end_element('Territories'):
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
	#   <gpp:Center>
        #   ...
	#   </gpp:Center>
	#   <gpp:DefaultLayers>
        #     ...
	#   </gpp:DefaultLayers>
	# </gpp:Territory>

        territory = Territory()
        
        if not self._match_start_element('Territory'):
            self._raise()
        attr = self._attribute_to_dict('default', 'id', 'name')
        territory.default = attr['default']
        territory.id = attr['id']
        territory.name = attr['name']
        
        while not self._read_match_end_element('Territory'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'defaultCRS':
                    territory.default_crs = self._read_text('defaultCRS')
                elif name == 'AdditionalCRS':
                    territory.additional_crs.append(self._read_text('AdditionalCRS'))
                elif name == 'BoundingBox':
                    territory.bounding_box = [float(x) for x in self._read_text('BoundingBox').split(',')]
                elif name == 'MinScaleDenominator':
                    territory.min_scale_denominator = float(self._read_text('MinScaleDenominator'))
                elif name == 'MaxScaleDenominator':
                    territory.max_scale_denominator = float(self._read_text('MaxScaleDenominator'))
                elif name == 'Resolution':
                    territory.resolution = float(self._read_text('Resolution'))
                elif name == 'Center':
                    territory.center = self._parse_Center()
                elif name == 'DefaultLayers':
                    self._parse_DefaultLayers(territory.default_layers)
                else:
                    self._raise()
        
        return territory

    ##############################################

    def _parse_Center(self):

	#   <gpp:Center>
	#     <gpp:x>2.345274398</gpp:x>
	#     <gpp:y>48.860832558</gpp:y>
	#   </gpp:Center>

        while not self._read_match_end_element('Center'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'x':
                    x = float(self._read_text('x'))
                elif name == 'y':
                    y = float(self._read_text('y'))
                else:
                    self._raise()

        return x, y

    ##############################################

    def _parse_DefaultLayers(self, default_layers):

	#   <gpp:DefaultLayers>
	#     <gpp:DefaultLayer layerId="ORTHOIMAGERY.ORTHOPHOTOS$GEOPORTAIL:OGC:WMTS"/>
	#     <gpp:DefaultLayer layerId="GEOGRAPHICALGRIDSYSTEMS.MAPS$GEOPORTAIL:OGC:WMTS"/>
        #     ...
	#   </gpp:DefaultLayers>

        while not self._read_match_end_element('DefaultLayers'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'DefaultLayer':
                    default_layers.append(self._attribute_to_dict('layerId'))
                else:
                    self._raise()

    ##############################################

    def _parse_TileMatrixSets(self, tile_matrix_sets):

	# <gpp:TileMatrixSets>
	#   <wmts:TileMatrixSet>
        #   ...
        #   </wmts:TileMatrixSet>
        #   ...
        # </gpp:TileMatrixSets>

        while not self._read_match_end_element('TileMatrixSets'):
            tile_matrix_sets.append(self._parse_TileMatrixSet())

    ##############################################

    def _parse_TileMatrixSet(self):

	# <wmts:TileMatrixSet>
	#   <ows:Identifier>PM</ows:Identifier>
	#   <ows:SupportedCRS>EPSG:3857</ows:SupportedCRS>
	#   <wmts:TileMatrix>
        #   ...
	#   </wmts:TileMatrix>
        # ...
        # </wmts:TileMatrixSet>

        tile_matrix_set = TileMatrixSet()
        
        if not self._match_start_element('TileMatrixSet'):
            self._raise()
        
        while not self._read_match_end_element('TileMatrixSet'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Identifier':
                    tile_matrix_set.identifier = int(self._read_text('Identifier'))
                elif name == 'SupportedCRS':
                    tile_matrix_set.supported_crs = self._read_text('SupportedCRS')
                elif name == 'TileMatrix':
                    tile_matrix_set.tile_matrixs.append(self._parse_TileMatrix())
                else:
                    self._raise()

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
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Identifier':
                    tile_matrix.identifier = int(self._read_text('Identifier'))
                elif name == 'ScaleDenominator':
                    tile_matrix.scale_denominator = float(self._read_text('ScaleDenominator'))
                elif name == 'TopLeftCorner':
                    tile_matrix.top_left_corner = [int(x) for x in self._read_text('TopLeftCorner').split()]
                elif name == 'TileWidth':
                    tile_matrix.tile_width = int(self._read_text('TileWidth'))
                elif name == 'TileHeight':
                    tile_matrix.tile_height = int(self._read_text('TileHeight'))
                elif name == 'MatrixWidth':
                    tile_matrix.matrix_width = int(self._read_text('MatrixWidth'))
                elif name == 'MatrixHeight':
                    tile_matrix.matrix_height = int(self._read_text('MatrixHeight'))
                else:
                    self._raise()

        return tile_matrix

    ##############################################

    def _parse_Resolutions(self):

        return [float(x) for x in self._read_text('Resolutions').split(',')]

    ##############################################

    def _parse_Services(self, services):

	# <gpp:Services>
	#   <Server service="OGC:OPENLS;Geocode" title="Service de Geocodage" version="1.2">
	#     ...
	#   </Server>
        #   ...
        # <gpp:Services>

        while not self._read_match_end_element('Services'):
            services.append(self._parse_Server())

    ##############################################

    def _parse_Server(self):

	#   <Server service="OGC:OPENLS;Geocode" title="Service de Geocodage" version="1.2">
	#     <OnlineResource xlink:href="http://wxs.ign.fr/geoportail/ols" xlink:type="simple"/>
	#   </Server>

        service = Service()
        attr = self._attribute_to_dict('service', 'title', 'version')
        service.service = attr['service']
        service.title = attr['title']
        service.version = attr['version']
        while not self._read_match_end_element('Server'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'OnlineResource':
                    service.href = self._attribute_to_dict('xlink:href')
                else:
                    self._raise()
        return service

    ##############################################

    def _parse_LayerList(self, layer_list):

        # <LayerList>
        #   <Layer hidden="1" queryable="1">
        #     ...
        #   </Layer>
        #   ...
        # </LayerList>

        while not self._read_match_end_element('LayerList'):
            layer_list.append(self._parse_Layer())

    ##############################################

    def _parse_Layer(self):

        layer = Layer()
        attr = self._attribute_to_dict('hidden', 'queryable')
        layer.hidden = bool(attr['hidden'])
        layer.queryable = bool(attr['queryable'])
        while not self._read_match_end_element('Layer'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Server':
                    self._parse_Server()
                elif name == 'Name':
                    layer.name = self._read_text('Name')
                elif name == 'Title':
                    layer.title = self._read_text('Title')
                elif name == 'Abstract':
                    layer.abstract = self._read_text('Abstract')
                elif name == 'MinScaleDenominator':
                    layer.min_scale_denominator = float(self._read_text('MinScaleDenominator'))
                elif name == 'MaxScaleDenominator':
                    layer.max_scale_denominator = float(self._read_text('MaxScaleDenominator'))
                elif name == 'FormatList':
                    self._parse_FormatList()
                elif name == 'StyleList':
                    self._parse_StyleList()
                elif name == 'DimensionList':
                    self._parse_DimensionList()
                elif name == 'Extension':
                    self._parse_Layer_Extension()
                elif name == 'SRS':
                    layer.srs = self._read_text('SRS')
                else:
                    self._raise()
        return layer

    ##############################################

    def _parse_FormatList(self):

        # <FormatList>
        #   <Format current="1">text/xml</Format>
        #   ...
        # </FormatList>

        while not self._read_match_end_element('FormatList'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Format':
                    attr = self._attribute_to_dict('current')
                    self._read_text('Format')
                else:
                    self._raise()

    ##############################################

    def _parse_StyleList(self):

        # <StyleList>
        #   <Style current="1">
        #   </Style>
        #   ...
        # <StyleList>

        while not self._read_match_end_element('StyleList'):
            self._parse_Style()

    ##############################################

    def _parse_Style(self):

        #   <Style current="1">
        #     <Name>normal</Name>
        #     <Title>Données Brutes</Title>
        #   </Style>

        attr = self._attribute_to_dict('current')
        while not self._read_match_end_element('Style'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Name':
                    self._read_text('Name')
                elif name == 'Title':
                    self._read_text('Title')
                else:
                    self._raise()

    ##############################################

    def _parse_DimensionList(self):

      # <DimensionList>
      #   <Dimension name="GeometricType" unitSymbol="" units="" userValue="">-</Dimension>
      # </DimensionList>

        while not self._read_match_end_element('DimensionList'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Dimension':
                    attr = self._attribute_to_dict('name', 'unitSymbol', 'units', 'userValue')
                    self._read_text('Dimension')
                else:
                    self._raise()

    ##############################################

    def _parse_Layer_Extension(self):

        # <Extension>
        #   <gpp:Layer id="BDPARCEL_PYR-PNG_WLD$GEOPORTAIL:OGC:WMS">
        #     <gpp:Thematics>
        #       <gpp:Thematic>Parcelles cadastrales</gpp:Thematic>
        #     </gpp:Thematics>
        #     <gpp:InspireThematics>
        #       <gpp:InspireThematic>Parcelles cadastrales</gpp:InspireThematic>
        #     </gpp:InspireThematics>
        #     <gpp:BoundingBox maxT="2015-08-24" minT="2015-08-24">-63.160706,-21.39223,55.84643,51.090965</gpp:BoundingBox>
        #     <gpp:AdditionalCRS>EPSG:2975</gpp:AdditionalCRS>
        #     <gpp:AdditionalCRS>EPSG:3727</gpp:AdditionalCRS>
        #     ...
        #     <gpp:Originators>
        #       <gpp:Originator name="IGN">
        #         <gpp:Attribution>Institut national de l'information géographique et forestière</gpp:Attribution>
        #         <gpp:Logo>http://wxs.ign.fr/static/logos/IGN/IGN.gif</gpp:Logo>
        #         <gpp:URL>http://www.ign.fr</gpp:URL>
        #         <gpp:Constraints>
        #           <gpp:Constraint>
        #             <gpp:CRS>EPSG:4326</gpp:CRS>
        #             <gpp:BoundingBox maxT="2015-08-24" minT="2015-08-24">-63.160706,-21.39223,55.84643,51.090965</gpp:BoundingBox>
        #             <sld:MinScaleDenominator>69885284</sld:MinScaleDenominator>
        #             <sld:MaxScaleDenominator>69885284</sld:MaxScaleDenominator>
        #           </gpp:Constraint>
        #         </gpp:Constraints>
        #       </gpp:Originator>
        #     </gpp:Originators>
        #     <gpp:Legends>
        #       <gpp:Legend>
        #         <sld:MinScaleDenominator>534</sld:MinScaleDenominator>
        #         <gpp:LegendURL format="format">
        #           <OnlineResource xlink:href="http://wxs.ign.fr/static/legends/NOLEGEND.JPG" xlink:type="simple"/>
        #         </gpp:LegendURL>
        #       </gpp:Legend>
        #     </gpp:Legends>
        #     <gpp:QuickLook>
        #       <OnlineResource xlink:href="http://wxs.ign.fr/static/pictures/BDPARCELLAIRE.png" xlink:type="simple"/>
        #     </gpp:QuickLook>
        #     <gpp:MetadataURL format="xml">
        #       <OnlineResource xlink:href="http://wxs.ign.fr/geoportail/csw?service=CSW&amp;version=2.0.2&amp;request=GetRecordById&amp;Id=IGNF_BDPARCELLAIREr_1-2_image.xml" xlink:type="simple"/>
        #     </gpp:MetadataURL>
        #     <gpp:Keys>
        #       <gpp:Key id="algzhye2iogn8fvb0nkgf0zx">http://wxs.ign.fr/algzhye2iogn8fvb0nkgf0zx/geoportail/r/wms</gpp:Key>
        #     </gpp:Keys>
        #   </gpp:Layer>
        # </Extension>

        self._read_until_end_of('Extension')

####################################################################################################
#
# End
#
####################################################################################################
