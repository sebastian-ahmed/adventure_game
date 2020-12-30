
#!/usr/bin/env python3

import os
from os import path
import re
import time
import json
import importlib
import pickle
from adventure_pkg.modules.Adventure   import Adventure
from adventure_pkg.modules.GUIWindow   import GUIWindow
from adventure_pkg.modules.Player      import Player
from adventure_pkg.modules.Level       import Level
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
    print("save (saves current game to saved-game)")
    print("load (loads saved game from saved-game)")
    print("h|help (print this message)")
    print("q|quit|exit (exits the game)\n")

def clearScreen(delay):
    time.sleep(delay)
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class InputManager(object):
    '''
    Provides a context-managed management layer for user input:
    - Selecting input from the terminal or from replay-script object
    - Processing user input (with regular expression matching) against supported commands
    - Logging of action commands
    - Dumping of action commands to JSON file (for level testing in scripted mode)
      - Dumping can be called by the user otherwise happens when this object goes out of scope
    '''

    def __init__(self,scripted:bool=False,script:PlayScript=None):
        self._scripted = scripted
        self._script   = script
        self._log      = [] # input log

    def __enter__(self):
        return self
    
    def __exit__(self,*args):
        '''
        Attempt to dump action history upon exiting scope
        '''
        self.dump()

    matchDict = {
        'quit':       r'^[qQ]uit$|^[qQ]$|^[eE]xit$',
        'help':       r'^[hH]elp$|^[hH]$|$',
        'look':       r'^[lL]ook$',
        'hint':       r'^[hH]int$',
        'inv':        r'^[iI]nv(?:entory)*$',
        'trace':      r'^[tT]race$',
        'dump':       r'^[dD]ump$',
        'use_self':   r'^[uU]se\s+([a-zA-Z0-9\-_]+)$',
        'use_object': r'^[uU]se\s+(?:the\s+)*([a-zA-Z0-9\-_]+)\s+(?:on\s+)*(?:the\s+)*([a-zA-Z0-9\-_]+)',
        'go':         r'^[gG]o\s+(?:to\s+)*([a-zA-Z0-9\-_]+)',
        'take':       r'^(?:[tT]ake|[gG]et)\s+(?:the\s+)*([a-zA-Z0-9\-_]+)',
        'drop':       r'^[dD]rop\s+(?:the\s+)*([a-zA-Z0-9\-_]+)',
        'save':       r'^[sS]ave',
        'load':       r'^[lL]oad'
    }

    def procUserInput (self,inString)->list:
        for command,exp in InputManager.matchDict.items():
            mobj = re.compile(exp)
            matches = mobj.match(inString)
            if (matches):
                return command,list(matches.groups())
        return 'invalid',[]

    def getInput(self,inputStr:str,logged:bool=True):
        if self._scripted:
            script_input = next(self._script)
            print(inputStr+script_input)
            return script_input
        else:
            # Support logging for non-scripted mode only
            user_input = input(inputStr)
            if logged==True:
                if self.procUserInput(user_input)[0] in ['dump','exit','save','invalid']:
                    pass
                else:
                    self._log.append(user_input)
            return user_input

    def dump(self):
        log_file = 'input-log.json'
        print(f"Dumping out player history to {log_file}")
        with open(log_file,'w') as f:
            json.dump(self._log,f,indent=4)

class GameState(object):
    '''
    Wrapper object which wraps the game objects to enable saving and loading of a game
    '''

    def __init__(self,level:Level,player:Player,state:ActionState):
        self._levelHandle  = level
        self._playerHandle = player
        self._stateHandle  = state

    fname='saved-game'

    @property
    def level(self)->Level:
        return self._levelHandle

    @property
    def player(self)->Player:
        return self._playerHandle

    @property
    def state(self)->ActionState:
        return self._stateHandle

    def save(self):
        print("Saving game to save-file")
        with open(GameState.fname,'wb') as f:
            pickle.dump(self,f)

    @staticmethod
    def checkSave()->bool:
        return path.exists(GameState.fname)

    @staticmethod
    def load():
        print("Loading game from save-file")
        with open(GameState.fname,'rb') as f:
            return pickle.load(f)


###############################################################################
# Main game code
###############################################################################

