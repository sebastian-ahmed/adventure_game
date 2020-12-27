from adventure_pkg.modules.Location   import Location
from adventure_pkg.modules.Obstructor import Obstructor
from adventure_pkg.modules.Level      import Level

level = Level("level2")

# Location descriptions
room1 = Location("room1")
room1.setDescription("You find yourself in a dark room. This is room 1")
level.locAdd(room1)

room2 = Location("room2")
room2.setDescription("You are now in room 2.")
level.locAdd(room2)

room3 = Location("room3")
room3.setDescription("You are n ow in room 3.")
level.locAdd(room3)

room4 = Location("room4")
room4.setDescription("You are now in room 4.")
level.locAdd(room4)

room5 = Location("room5")
room5.setDescription("you are now in room 5.")
level.locAdd(room5)

room6 = Location("room6")
room6.setDescription("You are now in room 6.")
level.locAdd(room6)

room7 = Location("room7")
room7.setDescription("you are now in room 7.")
level.locAdd(room7)

room8 = Location("room8",endLocation=True)
room8.setDescription("You are now outside!")
level.locAdd(room8)

# Create game obstruction objects
yellow_door = Obstructor(
    baseName='yellow-door',
    resolvedStateStr='unlocked',
    unresolvedStateStr='locked',
    resolutionItem='yellow-key'
)

red_door = Obstructor(
    baseName='red-door',
    resolvedStateStr='unlocked',
    unresolvedStateStr='locked',
    resolutionItem='red-key'
)

purple_door = Obstructor(
    baseName='purple-door',
    resolvedStateStr='unlocked',
    unresolvedStateStr='locked',
    resolutionItem='purple-key'
)
white_door = Obstructor(
    baseName='white-door',
    resolvedStateStr='unlocked',
    unresolvedStateStr='locked',
    resolutionItem='white-key'
)

giant_spider = Obstructor(
    baseName='giant-spider',
    resolvedStateStr='dead',
    unresolvedStateStr='',
    resolutionItem='sword',
    canKill=True
)

# Populate rooms with items
room3.addItem("yellow-key")
room2.addItem("purple-key")
room4.addItem("white-key")
room6.addItem("red-key")
room7.addItem("sword")

# Connect locations and obstructors
Location.connect(room1,'right',room4,obs=yellow_door)
Location.connect(room1,"left", room2)
Location.connect(room2,"forward", room3, obs=purple_door)
Location.connect(room4,"forward", room5)
Location.connect(room5,"left", room7, obs=red_door)
Location.connect(room5,"forward", room6, obs=white_door)
Location.connect(room5,"right", room8, obs=giant_spider)

# Assign start location handle
level.start_loc=room1

# Define a play-through test-script
level.testScript=[
    "go l",
    "take purple-key",
    "use purple-key on purple-door",
    "go f",
    "take yellow-key",
    "go b",
    "go r",
    "use yellow-key on yellow-door",
    "go r",
    "take white-key",
    "go f",
    "use white-key on white-door",
    "go f",
    "take red-key",
    "go b",
    "use red-key on red-door",
    "go l",
    "take sword",
    "go r",
    "use sword on giant-spider",
    "go r"
]