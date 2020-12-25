class Connector():
    '''
        Basic class to connect Locations comprised of a handle to connected Location
        and a handle to an obstruction
        By default a connector is not bound to anything
    '''
    def __init__(self,locHandle=None,obsHandle=None):
        self._locHandle = locHandle
        self._obsHandle = obsHandle
