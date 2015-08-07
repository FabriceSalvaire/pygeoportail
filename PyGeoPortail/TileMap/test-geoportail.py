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
#
# Logging
#

import PyGeoPortail.Logging.Logging as Logging

logger = Logging.setup_logging('pygeoportail')

####################################################################################################

import asyncio

####################################################################################################

from PyGeoPortail.TileMap.GeoPortail import (GeoPortailWebService,
                                             GeoPortailPyramid,
                                             GeoPortailWTMS,
                                             GeoPortailMapProvider,
                                             GeoPortailOthorPhotoProvider)

from PyGeoPortail.TileMap.Projection import GeoAngle, GeoCoordinate

####################################################################################################

geoportail_pyramid = GeoPortailPyramid()

level = 16
longitude = GeoAngle(6, 7, 0)
latitude = GeoAngle(44, 41, 0)
location = GeoCoordinate(longitude, latitude)
row, column = geoportail_pyramid[level].coordinate_to_mosaic(location)

user = 'fabrice.salvaire@orange.fr'
password = 'fA77Sal(!'
api_key = 'qd58byg78dg3nloou4ksa0pz'
geoportail_web_service = GeoPortailWebService(user, password, api_key, timeout=120)

print(geoportail_web_service.make_url('geoportail', 'wmts',
                                      service='WMTS',
                                      version='1.0.0',
                                      request='GetTile',
                                      layer='GEOGRAPHICALGRIDSYSTEMS.MAPS',
                                      style='normal',
                                      format='image/jpeg',
                                      tilematrixset='PM',
                                      tilematrix=level,
                                      tilerow=row,
                                      tilecol=column,
))

loop = asyncio.get_event_loop()

# print(loop.run_until_complete(geoportail_web_service.async_get('geoportail', 'wmts',
#                                                                service='WMTS',
#                                                                version='1.0.0',
#                                                                request='GetTile',
#                                                                layer='GEOGRAPHICALGRIDSYSTEMS.MAPS',
#                                                                style='normal',
#                                                                format='image/jpeg',
#                                                                tilematrixset='PM',
#                                                                tilematrix=level,
#                                                                tilerow=row,
#                                                                tilecol=column,
# )))

# Could take a while ...
# print(geoportail_web_service.autoconf(api_key))

# timeout ???
# tasks = [asyncio.async(geoportail_web_service.async_autoconf(api_key))]
# response = loop.run_until_complete(asyncio.wait(tasks, timeout=120))
# print(response)

xml_query = '''<?xml version="1.0" encoding="UTF-8"?>
<XLS xmlns:gml="http://www.opengis.net/gml"
     xmlns="http://www.opengis.net/xls"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     version="1.2"
     xsi:schemaLocation="http://www.opengis.net/xls http://schemas.opengis.net/ols/1.2/olsAll.xsd">
  <RequestHeader srsName="epsg:4326"/>
  <Request maximumResponses="1" methodName="GeocodeRequest" requestID="1" version="1.2">
    <GeocodeRequest>
      <Address countryCode="StreetAddress">
        <freeFormAddress>1 rue Marconi 57000 Metz</freeFormAddress>
      </Address>
    </GeocodeRequest>
  </Request>
</XLS>'''

# xml_query = '''<?xml version="1.0" encoding="UTF-8"?>
# <XLS
#   xmlns:xls="http://www.opengis.net/xls"
#   xmlns:gml="http://www.opengis.net/gml"
#   xmlns="http://www.opengis.net/xls"
#   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#   version="1.2"
#   xsi:schemaLocation="http://www.opengis.net/xls http://schemas.opengis.net/ols/1.2/olsAll.xsd">
#     <RequestHeader/>
#     <Request requestID="1" version="1.2" methodName="LocationUtilityService">
#        <GeocodeRequest returnFreeForm="false">
#          <Address countryCode="PositionOfInterest">
#                 <freeFormAddress>rennes</freeFormAddress>
#          </Address>
#        </GeocodeRequest>
#     </Request>
# </XLS>'''

# xml_query = '''<?xml version="1.0" encoding="UTF-8"?>
# <XLS version="1.2" xsi:schemaLocation="http://wxs.ign.fr/schemas/olsAll.xsd" xmlns:xls="http://www.opengis.net/xls" xmlns="http://www.opengis.net/xls" xmlns:xlsext="http://www.opengis.net/xlsext" xmlns:gml="http://www.opengis.net/gml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
# <RequestHeader/>
# <Request requestID="1" version="1.2" methodName="LocationUtilityService">
# <GeocodeRequest returnFreeForm="false">
# <Address countryCode="StreetAddress">
# <StreetAddress>
# <Street>1 rue Marconi</Street>
# </StreetAddress>
# <Place type="Municipality">Metz</Place>
# <PostalCode>57000</PostalCode>
# </Address>
# </GeocodeRequest>
# </Request>
# </XLS>'''

#print(geoportail_web_service.post('geoportail', 'ols', data=xml_query))
print(geoportail_web_service.get('geoportail', 'ols', xls=xml_query))

####################################################################################################
#
# End
#
####################################################################################################
