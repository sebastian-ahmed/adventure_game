from adventure_pkg.modules.Location   import Location
from adventure_pkg.modules.Obstructor import Obstructor
from adventure_pkg.modules.Level      import Level

level = Level("level1")

loc0 = Location("loc0")
loc0.setDescription("You are in the first room. You should take a look around")
level.locAdd(loc0)

loc1 = Location("loc1")
loc1.setDescription("This is location 1")
level.locAdd(loc1)

loc2 = Location("loc2")
loc2.setDescription("This is location 2")
level.locAdd(loc2)

loc3 = Location("loc3")
loc3.setDescription("This is location 3")
level.locAdd(loc3)

loc4 = Location("loc4",endLocation=True)
loc4.setDescription("This is location 4")
level.locAdd(loc4)

# Create game obstruction objects
red_door = Obstructor(
    baseName='red-door',
    resolvedStateStr='unlocked',
    unresolvedStateStr='locked',
    resolutionItem='red-key',
    canKill=False
)

blue_door = Obstructor(
    baseName='blue-door',
    resolvedStateStr='unlocked',
    unresolvedStateStr='locked',
    resolutionItem='blue-key',
    canKill=False
)

ghost = Obstructor(
    baseName='ghost',
    resolvedStateStr='dead',
    unresolvedStateStr='',
    resolutionItem='spell',
    canKill=False
)

# Populate rooms with items
loc1.addItem("red-key")
loc2.addItem("blue-key")
loc3.addItem("spell")

# Connect locations
Location.connect(loc0,'left',loc1)
Location.connect(loc0,'right',loc2,obs=red_door)
Location.connect(loc1,'left',loc3,obs=blue_door)
Location.connect(loc3,'forward',loc4,obs=ghost)

# Assign start location handle
level.start_loc=loc0
