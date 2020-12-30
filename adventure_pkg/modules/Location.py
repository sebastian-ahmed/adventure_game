from adventure_pkg.modules.Obstructor import Obstructor
from adventure_pkg.modules.Connector  import Connector
from adventure_pkg.modules.Utils      import GameError

# Special game items (non user-defined)
gameItems = {'healthpack':'healthpack'}

class Location():
    '''
        The Location class defines locations in the game world.
        Location's can:
          - connect to other locations via their 4 directions
          - have Obstacles bound to their directions
          - contain items which can pass to/from Player

        Location is basically is a pseudo-composite OO pattern, because it does not inherit an
        interface class and yet can present a full graph of Locations objects via its four
        "connectors"
    '''

    def __init__(self,name='unnamed location',endLocation=False):
        
        # Connections
        self._con = {
            'backward': Connector(None,None),
            'forward' : Connector(None,None),
            'left'    : Connector(None,None),
            'right'   : Connector(None,None)
        }
        
        # Name, Description
        self._name = name
        self._description = ''
        self._hint = 'This location does not have any hints'
        self._isDescribed = False
    
        # Items (e.g. keys, weapons)
        self._items = []

        # End game location flag
        self._endLocation = endLocation

    @property
    def name(self)->str:
        return self._name

    @property
    def description(self)->str:
        return self._description

    @property
    def hint(self)->str:
        return self._hint

    @property
    def items(self)->list:
        return self._items

    @staticmethod
    def connect(a,dir_a,b,dir_b=None,obs=None):
        '''
            Connect two Location objects with optional obstructor. Note that we
            make the connection on both Locations as well as making sure obstructions
            are bound to both sides

            In the case where a direction for location "b" is not specified we
            assume b's connector to be the opposite direction of the a connector
            This would be considered a reciprocating connection
            Non-reciprocating connections must specify dir_b (e.g. right of B connects to back of A)
        '''

        a._con[dir_a]._locHandle = b
        a._con[dir_a]._obsHandle = obs
        if dir_b == None:
            b._con[Location.getOppConnector(dir_a)]._locHandle = a
            b._con[Location.getOppConnector(dir_a)]._obsHandle = obs
        else:
            b._con[dir_b]._locHandle = a
            b._con[dir_b]._obsHandle    = obs

    @staticmethod
    def getOppConnector (direction):
        '''
            This function provides a connecter in the opposite direction to
            allow the connection API to not require bi-directional connection
            statements in normal "reciprocating" connections 
            (e.g. a left of A connects to a right of B, where the right of B is implied)
        '''

        if direction == 'left':
            return 'right'
        elif direction == 'right':
            return 'left'
        elif direction == 'forward':
            return 'backward'
        elif direction == 'backward':
            return 'forward'
        else:
            return 'UNDEFINED'

    def dirHasConnection(self,direction):
        if self._con[direction]._locHandle != None:
            return True
        return False

    def hasAnyConnections(self):
        for direction in self._con:
            if self.dirHasConnection(direction):
                return True
        return False

    def isEndLocation(self):
        return self._endLocation

    def setDescription (self,Description):
        self._description=Description
        self._isDescribed = True

    def printDescription(self):
        if self._isDescribed == True:
            print(self._description)
        else:
            print("This location has no description")

    def setHint(self,hint):
        self._hint=hint

    def getHint(self,hint):
        return self._hint

    def printHint(self):
        print(self._hint)

    def printDirections (self):
        valid_directions = [dir for dir in self._con.keys() if self._con[dir]._locHandle != None]
        print(f"Possible ways to go are: {valid_directions}")

    def dirHasObstructor(self,direction):
        return (self._con[direction]._obsHandle != None)

    def dirIsObstructed(self,direction):
        if self.dirHasObstructor(direction) == False or self._con[direction]._obsHandle.isResolved() == True:
            return False
        else:
            return True

    def dirIsObstacled(self,direction):
        if self.dirHasObstructor(direction):
            return self._con[direction]._obsHandle.isObstacle()
        else:
            return False

    def dirObstructorStr(self,direction):
        if self.dirHasObstructor(direction):
            return self._con[direction]._obsHandle.stateStr()
        else:
            return ''

    def obstructorExists(self,obstructorName):
        '''
        Does a specified obstuctor exist on any of the connectors
        in this location
        '''
        for x in self._con.keys():
            if (self._con[x]._obsHandle != None):
                if (self._con[x]._obsHandle._baseName == obstructorName):
                    return True
        return False

    def obsName2Handle(self,obstructorName):
       for direction in self._con.keys():
           if self.dirHasObstructor(direction):
               if (self._con[direction]._obsHandle._baseName == obstructorName):
                   return self._con[direction]._obsHandle
       return None

    def look(self):
        valid_directions = [dir for dir in self._con.keys() if self._con[dir]._locHandle != None]
        for dir in valid_directions:
            if self.dirHasObstructor(dir):
                print(f"In the {dir} direction you see a {self._con[dir]._obsHandle.stateStr()}")
            else:
                print(f"In the {dir} direction you see a clear path")

        if not self._items:
            print ("There is nothing here to pick up")
        else:
            print(f"I see the following things to pick up:")
            for item in  self._items:
                print(f"   {item}")

    def addItem(self,item):
        if not item in self._items:
            self._items.append(item)

    def addGameItem(self,item):
        if item in gameItems.keys():
            # Allow multiple instances
            self._items.append(item)
        else:
            raise GameError(f"{__name__} : Trying to add un-supported game item {item}")

    def removeItem(self,item):
        if item in self._items:
            self._items.remove(item)
