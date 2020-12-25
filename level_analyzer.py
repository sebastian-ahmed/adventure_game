#!/usr/bin/env python3

import os
import json
import importlib
from adventure_pkg.modules import Utils as utils

levelsDict =utils.readLevelJSON()
full_level_name = "adventure_pkg.levels." + utils.getLevelFromUser(levelsDict) 
level = importlib.import_module(full_level_name).level
noConnectionsCount = 0
unReachableRooms = 0

for curLoc in level.locList:
    print(f"Level {curLoc._name} has connections = {curLoc.hasAnyConnections()}")
    if not curLoc.hasAnyConnections():
        noConnectionsCount += noConnectionsCount

print("\nConnectivity trace analysis dump:")
tracedLocList = sorted(list(set(utils.debugPrintGraph(level.start_loc))))

print("\nList of registered locations (via level.locList)")
locListNames = [x._name for x in level.locList]
print(sorted(locListNames))

print("\nList of reached locations (via connection trace analysis)")
print(sorted(tracedLocList))

print("\nList of locations registered in level.locLList unreachable by connection trace analysis")
diffAB=list(set(locListNames).difference(set(tracedLocList)))
print(diffAB)

print("\nList of locations reached by connection trace analysis but not registered in level.locLList")
diffBA=list(set(tracedLocList).difference(set(locListNames)))
print(diffBA)

print("=======================================================================")
print("                     Issue Summary and Statistics:")
print("=======================================================================")
print(f"Number of registered locations (via level.locList)          : {len(level.locList)}")
print(f"Number of traced locations     (via trace analysis)         : {len(tracedLocList)}")
print(f"Number of registered locations with no connections          : {noConnectionsCount}")
print(f"Number of registered locations unreachable by trace analysis: {len(diffAB)}")
print(f"Number of traced locations not registered in level.locList  : {len(diffBA)}")

if (os.name == 'nt'):
    input("Hit ENTER to continue")
