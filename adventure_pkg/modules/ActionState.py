from adventure_pkg.modules.Utils import GameError

class ActionState():
    '''
        This is an auxillary class to encapsulate dynamic state of the game which
        is the result of actions such as moving or using an item

        There are base flags used by the main game engine, but there is an ability
        to add additional flags during run-time for customizations or customizations
        via the level files (advanced usage)

        Because this class is comprised of flags which can be dynamically added,
        we add more precise error reporting
    '''
    def __init__(self):
        self._flags = {
            'moved'        : False, # Flag that location has changed
            'checkHealth'  : False, # Flag that game app should do a health check on player
            'disableDamage': False, # Flag which disables player damage
            'waitForEnter' : False  # Flag that requests game app to pause the screen
        }

    def checkFlag(self,flagName):
        if flagName in self._flags:
            return True
        else:
            raise GameError(f"{__name__} : trying to access undefined flagName")
            
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


