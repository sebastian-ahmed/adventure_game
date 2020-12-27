
#!/usr/bin/env python3

import os
import re
import time
import json
import importlib
from adventure_pkg.modules.Adventure   import Adventure
from adventure_pkg.modules.GUIWindow   import GUIWindow
from adventure_pkg.modules.Player      import Player
from adventure_pkg.modules.ActionState import ActionState
from adventure_pkg.modules             import Utils as utils
from adventure_pkg.modules.TestClasses import GameConfig,PlayScript

gameVersion = '1.0'

def splashScreen():
    print("\n\n")
    print("******************************************")
    print("*                                        *")
    print(f"*              Adventure {gameVersion}             *")
    print("*          (c) 2020 Ahmed Family         *")
    print("*                                        *")
    print("*                                        *")
    print("******************************************")
    print("\n\n")

def welcomeMsg(player):
    print(f"\nWelcome to the game {player._name}!\n")

def waitEnter(skip:bool=False):
    if not skip:
        input("Press ENTER to continue")

def helpMsg():
    print("\nThe text-driven command-line interface of Adventure can take variation in user input")
    print("in order to make game play more smooth, for example the following commands are equivalent:")
    print("\t use key door")
    print("\t use key on door")
    print("\t use key on the door")
    print("\t use the key on the door")
    print("\nList of possible commands (supporting variations):")
    print("go f|forward|b|backward|l|left|r|right  (moves player to that direction). For example")
    print("\t go f     (will go forward)")
    print("inv (lists player inventory and health)")
    print("look (look around the location)")
    print("hint (print hint for this location)")
    print("take|get <item> (take an item in the room])")
    print("drop <item> (drop an item in your inventory)")
    print("use <item> (on) <object> (Use an item in player inventory on object such as door or enemy)")
    print("use <item> (Use an item directly such as food)")
    print("h|help (print this message)")
    print("q|quit|exit (exits the game)\n")

def clearScreen(delay):
    time.sleep(delay)
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def procUserInput (inString):

    matchDict = {
        'quit':       r'^[qQ]uit$|^[qQ]$|$|^[eE]xit$',
        'help':       r'^[hH]elp$|^[hH]$|$',
        'look':       r'^[lL]ook$',
        'hint':       r'^[hH]int$',
        'inv':        r'^[iI]nv(?:entory)*$',
        'trace':      r'^[tT]race$',
        'use_self':   r'^[uU]se\s+([a-zA-Z0-9\-_]+)$',
        'use_object': r'^[uU]se\s+(?:the\s+)*([a-zA-Z0-9\-_]+)\s+(?:on\s+)*(?:the\s+)*([a-zA-Z0-9\-_]+)',
        'go':         r'^[gG]o\s+(?:to\s+)*([a-zA-Z0-9\-_]+)',
        'take':       r'^(?:[tT]ake|[gG]et)\s+(?:the\s+)*([a-zA-Z0-9\-_]+)',
        'drop':       r'^[dD]rop\s+(?:the\s+)*([a-zA-Z0-9\-_]+)'
    }

    for command,exp in matchDict.items():
        mobj = re.compile(exp)
        matches = mobj.match(inString)
        if (matches):
            return command,list(matches.groups())
    return 'invalid',[]


def getInput(inputStr:str='',scripted:bool=True,scriptObj:PlayScript=None)->str:
    if scripted:
        print(inputStr)
        return next(scriptObj)
    else:
        return input(inputStr)

###############################################################################
# Main game code
###############################################################################

def main(guiEnable=True,scriptedMode:bool=False,scriptObj=None,configObj=None):
    if not scriptedMode:
        clearScreen(0)
        splashScreen()
    iname = getInput("Please enter your name:",scriptedMode,scriptObj)
    # Create a player object
    player = Player(iname)
    welcomeMsg(player)
 
    # Create game-state object
    state = ActionState()

    # Create an Adventure object and provide Player and State object handles
    adv = Adventure(player,state)

    # Select level
    levelsDict = utils.readLevelJSON()
    full_level_name = "adventure_pkg.levels."
    if scriptedMode:
        full_level_name += configObj.levelName
    else:
        full_level_name += utils.getLevelFromUser(levelsDict) 
    level = importlib.import_module(full_level_name)

    # Give option to turn off damage model
    userInputStr = getInput("\nDisable in-game damage to player (y/n)? (default=no):",scriptedMode,scriptObj)
    if userInputStr in ['y','Y','yes','Yes','YES']:
        state.setFlag('disableDamage')

    if guiEnable:
        # Instantiate a GUIWindow object
        gui = GUIWindow(f"Adventure {gameVersion}")

    # Initialize
    state.setFlag('moved')
    curloc = level.level.start_loc
    redrawFlag = True

    while True:
        if state.getFlag('checkHealth'):
            if player.isDead() :
                print(f"Too much damage, {player._name} is dead! Game Over")
                if guiEnable:
                    gui.playerDeadWindow(player)
                break
            else:
                player.printHealth()
                state.clearFlags(['checkHealth'])
        if state.getFlag('moved'):
            redrawFlag == True
            if state.getFlag('waitForEnter'):
                waitEnter(scriptedMode)
            if not scriptedMode:
                clearScreen(1)
            state.clearFlags(['moved','checkHealth','waitForEnter'])
            curloc.printDescription()
            if curloc.isEndLocation():
                print(f"Congratulations {player._name}, you have escaped! Game Over")
                if guiEnable:
                    gui.gameOverWindow(player)
                break
            else:
                curloc.printDirections()
        if redrawFlag and guiEnable:
            gui.updateWindow(curloc,player)
            redrawFlag==False
        userInputStr = getInput(f"Enter action {player._name}:",scriptedMode,scriptObj)
        # We use regular expressions to deal with some variability in user input
        command, args = procUserInput(userInputStr)
        if command == 'quit':
            print(f"Exiting ... thanks for playing the game {player._name}")
            break
        if command == 'go':
            if args[0] in ['f','forward','up']:
                curloc = adv.moveToLocation(curloc,'forward')
                continue
            elif args[0] in ['b','back','backward','down']:
                curloc = adv.moveToLocation(curloc,'backward')
                continue
            elif args[0] in ['l','left']:
                curloc = adv.moveToLocation(curloc,'left')
                continue
            elif args[0] in ['r','right']:
                curloc = adv.moveToLocation(curloc,'right')
                continue
            else:
                print(f"{args[0]} is not a valid direction to go")
                continue
        elif command == 'look':
            curloc.look()
            curloc.printDirections()
            continue
        elif command == 'hint':
            curloc.printHint()
        elif command == 'take':
            adv.xferItemToPlayer(curloc,args[0])
            redrawFlag==True
        elif command == 'drop':
            adv.xferItemToLoc(curloc,args[0])
            redrawFlag==True
        elif command == 'use_object':
            if adv.useItemOnObstructor(curloc,args[0],args[1]):
                redrawFlag==True
            continue
        elif command == 'use_self':
            if adv.useItemOnSelf(curloc,args[0]):
                redrawFlag==True
            continue
        elif command == 'inv':
            player.printInv()
        elif command == 'help':
            helpMsg()
        elif command == 'trace':
            utils.debugPrintGraph(curloc)
        else:
            print("I did not understand the action, type 'help' for list of commands")
            pass

    if scriptedMode:
        return not player.isDead()
    else:
        waitEnter()

if __name__ == '__main__':
    main()