def game_loop(inputManager,guiEnable=True,scriptedMode:bool=False,scriptObj=None,configObj=None):
    if not scriptedMode:
        clearScreen(0)
        splashScreen()

    userInputStr = ''
    if GameState.checkSave():
        userInputStr = inputManager.getInput("\nA saved game was found, would you like to load it? (default=no):",logged=False)
    if userInputStr in ['y','Y','yes','Yes','YES']:
        game = GameState.load()
        game.state.setFlags(['waitForEnter','moved'])
    else:
        iname = inputManager.getInput("Please enter your name:",logged=False)
        # Create a player object
        player = Player(iname)
        welcomeMsg(player)
    
        # Create game-state object
        state = ActionState()

        # Select level
        levelsDict = utils.readLevelJSON()
        full_level_name = "adventure_pkg.levels."
        if scriptedMode:
            full_level_name += configObj.levelName
        else:
            full_level_name += utils.getLevelFromUser(levelsDict) 
        level = importlib.import_module(full_level_name).level

        # Give option to turn off damage model
        userInputStr = inputManager.getInput("\nDisable in-game damage to player (y/n)? (default=no):",logged=False)
        if userInputStr in ['y','Y','yes','Yes','YES']:
            state.setFlag('disableDamage')

        # Wrap the player objects with wrapping class so we can easily save or load
        # a save-game
        game = GameState(level,player,state)
        game.level.cur_loc = game.level.start_loc

    if guiEnable:
        # Instantiate a GUIWindow object
        gui = GUIWindow(f"Adventure {gameVersion}")

    # Initialize
    game.state.setFlag('moved')
    redrawFlag = True

    # Create an Adventure object and provide Player and State object handles via the
    # wrapping object
    adv = Adventure(game.player,game.state)

    while True:
        if game.state.getFlag('checkHealth'):
            if game.player.isDead() :
                print(f"Too much damage, {game.player._name} is dead! Game Over")
                if guiEnable:
                    gui.playerDeadWindow(game.player)
                break
            else:
                game.player.printHealth()
                game.state.clearFlags(['checkHealth'])
        if game.state.getFlag('moved'):
            redrawFlag == True
            if game.state.getFlag('waitForEnter'):
                waitEnter(scriptedMode)
            if not scriptedMode:
                clearScreen(1)
            game.state.clearFlags(['moved','checkHealth','waitForEnter'])
            game.level.cur_loc.printDescription()
            if game.level.cur_loc.isEndLocation():
                print(f"Congratulations {game.player._name}, you have escaped! Game Over")
                if guiEnable:
                    gui.gameOverWindow(game.player)
                break
            else:
                game.level.cur_loc.printDirections()
        if redrawFlag and guiEnable:
            gui.updateWindow(game.level.cur_loc,game.player)
            redrawFlag==False
        userInputStr = inputManager.getInput(f"Enter action {game.player._name}:")
        # We use regular expressions to deal with some variability in user input
        command, args = inputManager.procUserInput(userInputStr)
        if command == 'quit':
            print(f"Exiting ... thanks for playing the game {game.player._name}")
            break
        if command == 'go':
            if args[0] in ['f','forward','up']:
                game.level.cur_loc = adv.moveToLocation(game.level.cur_loc,'forward')
                continue
            elif args[0] in ['b','back','backward','down']:
                game.level.cur_loc = adv.moveToLocation(game.level.cur_loc,'backward')
                continue
            elif args[0] in ['l','left']:
                game.level.cur_loc = adv.moveToLocation(game.level.cur_loc,'left')
                continue
            elif args[0] in ['r','right']:
                game.level.cur_loc = adv.moveToLocation(game.level.cur_loc,'right')
                continue
            else:
                print(f"{args[0]} is not a valid direction to go")
                continue
        elif command == 'look':
            game.level.cur_loc.look()
            game.level.cur_loc.printDirections()
            continue
        elif command == 'hint':
            game.level.cur_loc.printHint()
        elif command == 'take':
            adv.xferItemToPlayer(game.level.cur_loc,args[0])
            redrawFlag==True
        elif command == 'drop':
            adv.xferItemToLoc(game.level.cur_loc,args[0])
            redrawFlag==True
        elif command == 'use_object':
            if adv.useItemOnObstructor(game.level.cur_loc,args[0],args[1]):
                redrawFlag==True
            continue
        elif command == 'use_self':
            if adv.useItemOnSelf(game.level.cur_loc,args[0]):
                redrawFlag==True
            continue
        elif command == 'inv':
            game.player.printInv()
        elif command == 'help':
            helpMsg()
        elif command == 'trace':
            utils.debugPrintGraph(game.level.cur_loc)
        elif command == 'dump':
            inputManager.dump()
        elif command == 'save':
            game.save()
        elif command == 'load':
            if not GameState.checkSave():
                print(f"Game save file '{GameState.fname}' found")
            else:
                game = GameState.load()
                game.state.setFlags(['waitForEnter','moved'])
                # This is a bit of a hack because otherwise adv maintains handles to the 
                # previous Player and ActionState objects. An improvement needs to to be made
                # to encapsulate all game state objects in one place
                adv=Adventure(game.player,game.state)
            continue
        else:
            print("I did not understand the action, type 'help' for list of commands")
            pass

    if scriptedMode:
        return not game.player.isDead()
    else:
        waitEnter()

def main(guiEnable=True,scriptedMode:bool=False,scriptObj=None,configObj=None):

    # Initialize an InputManager object to handle game inputs
    with InputManager(scripted=scriptedMode,script=scriptObj) as inputManager:
        return game_loop(inputManager,guiEnable,scriptedMode,scriptObj,configObj)

if __name__ == '__main__':
    main()
