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

class GeoRapidClient(object):
    """
    Represents a client accessing the geospatial knowledge API services being hosted at Rapid API.
    """

    def __init__(self, url, auth_headers) -> None:
        """
        Initializes this instance using an url and an authorization header dictionary.
        The dictionary must contain 'x-rapidapi-host' and 'x-rapidapi-host' as keys.
        """
        self._url = url
        if not 'x-rapidapi-host' in auth_headers:
            raise ValueError("'x-rapidapi-host' must be specified in the authorization header!")
        if not 'x-rapidapi-key' in auth_headers:
            raise ValueError("'x-rapidapi-key' must be specified in the authorization header!")

        self._auth_headers = auth_headers

    @property
    def auth_headers(self):
        """Returns the authorization header dictionary."""
        return self._auth_headers

    @property
    def url(self):
        """Returns the endpoint url."""
        return self._url
