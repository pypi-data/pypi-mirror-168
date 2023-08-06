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



def aggregate(client: GeoRapidClient, date: datetime = datetime.utcnow(), format = OutFormat.GEOJSON):
    """
    Aggregates the broadcasted news related to wildfires using a spatial grid and returns the features as hexagonal bins.
    The date is optional. When not specified, we use datetime.utcnow().
    The underlying knowledge graph collects data from '2015-03-01' up to today.
    The format can be GeoJSON or Esri JSON.
    """
    endpoint = '{0}/aggregate'.format(client.url)
    params = {
        'format': str(format)
    }
    if date:
        params['date'] = datetime.strftime(date, '%Y-%m-%d')

    return requests.request('GET', endpoint, headers=client.auth_headers, params=params).json()

def articles(client: GeoRapidClient, date: datetime = datetime.utcnow()):
    """
    Returns a list of broadcasted articles related to wildfires.
    The date is optional. When not specified, we use datetime.utcnow().
    The underlying knowledge graph collects data from '2015-03-01' up to today.
    """
    endpoint = '{0}/articles'.format(client.url)
    params = {}
    if date:
        params['date'] = datetime.strftime(date, '%Y-%m-%d')

    return requests.request('GET', endpoint, headers=client.auth_headers, params=params).json()

def query(client: GeoRapidClient, date: datetime = datetime.utcnow(), format = OutFormat.GEOJSON):
    """
    Returns the locations related to wildfires.
    The date is optional. When not specified, we use datetime.utcnow().
    The underlying knowledge graph collects data from '2015-03-01' up to today.
    The format can be GeoJSON or Esri JSON.
    """
    endpoint = '{0}/query'.format(client.url)
    params = {
        'format': str(format)
    }
    if date:
        params['date'] = datetime.strftime(date, '%Y-%m-%d')

    return requests.request('GET', endpoint, headers=client.auth_headers, params=params).json()