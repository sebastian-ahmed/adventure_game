# Copyright 2020 Sebastian Ahmed
# This file, and derivatives thereof are licensed under the Apache License, Version 2.0 (the "License");
# Use of this file means you agree to the terms and conditions of the license and are in full compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, EITHER EXPRESSED OR IMPLIED.
# See the License for the specific language governing permissions and limitations under the License.

from adventure_pkg.modules.Location   import Location
from adventure_pkg.modules.Utils      import typeCheck

class Level(object):
    '''
    Encapsulates a level object:
     - a list of Location objects
     - start location
     - current location
     - playthrough test script
    '''

    def __init__(self,name:str='unnamed'):
        self._name       = name # String name for this level
        self._locList    = []   # List of locations for this level
        self._start_loc  = None # A handle to a starting location object
        self._cur_loc    = None # A handle to the currect location object
        self._testScript = None # A terminal command play-script (for testing)


    def locAdd (self,loc:Location):
        typeCheck(loc,Location)
        self._locList.append(loc)

    @property
    def name(self)->str:
        return self._name

    @property
    def size(self)->int:
        return len(self._locList)

    @property
    def locList(self)->list:
        return self._locList

    @property
    def start_loc(self)->Location:
        return self._start_loc

    @start_loc.setter
    def start_loc(self,loc:Location):
        typeCheck(loc,Location)
        self._start_loc = loc

    @property
    def cur_loc(self)->Location:
        return self._cur_loc

    @cur_loc.setter
    def cur_loc(self,loc:Location):
        typeCheck(loc,Location)
        self._cur_loc = loc

    @property
    def testScript(self)->list:
        return self._testScript

    @testScript.setter
    def testScript(self,script:list):
        self._testScript=script
