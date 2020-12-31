import random as random
import pickle
from os import path

from adventure_pkg.modules.Connector   import Connector
from adventure_pkg.modules.Location    import Location, gameItems
from adventure_pkg.modules.Player      import Player
from adventure_pkg.modules.Level       import Level
from adventure_pkg.modules.Utils       import GameError

class Adventure(object):
    '''
    This is the game-execution state class of Adventure. It is bound to a Level and Player
    object during initialization. It thus contains all the necessary state of a game allowing
    a game to be saved or loaded fully based on an object of this class.
    An object of this class uses flags to communicate with the client game loop
    This class also contains all relevant methods to manipulate the game-world such as moving
    the player, interactions with obstructions and mechanics of item movement between player
    and locations.
    '''

    fname='saved-game' # Filename for saved game

    def __init__(self,level:Level,player:Player):

        self._level  = level
        self._player = player

        # These are base flags used by this class, but there is an ability
        # to add additional flags during run-time for customizations or customizations
        # via the level files (advanced usage)
        # Because this class is comprised of flags which can be dynamically added,
        # we add more precise error reporting
        self._flags = {
            'moved'        : False, # Flag that location has changed
            'checkHealth'  : False, # Flag that game app should do a health check on player
            'disableDamage': False, # Flag which disables player damage
            'waitForEnter' : False  # Flag that requests game app to pause the screen
        }

    @property
    def level(self)->Level:
        return self._level
    
    @level.setter
    def level(self,level:Level):
        self._level = level

    @property
    def player(self)->Player:
        return self._player

    @player.setter
    def player(self,player:Player):
        self._player = player

    def save(self,auxObject=None):
        '''
        Besides saving this object, this method allows adding an arbitraty object to form
        a tuple consisting of self and and arbitrary object
        '''
        print("Saving game to save-file")
        with open(Adventure.fname,'wb') as f:
            pickle.dump((self,auxObject),f)

    @staticmethod
    def checkSave()->bool:
        return path.exists(Adventure.fname)

    @staticmethod
    def load()->list:
        '''
        Since the save method may have included an auxillary object, this method can 
        be assumed to return a tuple consisting of an Adventure object and a secondary
        object. The tuple is thus (Adventure,x) where x can be any object or None type
        '''
        print("Loading game from save-file")
        with open(Adventure.fname,'rb') as f:
            return pickle.load(f)

    def moveToLocation(self,direction:str):
        '''
            This function performs a move operation.
            If a successful move is achieved update the level.cur_loc handle
            otherwise we leave it unchanged
            If the move is made to an obstruction that can damage the player, we perform
            damage operations and update the state object for the game to do a health 
            check.
            In summary things that can happen in this action function:
            - The location pointed to by level.cur_loc is updated or left un-changed
            - The player's health is reduced
            - In the case of an "obstacled" path the location pointed to by level.cur_loc is updated
              and the player's health is reduced
        '''
        self.clearFlags(['moved','checkHealth'])
        if direction in self.level.cur_loc._con:
            if self.level.cur_loc._con[direction]._locHandle != None:
                if self.level.cur_loc.dirIsObstructed(direction):
                    obstruction=self.level.cur_loc._con[direction]._obsHandle.stateStr()
                    if self.level.cur_loc.dirIsObstacled(direction):
                        print(f"{direction} is endangered by {obstruction}")
                    else:
                        print(f"{direction} is obstructed by {obstruction}")
                    if self.level.cur_loc._con[direction]._obsHandle.canKill() and self.getFlag('disableDamage')==False:
                        damage = Adventure.getRandDamage()
                        self._player.reduceHealth(damage)
                        print(f"{self._player._name} suffered {damage} points of damage from {obstruction}!")
                        print(f"Use the 'look' command to check for obstacles and dangers")
                        self.setFlag('checkHealth')
                    if self.level.cur_loc.dirIsObstacled(direction):
                        print(f"Going to {direction}")
                        self.setFlag('moved')
                        if self.getFlag('disableDamage')==False:
                            self.setFlag('waitForEnter')
                        self.level.cur_loc = self.level.cur_loc._con[direction]._locHandle
                        return
                    else:
                        return
                else:
                    print(f"Going to {direction}")
                    self.setFlag('moved')
                    self.level.cur_loc = self.level.cur_loc._con[direction]._locHandle
                    return
            else:
                print("Can't go there")
                self.level.cur_loc.printDirections()
                return
        else:
            raise GameError(f"{__name__} : un-supported direction string")

    def xferItemToPlayer (self,item):
        if not item in self.level.cur_loc._items:
            print(f"Item {item} does not exist in this location. Take a 'look' first")
            return
        if self._player.takeItem(item):
            self.level.cur_loc.removeItem(item)

    def xferItemToLoc (self,item):
        if self._player.dropItem(item):
            self.level.cur_loc.addItem(item)

    def useItemOnSelf(self,item)->bool:
        if not self._player.hasItem(item):
            print(f"You do not have a '{item}'")
            return False
        else:
            if item == gameItems['healthpack']:
                health = Adventure.getRandDamage()
                self._player.increaseHealth(health)
                print(f"{self._player._name} got {health} points of health from {gameItems['healthpack']}!")
                self.setFlag('checkHealth')
                self._player.removeItem(gameItems['healthpack'])
                return True
            else:
                print(f"'{item}' has no effect on you")
                return False

    def useItemOnObstructor(self,item,obsName:str)->bool:
        if not self.level.cur_loc.obstructorExists(obsName):
            print(f"There is no {obsName} in this location")
            return False
        if not self._player.hasItem(item):
            print(f"You do not have a '{item}'")
            return False
        else:
            obsHandle = self.level.cur_loc.obsName2Handle(obsName)
            if obsHandle.useItem(item) == True:
                self._player.removeItem(item)
                # Some obstructions drop items when resolved
                if obsHandle.hasItem() == True:
                    self.level.cur_loc.addItem(obsHandle.getItem())
                return True

    def checkFlag(self,flagName):
        if flagName in self._flags:
            return True
        else:
            raise GameError(f"{__name__} : trying to access undefined flagName {flagName}")
            
    def setFlag(self,flagName):
        if self.checkFlag(flagName):
            self._flags[flagName]=True
            
    def setFlags(self,flagsList):
        for flag in flagsList:
            self.setFlag(flag)

    def getFlag(self,flagName):
        if self.checkFlag(flagName):
            return self._flags[flagName]

    def clearFlag(self,flagName):
        if self.checkFlag(flagName):
            self._flags[flagName]=False

    def clearFlags(self,flagsList):
        for flag in flagsList:
            self.clearFlag(flag)

    def clearAllFlags(self):
        for flag in self._flags.keys():
            self._flags[flag]=False

    def addFlag(self,flagName):
        if not flagName in self._flags:
            self._flags[flagName]=False

    def printFlags(self):
        print(self._flags)

    @staticmethod
    def getRandDamage()->int:
        '''
            Uses probabilities to determine how much health
            damage should occur to Player
        '''
        return random.randint(20,50)