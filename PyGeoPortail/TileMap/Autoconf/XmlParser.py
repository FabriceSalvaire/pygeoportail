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

from PyQt5.QtCore import QXmlStreamReader

####################################################################################################

class XmlParser(object):

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

        self._xml_parser = QXmlStreamReader(xml_document)
        # xml_parser.setDevice(xml_document)
        return self.parser_loop()

    ##############################################

    def parser_loop(self):

        raise NotImplementedError

####################################################################################################
#
# End
#
####################################################################################################
