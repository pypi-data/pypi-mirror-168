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

from enum import Enum, unique



@unique
class LinearUnit(Enum):
    """Represents the supported linear units."""
    mm=0
    cm=1
    m=2
    km=3
    in_=4
    ft=5
    yd=6
    sm=7
    nm=8
    ly=9

    def __str__(self) -> str:
        if 4 == self.value:
            return 'in'
        
        return self.name