class Obstructor():
    '''
        Connections between locations can be obstructed by a variety of objects such as doors, trap or enemies
        Non-resolvable obstructions are supported by leaving resolutionItem undefined or setting to None
        Applications for non-resolvable items are obstacles such as fire which can damage the player but
        do not obstruct passage

    '''
    def __init__(
        self,baseName,
        resolvedStateStr,
        unresolvedStateStr,
        resolutionItem=None,
        canKill=False):
        self._baseName = baseName
        self._resolvedStateStr = resolvedStateStr
        self._unresolvedStateStr = unresolvedStateStr
        self._resolutionItem = resolutionItem
        self._canKill = canKill
        self._resolved = False

        self._item = ''
        if self._resolutionItem == None:
            self._isObstacle = True
        else:
            self._isObstacle = False

    def resolve(self):
        self._resolved = True
    
    def unresolve(self):
        self._resolved = False

    def hasItem(self):
        return self._item != ''

    def setItem(self,item):
        self._item=item

    def getItem(self):
        return self._item

    def description(self):
        if self._resolved:
            return self._resolvedStateStr
        else:
            return self._unresolvedStateStr
    
    def stateStr(self):
        if self.isResolved():
            return (f"{self._resolvedStateStr} {self._baseName}")
        else:
            return (f"{self._unresolvedStateStr} {self._baseName}")

    def isResolved(self):
        return self._resolved

    def canKill(self):
        return self._canKill

    def isObstacle(self):
        return self._isObstacle

    def useItem(self,item):
        if self.isResolved() or self._resolutionItem != item or self.isObstacle():
            print(f"Using {item} on {self._baseName} has no effect")
            return False
        elif self._resolutionItem == item:
            print(f"Success! {self._baseName} is now {self._resolvedStateStr}")
            if self.hasItem():
                print(f"{self._baseName} dropped {self._item} on the floor")
            self.resolve()
            return True
