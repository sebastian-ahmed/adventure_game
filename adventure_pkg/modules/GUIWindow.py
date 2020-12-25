import turtle

from adventure_pkg.modules.Location   import Location
from adventure_pkg.modules.Player     import Player

class GUIWindow():
    '''
        This class works in conjunction with Adventure objects to provide
        a basic GUI representation of the Player's current location and
        inventory
    '''

    def __init__(self,title="Adventure Game Default Window Name"):
        self._title = title
        # Configure Turtle window
        self._thandle = turtle.Turtle()
        self._shandle = self._thandle.getscreen()
        self._shandle.setup(600+4, 600+8)
        self._thandle.speed("fastest")
        self._shandle.title(self._title)
  
    def clearWindow(self):
        self._thandle.clear()
        self._thandle.penup()
        self._thandle.home()

    def gameOverWindow(self, player):
        self.clearWindow()
        self._thandle.color("green")
        self._thandle.write(f"{player._name} Has Escaped!", font=("Arial", 20, "normal"), align='center')
        self._thandle.setpos(0,-50)
        self._thandle.write("Game Over", font=("Arial", 20, "normal"), align='center')

    def playerDeadWindow(self, player):
        self.clearWindow()
        self._thandle.color("red")
        self._thandle.write(f"{player._name} Has Died!", font=("Arial", 20, "normal"), align='center')
        self._thandle.setpos(0,-50)
        self._thandle.write("Game Over", font=("Arial", 20, "normal"), align='center')

    def writeObstructor(self,label):
        self._thandle.write(label, font=("Arial", 8, "bold"), align='center')

    def updateWindow (self,loc,player):
        self.clearWindow()
        self._thandle.write(loc._name, font=("Arial", 12, "normal"), align='center')
        self._thandle.setpos(-100,-100)
        self._thandle.pendown()
        self._thandle.hideturtle()

        # Draw main box to represent the Location and state
        # of each direction
        for direction in ['backward','right','forward','left']:
            self._thandle.fd(100)
            if loc.dirHasConnection(direction):
                if loc.dirIsObstacled(direction):
                    self._thandle.dot(20,"orange")
                elif loc.dirIsObstructed(direction):
                    self._thandle.dot(20,"red")
                else:
                    self._thandle.dot(20,"green")
            self.writeObstructor(loc.dirObstructorStr(direction))
            self._thandle.fd(100)
            self._thandle.lt(90)

        # Draw items in the room
        self._thandle.penup()
        self._thandle.fd(20)
        self._thandle.lt(90)
        self._thandle.fd(20)
        for item in loc._items:
            self._thandle.write(item, font=("Arial", 8, "normal"), align='left')
            self._thandle.fd(10)

        # Draw player inventory
        self._thandle.home()
        self._thandle.setpos(110,90)
        self._thandle.write(f"{player._name}'s Items", font=("Arial", 10, "normal"), align='left')
        self._thandle.rt(90)
        self._thandle.fd(10)
        for key,val in player._inv.items():
            self._thandle.write(f"{key}:{val}", font=("Arial", 8, "normal"), align='left')
            self._thandle.fd(10)
        
        # Draw player health
        self._thandle.fd(100)
        self._thandle.write(f"{player._name}'s health level", font=("Arial", 10, "normal"), align='left')
        self._thandle.fd(10)
        self._thandle.write(f"{player.getHealth()}/100", font=("Arial", 8, "normal"), align='left')

