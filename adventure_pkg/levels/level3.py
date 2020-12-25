from adventure_pkg.modules.Location   import Location
from adventure_pkg.modules.Obstructor import Obstructor
from adventure_pkg.modules.Level      import Level

level = Level("level3")

# In this level the room numbering follows a 2-D grid of (x,y) coordinates

# Location descriptions
room00 = Location("room00")
room00.setDescription("A mysterious room")
level.locAdd(room00)

room01 = Location("room01")
room01.setDescription("A mysterious room")
level.locAdd(room01)

room02 = Location("room02")
room02.setDescription("A mysterious room")
level.locAdd(room02)

room10 = Location("room10")
room10.setDescription("A mysterious room")
level.locAdd(room10)

room11 = Location("room11")
room11.setDescription("A mysterious room")
level.locAdd(room11)

room12 = Location("room12")
room12.setDescription("A mysterious room")
level.locAdd(room12)

room13 = Location("room13")
room13.setDescription("A mysterious room")
level.locAdd(room13)

room20 = Location("room20")
room20.setDescription("A mysterious room")
level.locAdd(room20)

room21 = Location("room21")
room21.setDescription("A mysterious room")
level.locAdd(room21)

room22 = Location("room22")
room22.setDescription("A mysterious room")
level.locAdd(room22)

room23 = Location("room23")
room23.setDescription("A mysterious room")
level.locAdd(room23)

room31 = Location("room31")
room31.setDescription("A mysterious room")
level.locAdd(room31)

room32 = Location("room32")
room32.setDescription("A mysterious room")
level.locAdd(room32)

room33 = Location("room33")
room33.setDescription("A mysterious room")
level.locAdd(room33)

room41 = Location("room41")
room41.setDescription("A mysterious room")
level.locAdd(room41)

room51 = Location("room51")
room51.setDescription("A mysterious room")
level.locAdd(room51)

room50 = Location("room50",endLocation=True)
room50.setDescription("You see sunlight and a forest!")
level.locAdd(room50)

# Create game obstruction objects
black_door = Obstructor(
    'black-door',
    'unlocked',
    'locked',
    'black-key'
)

red_door = Obstructor(
    'red-door',
    'unlocked',
    'locked',
    'red-key'
)

blue_door = Obstructor(
    'blue-door',
    'unlocked',
    'locked',
    'blue-key'
)

wolf = Obstructor(
    'wolf',
    'sleeping',
    '',
    'meat',
    canKill=True
)
# This obstructor will drop an item
wolf.setItem('poison')

rat = Obstructor(
    'rat',
    'dead',
    '',
    'poison',
    canKill=True
)

wizard = Obstructor(
    'wizard',
    'frozen',
    '',
    'potion',
    canKill=True
)

stone_wall = Obstructor(
    'stone-wall',
    'destroyed',
    '',
    'dynamite'
)

# Populate rooms with items
room01.addItem('blue-key')
room02.addItem('dynamite')
room12.addItem('potion')
room13.addItem('meat')
room20.addItem('knife') # this is a dummy item to trick the player
room23.addItem('red-key')
room33.addItem('black-key')

# Connect locations and obstructors. Note that some of the connections
# are non-reciprocating, e.g. a forward connector of one location may
# connect to the right connector of another location. In these cases
# a second direction (for the second location) is also specified
Location.connect(room00,'forward' ,room01)
Location.connect(room00,'right'   ,room10)
Location.connect(room10,'forward' ,room11,obs=red_door)
Location.connect(room20,'left'    ,room10)
Location.connect(room20,'right'   ,room31,dir_b='backward')
Location.connect(room50,'forward' ,room51,obs=stone_wall)
Location.connect(room11,'right'   ,room21,obs=wolf)
Location.connect(room31,'forward' ,room32)
Location.connect(room31,'right'   ,room41)
Location.connect(room41,'backward',room10,dir_b='backward')
Location.connect(room41,'forward' ,room33,dir_b='right')
Location.connect(room41,'right'   ,room51,obs=wizard)
Location.connect(room02,'right'   ,room12,obs=black_door)
Location.connect(room12,'forward' ,room13,obs=rat)
Location.connect(room22,'forward' ,room23)
Location.connect(room22,'right'   ,room32,obs=blue_door)
Location.connect(room32,'backward',room31)
Location.connect(room32,'forward' ,room33)
Location.connect(room13,'right'   ,room23)

# Assign start location handle
level.start_loc=room31

