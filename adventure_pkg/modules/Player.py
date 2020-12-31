from adventure_pkg.modules.Utils import GameError

class Player():
    '''
        The Player class is intended to be a single instance object as the player of
        the game. The player has an inventory which can hold items. Items can move between
        the Player object and a Location object. The Player also has a health of 100 points
        which can be increased or reduced.
    '''

    def __init__(self,name):
        self._name = name
        self._inv  = {
            'slot0':'',
            'slot1':'',
            'slot2':'',
            'slot3':''
        }
        self._invCount = 0
        self._invMaxCount = 4
        self._health = 100

    def hasEmptySlots(self)->bool:
        return (self._invCount != self._invMaxCount)

    def takeItem(self,item)->bool:
        if (self._invCount == self._invMaxCount):
            print(f"Cannot add any more items, max of {self._invMaxCount} items reached")
            return False
        else:
            print(f"Picked up {item}")
            for key in self._inv.keys():
                if self._inv[key] == '':
                    self._inv[key] = item
                    self._invCount += 1
                    return True

    def hasItem(self,item):
        if item in self._inv.values():
            return True
        else:
            return False

    def removeItem(self,item):
        if not self.hasItem(item):
            raise GameError(f"Trying to remove item '{item}' which player does not have")
        else:
            # We make sure to only remove one instance of a duplicate item
            # by returning after the first match
            for key in self._inv.keys():
                if self._inv[key] == item:
                    self._inv[key] = ''
                    self._invCount -= 1
                    return

    def dropItem(self,item):
        if not self.hasItem(item):
            print(f"{self._name}, you do not have '{item}' in your inventory")
            return False
        else:
            print(f"Dropping {item}")
            self.removeItem(item)
            return True

    def printInv(self):
        print(f"{self._name}'s Inventory:")
        for k,v in self._inv.items():
            if v=='':
                print(f"   {k} : empty slot")       
            else:
                print(f"   {k} : {v}")
        self.printHealth()

    def printHealth(self):
        print(f"{self._name}'s health is {self.getHealth()}/100 points")

    def getHealth(self)->int:
        return self._health
    
    def isDead(self)->bool:
        return (self._health == 0)
    
    def reduceHealth(self,amount):
        self._health = max(self._health - amount,0)
        
    def increaseHealth(self,amount):
        self._health = min(self._health + amount,100)
