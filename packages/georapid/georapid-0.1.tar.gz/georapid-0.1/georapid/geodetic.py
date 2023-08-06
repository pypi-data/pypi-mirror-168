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

from . client import GeoRapidClient
from . formats import OutFormat
from . units import LinearUnit



def create_points_along(client: GeoRapidClient, lat1: float, lon1: float, lat2: float, lon2: float, distances: list[float], offsets: list[float], unit: LinearUnit=LinearUnit.km, format: OutFormat=OutFormat.GEOJSON):
    """
    Creates points along the line defined by lat1, lon1 and lat2, lon2.
    The distances define the location along the line, and the offsets define the lateral offset.
    The number of distances must equal the number of offsets.
    A combination of distances=[0, <line length>] and offsets=[0, 0] creates a point at the start and another at the end location.
    The unit defines the linear unit e.g. 'km' for the distances and the offsets.
    The format can be GeoJSON or Esri.
    """
    endpoint = '{0}/along'.format(client.url)
    json = {
        'lat1': lat1,
        'lon1': lon1,
        'lat2': lat2,
        'lon2': lon2,
        'distances': distances,
        'offsets': offsets,
        'unit': str(unit),
        'format': str(format)
    }
    response = requests.request('POST', endpoint, headers=client.auth_headers, json=json)
    response.raise_for_status()
    return response.json()

def create_buffers(client: GeoRapidClient, latitudes: list[float], longitudes: list[float], distance: float, unit='km', format: OutFormat=OutFormat.GEOJSON):
    """
    Creates geodetic buffers representing a region or protected area around the specified locations.
    The distance defines the location of the buffer's boundary.
    The unit defines the linear unit e.g. 'km' for the distance.
    The format can be GeoJSON or Esri.
    """
    endpoint = '{0}/buffer'.format(client.url)
    json = {
        'lat': latitudes,
        'lon': longitudes,
        'distance': distance,
        'unit': str(unit),
        'format': str(format)
    }
    response = requests.request('POST', endpoint, headers=client.auth_headers, json=json)
    response.raise_for_status()
    return response.json()

def create_buffers_from_points(client: GeoRapidClient, point_feature_collection: dict, distance: float, unit='km', format: OutFormat=OutFormat.GEOJSON):
    """
    Creates geodetic buffers representing a region or protected area around the specified point features.
    The distance defines the location of the buffer's boundary.
    The unit defines the linear unit e.g. 'km' for the distance.
    The format can be GeoJSON or Esri.
    """
    if not 'type' in point_feature_collection:
        raise ValueError("Feature collection must contain 'type' property!")
        
    geojson_type = point_feature_collection['type']
    if not 'FeatureCollection' == geojson_type:
        raise ValueError("Feature collection must be of type 'FeatureCollection'!")

    if 'crs' in point_feature_collection:
        geojson_crs = point_feature_collection['crs']
        if 'type' in geojson_crs and 'properties' in geojson_crs:
            crs_type = geojson_crs['type']
            if 'name' == crs_type:
                crs_properties = geojson_crs['properties']
                if 'name' in crs_properties:
                    crs_name = str(crs_properties['name'])
                    if not crs_name.endswith(':CRS84'):
                        raise ValueError("Spatial reference '{0}' is not supported!".format(crs_name))
                
    if not 'features' in point_feature_collection:
        raise ValueError("Feature collection must contain 'features' property!")

    latitudes = []
    longitudes = []
    features = point_feature_collection['features']
    for feature in features:
        if not 'geometry' in feature:
            raise ValueError("Feature must contain 'geometry' property!")

        geometry = feature['geometry']
        if not 'type' in geometry:
            raise ValueError("Geometry must contain 'type' property!")

        geometry_type = geometry['type']
        if 'Point' != geometry_type:
            raise ValueError("Geometry must represent a 'Point'!")

        if not 'coordinates' in geometry:
            raise ValueError("Geometry must contain 'coordinates' property!")
        
        coordinates = geometry['coordinates']
        if not type(coordinates) == list:
            raise ValueError("Coordinates must be of type list!")

        if len(coordinates) < 2:
            raise ValueError("Coordinates must contain at least X and Y!")

        latitudes.append(coordinates[1])
        longitudes.append(coordinates[0])

    return create_buffers(client, latitudes, longitudes, distance, unit, format)
        
def create_points_from_direction(client: GeoRapidClient, latitudes: list[float], longitudes: list[float], azimuth: float, distance: float, unit='km', format: OutFormat=OutFormat.GEOJSON):
    """
    Creates points using locations of observers, a distance and a direction representing the azimuth using degree targeting onto the observed location.
    The unit defines the linear unit, e.g. 'km' for the distance.
    The format can be GeoJSON or Esri.
    """
    endpoint = '{0}/direction'.format(client.url)
    json = {
        'lat': latitudes,
        'lon': longitudes,
        'azimuth': azimuth,
        'distance': distance,
        'unit': str(unit),
        'format': str(format)
    }
    response = requests.request('POST', endpoint, headers=client.auth_headers, json=json)
    response.raise_for_status()
    return response.json()

def create_path_from_directions(client: GeoRapidClient, latitude: float, longitude: float, azimuths: list[float], distances: list[float], unit='km', format: OutFormat=OutFormat.GEOJSON):
    """
    Creates a path using a start location, a combination of distances defining the location along the path and directions representing the azimuths at every vertex of the path.
    The unit defines the linear unit, e.g. 'km' for the distance.
    The format can be GeoJSON or Esri.
    """
    endpoint = '{0}/path'.format(client.url)
    json = {
        'lat': latitude,
        'lon': longitude,
        'azimuths': azimuths,
        'distances': distances,
        'unit': str(unit),
        'format': str(format)
    }
    response = requests.request('POST', endpoint, headers=client.auth_headers, json=json)
    response.raise_for_status()
    return response.json()

def create_wedges(client: GeoRapidClient, latitudes: list[float], longitudes: list[float], azimuth: float, azimuth_span: float, distance: float, unit='km', format: OutFormat=OutFormat.GEOJSON):
    """
    Creates parametric wedges using locations of observers, a distance, a direction representing the azimuth using degree and an azimuth span targeting onto the observed location.
    The unit defines the linear unit, e.g. 'km' for the distance.
    The format can be GeoJSON or Esri.
    """
    endpoint = '{0}/wedge'.format(client.url)
    json = {
        'lat': latitudes,
        'lon': longitudes,
        'azimuth': azimuth,
        'span': azimuth_span,
        'distance': distance,
        'unit': str(unit),
        'format': str(format)
    }
    response = requests.request('POST', endpoint, headers=client.auth_headers, json=json)
    response.raise_for_status()
    return response.json()

def to_azimuth(client: GeoRapidClient, direction: str):
    """
    Calculates the corresponding azimuth using a 32-wind compass rose.
    A direction of N equals an azimuth of 0 and a direction of S equals an azimuth of 180.
    """
    endpoint = '{0}/azimuth'.format(client.url)
    params = {
        'direction': direction
    }
    response = requests.request('GET', endpoint, headers=client.auth_headers, params=params)
    response.raise_for_status()
    return response.json()