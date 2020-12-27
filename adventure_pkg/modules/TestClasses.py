class GameConfig(object):
    '''
    Class to wrap the player configuration settings for testing
    '''

    def __init__(self,levelName:str='',disableDamage:bool=False):
        self._playerName    ='TestPlayer'
        self._levelName     = levelName
        self._disableDamage = disableDamage
        self._strList       = [self.playerName,self.levelName,self.disableDamage]

    @property
    def strList(self)->list:
        return self._strList

    @property
    def playerName(self)->str:
        return self._playerName

    @playerName.setter
    def playerName(self,name:str):
        self._playerName = name
    
    @property
    def levelName(self)->str:
        return self._levelName
    
    @levelName.setter
    def levelName(self,name):
        self._levelName = name

    @property
    def disableDamage(self)->str:
        if self._disableDamage == True:
            return "y"
        else:
            return "n"

    @disableDamage.setter
    def disableDamage(self,flag:bool):
        self._disableDamage = flag

class PlayScript(object):
    '''
    Sequence class which takes a list of script commands to emulate player terminal commands.
    Initialized with a list of command strings.
   
    StopIteration is raised if the end of the command list is exceeded, so it is important
    that the play script results in ending a level
    '''
    def __init__(self,script:list=[],config:GameConfig=None):
        if GameConfig:# Pre-pend config strings into script
            self._script = config.strList + script
        else:
            self._script = script

    def __next__(self):
        
        if len(self._script) == 0:
            raise StopIteration
        else:
            return self._script.pop(0)

    def __iter__(self):
        return self


