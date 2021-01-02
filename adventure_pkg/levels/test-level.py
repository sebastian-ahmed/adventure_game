# Copyright 2020 Sebastian Ahmed
# This file, and derivatives thereof are licensed under the Apache License, Version 2.0 (the "License");
# Use of this file means you agree to the terms and conditions of the license and are in full compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, EITHER EXPRESSED OR IMPLIED.
# See the License for the specific language governing permissions and limitations under the License.

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
    baseName='snake',
    resolvedStateStr='dead',
    unresolvedStateStr='',
    resolutionItem='grenade',
    canKill=True
)
snake.setItem('dagger')

# Non-blocking but can be resolved
fire = Obstructor(
    baseName='fire',
    resolvedStateStr='extinguished',
    unresolvedStateStr='burning',
    resolutionItem='water',
    canKill=True,
    nonBlocking=True
)

# Populate rooms with items
loc1.addItem("water")
loc1.addGameItem("healthpack")
loc1.addGameItem("healthpack")
loc1.addGameItem("healthpack")
loc2.addItem("grenade")

# Connect locations
Location.connect(loc1,'left',loc2,obs=fire)
Location.connect(loc1,'right',loc3,obs=snake)

# Assign start location handle
level.start_loc=loc1

# Define a play-through test-script
level.testScript=[
    "take healthpack",
    "take healthpack",
    "take healthpack",
    "go l",
    "use healthpack",
    "take grenade",
    "go r",
    "use healthpack",
    "go r",
    "use grenade on snake",
    "go r"
]