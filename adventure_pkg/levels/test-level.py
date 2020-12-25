from adventure_pkg.modules.Location   import Location
from adventure_pkg.modules.Obstructor import Obstructor
from adventure_pkg.modules.Level      import Level

level = Level("test-level")

loc1 = Location("loc1")
loc1.setDescription("You are in the first room")
level.locAdd(loc1)

loc2 = Location("loc2")
loc2.setDescription("This is location 2")
level.locAdd(loc2)

loc3 = Location("loc3",endLocation=True)
loc3.setDescription("This is final location")
level.locAdd(loc3)

# Create game obstruction objects
snake = Obstructor(
    'snake',
    'dead',
    '',
    'grenade',
    canKill=True
)
snake.setItem('dagger')

fire = Obstructor(
    'fire',
    '',
    '',
    None,
    canKill=True
)

# Populate rooms with items
loc1.addItem("grenade")
loc1.addGameItem("healthpack")
loc1.addGameItem("healthpack")
loc1.addGameItem("healthpack")

# Connect locations
Location.connect(loc1,'left',loc2,obs=fire)
Location.connect(loc1,'right',loc3,obs=snake)

# Assign start location handle
level.start_loc=loc1
