import random as random

from adventure_pkg.modules.Connector   import Connector
from adventure_pkg.modules.Location    import Location, gameItems
from adventure_pkg.modules.Player      import Player
from adventure_pkg.modules.ActionState import ActionState
from adventure_pkg.modules.Utils       import GameError

class Adventure(object):
    def __init__(self,player:Player,state:ActionState):
        self._player        = player
        self._state         = state

    def moveToLocation(self,loc:Location,direction:str)->Location:
        '''
            This function performs actions on Player and ActionState objects and returns
            a location handle.
            If a successful move is achieved, we return a handle to the moved-to location
            otherwise we return the input location handle
            If the move is made to an obstruction that can damage the player, we perform
            damage operations and update the state object for the game to do a health 
            check.
            In summary things that can happen in this action function:
            - The location handle is updated or returned un-changed
            - The player's health is reduced
            - In the case of an "obstacled" path the location handle is updated
              and the player's health is reduced
        '''
        self._state.clearFlags(['moved','checkHealth'])
        if direction in loc._con:
            if loc._con[direction]._locHandle != None:
                if loc.dirIsObstructed(direction):
                    obstruction=loc._con[direction]._obsHandle.stateStr()
                    if loc.dirIsObstacled(direction):
                        print(f"{direction} is endangered by {obstruction}")
                    else:
                        print(f"{direction} is obstructed by {obstruction}")
                    if loc._con[direction]._obsHandle.canKill() and self._state.getFlag('disableDamage')==False:
                        damage = Adventure.getRandDamage()
                        self._player.reduceHealth(damage)
                        print(f"{self._player._name} suffered {damage} points of damage from {obstruction}!")
                        print(f"Use the 'look' command to check for obstacles and dangers")
                        self._state.setFlag('checkHealth')
                    if loc.dirIsObstacled(direction):
                        print(f"Going to {direction}")
                        self._state.setFlag('moved')
                        if self._state.getFlag('disableDamage')==False:
                            self._state.setFlag('waitForEnter')
                        return loc._con[direction]._locHandle
                    else:
                        return loc
                else:
                    print(f"Going to {direction}")
                    self._state.setFlag('moved')
                    return loc._con[direction]._locHandle
            else:
                print("Can't go there")
                loc.printDirections()
                return loc
        else:
            raise GameError(f"{__name__} : un-supported direction string")

    def xferItemToPlayer (self,loc:Location,item):
        if not item in loc._items:
            print(f"Item {item} does not exist in this location. Take a 'look' first")
            return
        if self._player.takeItem(item):
            loc.removeItem(item)

    def xferItemToLoc (self,loc:Location,item):
        if self._player.dropItem(item):
            loc.addItem(item)

    def useItemOnSelf(self,loc:Location,item):
        if not self._player.hasItem(item):
            print(f"You do not have a '{item}'")
            return False
        else:
            if item == gameItems['healthpack']:
                health = Adventure.getRandDamage()
                self._player.increaseHealth(health)
                print(f"{self._player._name} got {health} points of health from {gameItems['healthpack']}!")
                self._state.setFlag('checkHealth')
                self._player.removeItem(gameItems['healthpack'])
                return True
            else:
                print(f"'{item}' has no effect on you")
                return False

    def useItemOnObstructor(self,loc:Location,item,obsName:str)->bool:
        if not loc.obstructorExists(obsName):
            print(f"There is no {obsName} in this location")
            return False
        if not self._player.hasItem(item):
            print(f"You do not have a '{item}'")
            return False
        else:
            obsHandle = loc.obsName2Handle(obsName)
            if obsHandle.useItem(item) == True:
                self._player.removeItem(item)
                # Some obstructions drop items when resolved
                if obsHandle.hasItem() == True:
                    loc.addItem(obsHandle.getItem())
                return True

    @staticmethod
    def getRandDamage()->int:
        '''
            Uses probabilities to determine how much health
            damage should occur to Player
        '''
        #return random.choices([True,False],[0.2,0.8])[0]
        return random.randint(20,50)