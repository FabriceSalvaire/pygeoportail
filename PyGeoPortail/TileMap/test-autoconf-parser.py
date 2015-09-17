####################################################################################################

from PyQt5.QtCore import QXmlStreamReader

####################################################################################################

xml_path = '/home/gv/sys/fc14/fabrice/pygeoportail/notes/wmts/geoportail-autoconf-raw.xml'
with open(xml_path) as f:
    xml_document = f.read()
xml_document = bytes(xml_document, encoding='utf8')
# print(xml_document)

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

        if self._xml_parser.readNext() != QXmlStreamReader.StartDocument:
            self._raise()
        if not self._read_match_start_element('ViewContext'):
            self._raise()
        while not self._read_match_end_element('ViewContext'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'General':
                    self._parse_General()
                elif name == 'LayerList':
                    self._parse_LayerList()
                else:
                    self._raise()
        if self._xml_parser.readNext() != QXmlStreamReader.EndDocument:
            self._raise()

    ##############################################

    def _parse_General(self):

        while not self._read_match_end_element('General'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Window':
                    self._parse_Window()
                elif name == 'BoundingBox':
                    self._parse_BoundingBox()
                elif name == 'Title':
                    self._parse_Title()
                elif name == 'Extension':
                    self._parse_Extension()
                else:
                    self._raise()

    ##############################################

    def _parse_Window(self):

        # <Window height="300" width="500"/>
        print('Window', self._attribute_to_dict('height', 'width'))

    ##############################################

    def _parse_BoundingBox(self):

        # <BoundingBox SRS="EPSG:4326" maxx="180.0" maxy="90.0" minx="-90.0" miny="-180.0"/>
        print('BoundingBox', self._attribute_to_dict('SRS', 'maxx', 'maxy', 'minx', 'miny'))

    ##############################################

    def _parse_Title(self):

        # <Title>Service d'autoconfiguration des API</Title>
        print('Title', self._read_text('Title'))

    ##############################################

    def _parse_Extension(self):

        # <Extension>
        #   <gpp:General>

        # gpp:
        if not self._read_match_start_element('General'):
            self._raise()
        
        while not self._read_match_end_element('General'):
            if self._xml_parser.isStartElement:
                name = self._xml_parser.name()
                if name == 'Theme':
                    self._read_text('Theme')
                elif name == 'defaultGMLGFIStyleUrl':
                    self._read_text('defaultGMLGFIStyleUrl')
                elif name == 'Territories':
                    self._parse_Territories()
                elif name == 'TileMatrixSets':
                    self._parse_TileMatrixSets()
                elif name == 'Resolutions':
                    self._parse_Resolutions()
                elif name == 'Services':
                    self._parse_Services()
                else:
                    self._raise()
        
        if not self._read_match_end_element('Extension'):
            self._raise()

    ##############################################

    def _parse_Territories(self):

        # <gpp:Territories>
	#   <gpp:Territory default="1" id="FXX" name="FXX">

        while not self._read_match_end_element('Territories'):
            self._parse_Territory()

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

        if not self._match_start_element('Territory'):
            self._raise()
        print('Territory', self._attribute_to_dict('default', 'id', 'name'))
        
        while not self._read_match_end_element('Territory'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'defaultCRS':
                    self._read_text('defaultCRS')
                elif name == 'AdditionalCRS':
                    self._read_text('AdditionalCRS')
                elif name == 'BoundingBox':
                    self._read_text('BoundingBox')
                elif name == 'MinScaleDenominator':
                    self._read_text('MinScaleDenominator')
                elif name == 'MaxScaleDenominator':
                    self._read_text('MaxScaleDenominator')
                elif name == 'Resolution':
                    self._read_text('Resolution')
                elif name == 'Center':
                    self._parse_Center()
                elif name == 'DefaultLayers':
                    self._parse_DefaultLayers()
                else:
                    self._raise()

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
                    self._read_text('x')
                elif name == 'y':
                    self._read_text('y')
                else:
                    self._raise()

    ##############################################

    def _parse_DefaultLayers(self):

	#   <gpp:DefaultLayers>
	#     <gpp:DefaultLayer layerId="ORTHOIMAGERY.ORTHOPHOTOS$GEOPORTAIL:OGC:WMTS"/>
	#     <gpp:DefaultLayer layerId="GEOGRAPHICALGRIDSYSTEMS.MAPS$GEOPORTAIL:OGC:WMTS"/>
        #     ...
	#   </gpp:DefaultLayers>

        while not self._read_match_end_element('DefaultLayers'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'DefaultLayer':
                    print('DefaultLayer', self._attribute_to_dict('layerId'))
                else:
                    self._raise()

    ##############################################

    def _parse_TileMatrixSets(self):

	# <gpp:TileMatrixSets>
	#   <wmts:TileMatrixSet>
        #   ...
        #   </wmts:TileMatrixSet>
        #   ...
        # </gpp:TileMatrixSets>

        while not self._read_match_end_element('TileMatrixSets'):
            self._parse_TileMatrixSet()

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

        if not self._match_start_element('TileMatrixSet'):
            self._raise()
        
        while not self._read_match_end_element('TileMatrixSet'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Identifier':
                    self._read_text('Identifier')
                elif name == 'SupportedCRS':
                    self._read_text('SupportedCRS')
                elif name == 'TileMatrix':
                    self._parse_TileMatrix()
                else:
                    self._raise()

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

        while not self._read_match_end_element('TileMatrix'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Identifier':
                    self._read_text('Identifier')
                elif name == 'ScaleDenominator':
                    self._read_text('ScaleDenominator')
                elif name == 'TopLeftCorner':
                    self._read_text('TopLeftCorner')
                elif name == 'TileWidth':
                    self._read_text('TileWidth')
                elif name == 'TileHeight':
                    self._read_text('TileHeight')
                elif name == 'MatrixWidth':
                    self._read_text('MatrixWidth')
                elif name == 'MatrixHeight':
                    self._read_text('MatrixHeight')
                else:
                    self._raise()

    ##############################################

    def _parse_Resolutions(self):

        resolutions = self._read_text('Resolutions').split(',')
        print('Resolutions', resolutions)

    ##############################################

    def _parse_Services(self):

	# <gpp:Services>
	#   <Server service="OGC:OPENLS;Geocode" title="Service de Geocodage" version="1.2">
	#     ...
	#   </Server>
        #   ...
        # <gpp:Services>

        while not self._read_match_end_element('Services'):
            self._parse_Server()

    ##############################################

    def _parse_Server(self):

	#   <Server service="OGC:OPENLS;Geocode" title="Service de Geocodage" version="1.2">
	#     <OnlineResource xlink:href="http://wxs.ign.fr/geoportail/ols" xlink:type="simple"/>
	#   </Server>

        while not self._read_match_end_element('Server'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'OnlineResource':
                    print('OnlineResource', self._attribute_to_dict('xlink:href'))
                else:
                    self._raise()

    ##############################################

    def _parse_LayerList(self):

        # <LayerList>
        #   <Layer hidden="1" queryable="1">
        #     ...
        #   </Layer>
        #   ...
        # </LayerList>

        while not self._read_match_end_element('LayerList'):
            self._parse_Layer()

    ##############################################

    def _parse_Layer(self):

        while not self._read_match_end_element('Layer'):
            if self._xml_parser.isStartElement():
                name = self._xml_parser.name()
                if name == 'Server':
                    self._parse_Server()
                elif name == 'Name':
                    self._read_text('Name')
                elif name == 'Title':
                    self._read_text('Title')
                elif name == 'Abstract':
                    self._read_text('Abstract')
                elif name == 'MinScaleDenominator':
                    self._read_text('MinScaleDenominator')
                elif name == 'MaxScaleDenominator':
                    self._read_text('MaxScaleDenominator')
                elif name == 'FormatList':
                    self._parse_FormatList()
                elif name == 'StyleList':
                    self._parse_StyleList()
                elif name == 'DimensionList':
                    self._parse_DimensionList()
                elif name == 'Extension':
                    self._parse_Layer_Extension()
                elif name == 'SRS':
                    self._read_text('SRS')
                else:
                    self._raise()

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
                    print('Format', self._attribute_to_dict('current'), self._read_text('Format'))
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

        print('Style', self._attribute_to_dict('current'))
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
                    print('Dimension',
                          self._attribute_to_dict('name', 'unitSymbol', 'units', 'userValue'),
                          self._read_text('Dimension'))
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

autoconf_parser = AutoConfParser(xml_document)

####################################################################################################
#
# End
#
####################################################################################################
