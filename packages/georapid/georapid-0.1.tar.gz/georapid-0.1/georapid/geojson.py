# Copyright (C) 2022 Jan Tschada (gisfromscratch@live.de)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests

class GeoJSON:

    @staticmethod
    def from_url(url: str) -> dict:
        """
        Returns the GeoJSON object representation using the specified url linking to a valid WGS84 GeoJSON file.
        """
        response = requests.get(url)
        response.raise_for_status()
        geojson = response.json()
        if not 'type' in geojson:
            raise ValueError("GeoJSON response must contain 'type' property!")
        
        geojson_type = geojson['type']
        if not 'FeatureCollection' == geojson_type:
            raise ValueError("GeoJSON response must be of type 'FeatureCollection'!")

        if 'crs' in geojson:
            geojson_crs = geojson['crs']
            if 'type' in geojson_crs and 'properties' in geojson_crs:
                crs_type = geojson_crs['type']
                if 'name' == crs_type:
                    crs_properties = geojson_crs['properties']
                    if 'name' in crs_properties:
                        crs_name = str(crs_properties['name'])
                        if not crs_name.endswith(':CRS84'):
                            raise ValueError("Spatial reference '{0}' is not supported!".format(crs_name))
                 
        if not 'features' in geojson:
            raise ValueError("GeoJSON response must contain 'features' property!")

        return geojson