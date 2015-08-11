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

### <?xml version="1.0" encoding="UTF-8"?>
### <XLS
###   xmlns:xls="http://www.opengis.net/xls"
###   xmlns:gml="http://www.opengis.net/gml"
###   xmlns="http://www.opengis.net/xls"
###   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
###   version="1.2"
###   xsi:schemaLocation="http://www.opengis.net/xls http://schemas.opengis.net/ols/1.2/olsAll.xsd">
###     <RequestHeader/>
###     <Request requestID="1" version="1.2" methodName="LocationUtilityService">
###        <GeocodeRequest returnFreeForm="false">
###          <Address countryCode="PositionOfInterest">
###                 <freeFormAddress>rennes</freeFormAddress>
###          </Address>
###        </GeocodeRequest>
###     </Request>
### </XLS>
### 
### <?xml version="1.0" encoding="UTF-8"?>
### <XLS
###   xmlns:xls="http://www.opengis.net/xls"
###   xmlns:gml="http://www.opengis.net/gml"
###   xmlns="http://www.opengis.net/xls"
###   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
###   version="1.2"
###   xsi:schemaLocation="http://www.opengis.net/xls http://schemas.opengis.net/ols/1.2/olsAll.xsd">
###     <RequestHeader/>
###     <Request requestID="1" version="1.2" methodName="LocationUtilityService">
###        <GeocodeRequest returnFreeForm="false">
###          <Address countryCode="Administratif">
###             <freeFormAddress>Bretagne</freeFormAddress>
###          </Address>
###        </GeocodeRequest>
###     </Request>
### </XLS>
### 
### <?xml version="1.0" encoding="UTF-8"?>
### <XLS 
###   xmlns:gml="http://www.opengis.net/gml" 
###   xmlns="http://www.opengis.net/xls" 
###   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" 
###   xsi:schemaLocation="http://www.opengis.net/xls http://schemas.opengis.net/ols/1.2/olsAll.xsd">
###   <RequestHeader srsName="epsg:4326"/>
###   <Request maximumResponses="25" methodName="GeocodeRequest" requestID="uid42" version="1.2">
###   <GeocodeRequest returnFreeForm="false">
###     <Address countryCode="StreetAddress">
###       <freeFormAddress>2 avenue Pasteur 94160 Saint-Mandé</freeFormAddress>
###     </Address>
###   </GeocodeRequest>
###   </Request>
### </XLS>
### 
### <?xml version="1.0" encoding="UTF-8"?>
### <XLS
###   xmlns:xls="http://www.opengis.net/xls"
###   xmlns:gml="http://www.opengis.net/gml"
###   xmlns="http://www.opengis.net/xls"
###   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
###   version="1.2"
###   xsi:schemaLocation="http://www.opengis.net/xls http://schemas.opengis.net/ols/1.2/olsAll.xsd">
###     <RequestHeader/>
###     <Request requestID="1" version="1.2" methodName="LocationUtilityService">
###        <GeocodeRequest returnFreeForm="false">
###            <Address countryCode="StreetAddress">
###                <StreetAddress>
###                         <Street>1 rue Marconi</Street>
###                </StreetAddress>
###                <Place type="Municipality">Metz</Place>
###                <PostalCode>57000</PostalCode>
###            </Address>
###        </GeocodeRequest>
###     </Request>
### </XLS>
### 
### <?xml version="1.0" encoding="UTF-8"?>
### <XLS
###   xmlns:xls="http://www.opengis.net/xls"
###   xmlns:gml="http://www.opengis.net/gml"
###   xmlns="http://www.opengis.net/xls"
###   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
###   version="1.2"
###   xsi:schemaLocation="http://www.opengis.net/xls http://schemas.opengis.net/ols/1.2/olsAll.xsd">
###     <RequestHeader/>
###     <Request requestID="1" version="1.2" methodName="LocationUtilityService">
###        <GeocodeRequest returnFreeForm="false">
###            <Address countryCode="PositionOfInterest">
###             <freeFormAddress>Saint-Mandé</freeFormAddress>
###               <gml:envelope>
###                     <gml:pos>48.80 2.35</gml:pos>
###                     <gml:pos>48.86 2.47</gml:pos>
###               </gml:envelope>
###            </Address>
###        </GeocodeRequest>
###     </Request>
### </XLS>
### 
### <?xml version="1.0" encoding="UTF-8"?>
### <XLS
###   xmlns:xls="http://www.opengis.net/xls"
###   xmlns:gml="http://www.opengis.net/gml"
###   xmlns="http://www.opengis.net/xls"
###   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
###   version="1.2"
###   xsi:schemaLocation="http://www.opengis.net/xls http://schemas.opengis.net/ols/1.2/olsAll.xsd">
###     <RequestHeader/>
###     <Request requestID="1" version="1.2" methodName="LocationUtilityService">
###        <GeocodeRequest returnFreeForm="false">
###            <Address countryCode="PositionOfInterest">
###                <freeFormAddress>Saint-Mandé</freeFormAddress>
###                <Place type="nature">Lieu-dit habité</Place>
###                <Place type="nature">Ruines</Place>
###            </Address>
###        </GeocodeRequest>
###     </Request>
### </XLS>
### 
### <?xml version="1.0" encoding="UTF-8"?>
### <XLS version="1.2"
###   xmlns="http://www.opengis.net/xls"
###   xmlns:gml="http://www.opengis.net/gml"
###   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
###   xsi:schemaLocation="http://www.opengis.net/xls http://schemas.opengis.net/ols/1.2/olsAll.xsd">
###     <RequestHeader/>
###     <Request methodName="ReverseGeocodeRequest" maximumResponses="10" requestID="abc" version="1.2">
###        <ReverseGeocodeRequest>
###           <ReverseGeocodePreference>StreetAddress</ReverseGeocodePreference>
###           <Position>
###              <gml:Point>
###                 <gml:pos>48.8033333 2.3241667</gml:pos>
###              </gml:Point>
###           </Position>
###        </ReverseGeocodeRequest>
###   </Request>
### </XLS>
### 
### <?xml version="1.0" encoding="UTF-8"?>
### <XLS version="1.2"
###   xmlns="http://www.opengis.net/xls"
###   xmlns:gml="http://www.opengis.net/gml"
###   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
###   xsi:schemaLocation="http://www.opengis.net/xls http://schemas.opengis.net/ols/1.2/olsAll.xsd">
###     <RequestHeader/>
###     <Request methodName="ReverseGeocodeRequest" maximumResponses="10" requestID="abc" version="1.2">
###        <ReverseGeocodeRequest>
###           <ReverseGeocodePreference>StreetAddress</ReverseGeocodePreference>
###             <Position>
###                <gml:Point>
###                         <gml:pos>48.8033333 2.3241667</gml:pos>
###                </gml:Point>
###                <gml:Polygon>
###                   <gml:exterior>
###                       <gml:LinearRing>
###                           <gml:pos>48.8033 2.3241</gml:pos>
###                           <gml:pos>48.8033 2.3242</gml:pos>
###                           <gml:pos>48.8032 2.3242</gml:pos>
###                           <gml:pos>48.8032 2.3241</gml:pos>         
###                       </gml:LinearRing>
###                   </gml:exterior>
###                </gml:Polygon>
###             </Position>
###        </ReverseGeocodeRequest>
###   </Request>
### </XLS>
###

print(geoportail_web_service.get('geoportail', 'ols', xls=xml_query)) # , output='json'

print(geoportail_web_service.get('ols', 'apis', 'completion',
                                 text='20 avenue pasteur saint m',
                                 type='StreetAddress',
                                 maximumResponses=5))

print(geoportail_web_service.get('ols', 'apis', 'completion',
                                 terr='METROPOLE',
                                 text='mont pelvo',
                                 type='PositionOfInterest',
                                 maximumResponses=5))

print(geoportail_web_service.get('ols', 'apis', 'completion',
                                 terr='METROPOLE',
                                 text='refuge des ban',
                                 type='PositionOfInterest',
                                 maximumResponses=5))

####################################################################################################
#
# End
#
####################################################################################################
