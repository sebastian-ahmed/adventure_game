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
