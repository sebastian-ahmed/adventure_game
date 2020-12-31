from adventure_pkg.modules.Location   import Location
from adventure_pkg.modules.Obstructor import Obstructor
from adventure_pkg.modules.Level      import Level

level = Level("level4")

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
room31.setDescription("The starting location")
room31.setHint("Be careful when walking through endangered paths")
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
    baseName='black-door',
    resolvedStateStr='unlocked',
    unresolvedStateStr='locked',
    resolutionItem='black-key',
    canKill=False
)

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

wolf = Obstructor(
    baseName='wolf',
    resolvedStateStr='sleeping',
    unresolvedStateStr='',
    resolutionItem='meat',
    canKill=True
)
# This obstructor will drop an item
wolf.setItem('poison')

rat = Obstructor(
    baseName='rat',
    resolvedStateStr='dead',
    unresolvedStateStr='',
    resolutionItem='poison',
    canKill=True
)

wizard = Obstructor(
    baseName='wizard',
    resolvedStateStr='frozen',
    unresolvedStateStr='',
    resolutionItem='potion',
    canKill=True
)

stone_wall = Obstructor(
    baseName='stone-wall',
    resolvedStateStr='destroyed',
    unresolvedStateStr='',
    resolutionItem='dynamite',
    canKill=False
)

# This is a non-blocking obstructor
# and will damage the player, note
# we set resolutionItem=None
fire = Obstructor(
    baseName='flaming-pathway',
    resolvedStateStr='',
    unresolvedStateStr='',
    resolutionItem=None,
    canKill=True,
    nonBlocking=True
)

# Populate rooms with items
room01.addItem('blue-key')
room02.addItem('dynamite')
room12.addItem('potion')
room13.addItem('meat')
room20.addItem('knife') # dummy item to trick the player
room23.addItem('red-key')
room33.addItem('black-key')

# Populate rooms with special game items
# (note these are game-specific items)
room01.addGameItem('healthpack')
room21.addGameItem('healthpack')
room21.addGameItem('healthpack')
room33.addGameItem('healthpack')

# Connect locations and obstructors. All here assumed to be reciprocating connectors
Location.connect(room00,'forward' ,room01)
Location.connect(room00,'right'   ,room10,obs=fire)
Location.connect(room10,'forward' ,room11,obs=red_door)
Location.connect(room20,'left'    ,room10)
Location.connect(room20,'forward' ,room31)
Location.connect(room50,'forward' ,room51,obs=stone_wall)
Location.connect(room11,'right'   ,room21,obs=wolf)
Location.connect(room31,'forward' ,room32)
Location.connect(room31,'right'   ,room41,obs=fire)
Location.connect(room41,'right'   ,room51,obs=wizard)
Location.connect(room02,'right'   ,room12,obs=black_door)
Location.connect(room12,'forward' ,room13,obs=rat)
Location.connect(room22,'forward' ,room23)
Location.connect(room22,'right'   ,room32,obs=blue_door)
Location.connect(room32,'backward',room31)
Location.connect(room32,'forward' ,room33,obs=fire)
Location.connect(room13,'right'   ,room23)

# Assign start location handle
level.start_loc=room31

# Define a play-through test-script
level.testScript=[
    "go b",
    "go l",
    "go l",
    "go f",
    "take healthpack",
    "take blue-key",
    "go b",
    "go r",
    "use healthpack",
    "go r",
    "go f",
    "go f",
    "use blue-key on blue-door",
    "go l",
    "go f",
    "take red-key",
    "go l",
    "take meat",
    "go r",
    "go b",
    "go r",
    "go b",
    "go b",
    "go l",
    "use red-key on red-door",
    "go f",
    "use meat on wolf",
    "take poison",
    "go r",
    "take healthpack",
    "take healthpack",
    "use healthpack",
    "go l",
    "go b",
    "go r",
    "go f",
    "go f",
    "go l",
    "go r",
    "go l",
    "go b",
    "go f",
    "go l",
    "use poison on rat",
    "go b",
    "take potion",
    "go f",
    "go r",
    "go b",
    "go r",
    "go f",
    "take healthpack",
    "use healthpack",
    "take black-key",
    "go b",
    "use healthpack",
    "go l",
    "go f",
    "go l",
    "go b",
    "use black-key on black-door",
    "go l",
    "take dynamite",
    "go r",
    "go f",
    "go r",
    "go b",
    "go r",
    "go b",
    "go r",
    "use potion on wizard",
    "go r",
    "use dynamite on stone-wall",
    "go b"
]