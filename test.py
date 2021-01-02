# Copyright 2020 Sebastian Ahmed
# This file, and derivatives thereof are licensed under the Apache License, Version 2.0 (the "License");
# Use of this file means you agree to the terms and conditions of the license and are in full compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, EITHER EXPRESSED OR IMPLIED.
# See the License for the specific language governing permissions and limitations under the License.

import importlib
import adventure_pkg.modules.Utils as utils
import game
from adventure_pkg.modules.TestClasses import GameConfig,PlayScript

def main():
    results={}
    levels = utils.readLevelJSON()
    for level in levels.keys():
        print(f"Loading level:{level}")
        full_level_name = "adventure_pkg.levels." + level 
        levelObject = importlib.import_module(full_level_name).level
        results[levelObject.name]='No script found'
        if levelObject.testScript:
            config = GameConfig(levelName=level,disableDamage=False)
            scriptObj=PlayScript(levelObject.testScript,config)
            #print(scriptObj._script)
            flag = game.main(guiEnable=False,scriptedMode=True,scriptObj=scriptObj,configObj=config)
            print(f"Test result = {flag}")
            results[levelObject.name]=flag

    print("Test Results Summary:")
    print("=====================")
    for level,result in results.items():
        print(f"Level: {level} : Pass={result}")

if __name__ == '__main__':
    main()
