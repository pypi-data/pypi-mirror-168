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

from datetime import datetime
import requests

from . client import GeoRapidClient
from . formats import OutFormat



def aggregate(client: GeoRapidClient, date: datetime = None, format = OutFormat.GEOJSON):
    """
    Aggregates the broadcasted news related to protests/demonstrations using a spatial grid and returns the features as hexagonal bins.
    The date is optional. When not specified, we return the features of the last 24 hours.
    The underlying hosted feature service saves the last 90 days and yesterday should be the latest available date.
    The format can be GeoJSON or Esri JSON.
    """
    endpoint = '{0}/aggregate'.format(client.url)
    params = {
        'format': str(format)
    }
    if date:
        params['date'] = datetime.strftime(date, '%Y-%m-%d')

    return requests.request('GET', endpoint, headers=client.auth_headers, params=params).json()

def articles(client: GeoRapidClient, date: datetime = None):
    """
    Returns a list of broadcasted articles related to protests/demonstrations.
    The date is optional. When not specified, we return the articles of the last 24 hours.
    The underlying web service saves the last 90 days and yesterday should be the latest available date.
    """
    endpoint = '{0}/articles'.format(client.url)
    params = {}
    if date:
        params['date'] = datetime.strftime(date, '%Y-%m-%d')

    return requests.request('GET', endpoint, headers=client.auth_headers, params=params).json()

def hotspots(client: GeoRapidClient, date: datetime = None, format = OutFormat.GEOJSON):
    """
    Returns the hotspot locations related to protests/demonstrations.
    The date is optional. When not specified, we return the features of the last 24 hours.
    The underlying hosted feature service saves the last 90 days and yesterday should be the latest available date.
    The format can be GeoJSON or Esri JSON.
    """
    endpoint = '{0}/hotspots'.format(client.url)
    params = {
        'format': str(format)
    }
    if date:
        params['date'] = datetime.strftime(date, '%Y-%m-%d')

    return requests.request('GET', endpoint, headers=client.auth_headers, params=params).json()