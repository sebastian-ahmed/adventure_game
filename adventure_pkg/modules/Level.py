from adventure_pkg.modules.Location   import Location
from adventure_pkg.modules.Utils      import typeCheck

class Level(object):
    '''
    Encapsulates a level object : a list of Location objects
    '''

    def __init__(self,name:str='unnamed'):
        self._name      = name # String name for this level
        self._locList   = []   # List of locations for this level
        self._start_loc = None # A handle to a starting location object

    def locAdd (self,loc:Location):
        typeCheck(loc,Location)
        self._locList.append(loc)

    @property
    def size(self)->int:
        return len(self._locList)

    @property
    def locList(self)->list:
        return self._locList

    @property
    def start_loc(self)->Location:
        return self._start_loc

    @start_loc.setter
    def start_loc(self,loc:Location):
        typeCheck(loc,Location)
        self._start_loc = loc
