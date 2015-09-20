####################################################################################################

from PyGeoPortail.TileMap.Autoconf import AutoConfParser

####################################################################################################

xml_path = '/home/gv/sys/fc14/fabrice/pygeoportail/notes/wmts/geoportail-autoconf-raw.xml'
with open(xml_path) as f:
    xml_document = f.read()
xml_document = bytes(xml_document, encoding='utf8')

autoconf_parser = AutoConfParser()
autoconf = autoconf_parser.parse_document(xml_document)

print(autoconf.to_json())

####################################################################################################
#
# End
#
####################################################################################################