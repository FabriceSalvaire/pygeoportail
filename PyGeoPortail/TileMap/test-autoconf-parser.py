####################################################################################################

from PyGeoPortail.TileMap.Autoconf.AutoconfParser import AutoconfParser

####################################################################################################

# xml_path = '/home/fabrice/pygeoportail/notes/wmts/geoportail-autoconf-raw.xml'
xml_path = '/home/fabrice/pygeoportail/notes/wmts/geoportail-autoconf.xml'
with open(xml_path) as f:
    xml_document = f.read()
xml_document = bytes(xml_document, encoding='utf8')

autoconf_parser = AutoconfParser()
autoconf = autoconf_parser.parse_document(xml_document)

print(autoconf.to_json())

####################################################################################################
#
# End
#
####################################################################################################
