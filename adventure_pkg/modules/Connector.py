# Copyright 2020 Sebastian Ahmed
# This file, and derivatives thereof are licensed under the Apache License, Version 2.0 (the "License");
# Use of this file means you agree to the terms and conditions of the license and are in full compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, EITHER EXPRESSED OR IMPLIED.
# See the License for the specific language governing permissions and limitations under the License.

class Connector():
    '''
        Basic class to connect Locations comprised of a handle to connected Location
        and a handle to an obstruction
        By default a connector is not bound to anything
    '''
    def __init__(self,locHandle=None,obsHandle=None):
        self._locHandle = locHandle
        self._obsHandle = obsHandle
