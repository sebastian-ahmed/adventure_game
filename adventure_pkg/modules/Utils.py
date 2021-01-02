# Copyright 2020 Sebastian Ahmed
# This file, and derivatives thereof are licensed under the Apache License, Version 2.0 (the "License");
# Use of this file means you agree to the terms and conditions of the license and are in full compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, EITHER EXPRESSED OR IMPLIED.
# See the License for the specific language governing permissions and limitations under the License.

import json
import pathlib

class GameError(Exception):
    '''
        This is essentially a named exception which is intended
        to be used as a general game error
    '''
    def __init__(self,errorStr):
        super().__init__(self,"{0}".format(errorStr))

def typeCheck(arg,ctype):
    if not isinstance(arg,ctype):
        raise GameError(f"{__name__} : Specified argument {arg} was not of type {type(ctype).__name__}")

###############################################################################
# Functions for level file management
###############################################################################
def readLevelJSON()->dict:
    path = pathlib.Path(__file__).parent.parent.parent.absolute()/"levels.json"
    with open(path,'r') as f:
        levelsDict = json.load(f)
    return levelsDict

def getLevelFromUser(lvlDict)->str:
    print("\nPlease select a level from the list below\n")
    for lvl in lvlDict.keys():
        print(f"{lvl} : {lvlDict[lvl]}")
    while True:
        lvl_name=input("\nType the level name and press ENTER:")
        if (lvl_name not in lvlDict):
            print(f"This is not a valid level choice. Available choices are : {[x for x in lvlDict.keys()]}")
        else:
            return lvl_name

def recPrintGraph(startLoc,visitedLocList,reqDepth):
    '''
        This function should only be called by a wrapping function
        which initializes all the parameters
        Iterates and recurses through entire location connectivity graph
        prints output during traversal and appends reachable locations
        into visitedLocList
        reqDepth allows recursion to keep track of recursion depth for
        indendation of formatting
    '''
    reqDepth += 1
    for direction in startLoc._con.keys():
        listStr = f"{startLoc._name}:{direction}"
        visitedLocList.append(startLoc._name)
        indentStr = reqDepth * "  "
        print(f"{indentStr}{reqDepth}:{listStr}->", end="")
        if (startLoc._con[direction]._locHandle == None):
            print(f" Terminate(NONE)")
            # This is a bit of a hack to detect last iteration
            if direction == 'right':
                reqDepth -= 1
        else:
            nextLocName = startLoc._con[direction]._locHandle._name
            if not nextLocName in visitedLocList:
                print("\n")
                recPrintGraph(startLoc._con[direction]._locHandle,visitedLocList,reqDepth)
            else:
                print(f"{nextLocName}-> Terminate(Wrap-around)")
                #This is a bit of a hack to detect last iteration
                if direction == 'right':
                    reqDepth -= 1
    reqDepth -= 1

def debugPrintGraph(startLoc):
    '''
        Wrapping function to initialize parameters for recursive graphing
        of locator objects in a location graph
        The returned lists contains all discovered locations in the graph
    '''
    visitedLocList = []
    reqDepth = 0
    recPrintGraph(startLoc,visitedLocList,reqDepth)
    return visitedLocList