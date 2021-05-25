
# MUST BE DONE BEFORE IMPORTING pgzrun OR DOESN'T WORK
import os
window_pos_x = 400
window_pos_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_pos_x, window_pos_y)

# imports
import pgzrun
import random

# Constants
#pygame Zero window size
WIDTH = 700
HEIGHT = 800

GAME_MENU = 0
GAME_DRIVING = 1
GAME_LOST = 2
GAME_WON = 3
GAME_TAS = 4

OVERRIDE_TRACK = False
TRACK_NAME = "track_1.txt"

# Classes
class Game:
    state = GAME_MENU
    
    def drive(self):
        self.track_file = f"tracks/{TRACK_NAME}"
        self.SPEED = 16                  # vertical scrolling speed
        self.trackCenter = 350
        self.trackWidth = 150            # width between center and edge of track
		
        self.trackLeft = []              # list to store left barriers
        self.trackRight = []             # list to store right barriers
        self.trackCount = 0              # count the number of barriers
        self.trackDirection = False
        
        if OVERRIDE_TRACK:
            self.generate_track()
            
        self.load_track()  # Track layout
        
        self.inputs = []
        self.state = GAME_DRIVING
    
    def tas(self):
        self.state = GAME_TAS
        
    # function to make one barrier at the left and right
    def makeObstacle(self):
        #print("makeObstacle")
        track_center = self.track_centers[self.trackCount]
        self.trackLeft.append(Actor("bare", pos = (track_center - self.trackWidth, 0)))
        self.trackRight.append(Actor("bare", pos = (track_center + self.trackWidth, 0)))
        self.trackCount += 1

    def updateTrack(self):
	    # Check obstacle collision and move obstacles down
        for i in range(len(self.trackLeft)):
            if car.colliderect(self.trackLeft[i]) or car.colliderect(self.trackRight[i]):
                self.state = GAME_LOST
                self.save_inputs()
            self.trackLeft[i].y += self.SPEED
            self.trackRight[i].y += self.SPEED
            i += 1
            
        # Create 1st obstacle
        if self.trackCount == 0:
            self.makeObstacle()
            
        # Create new obstacle when last one is far enough
        if self.trackLeft[-1].y > 32:
            self.makeObstacle()
    
	# Read self.track_file
    def load_track(self):
        self.track_centers = []
		
        with open(self.track_file) as file:
            for line in file:
                center = int(line.split(" = ")[-1].strip())
                #print(center)
                self.track_centers.append(center)
    
	# Write self.track_file
    def generate_track(self):
        f = open(self.track_file, "w")
        for _ in range(500):
            f.write(f"center = {self.trackCenter}\n")
            
            if self.trackDirection:  
                self.trackCenter += 16
            else:
                self.trackCenter -= 16
            if random.random() < 0.2:
                self.trackDirection = not self.trackDirection
            if self.trackCenter > 700 - self.trackWidth:
                self.trackDirection = True
            if self.trackCenter < self.trackWidth:
                self.trackDirection = False
        f.close()
    
	# Write self.inputs_file
    def save_inputs(self):
        time = "test_improve_taf"
        self.inputs_file = f"inputs/last_inputs.txt"
        
        f = open(self.inputs_file, "w")
        for input in self.inputs:
            f.write(f"steer = {input}\n")
        f.close()

# pygame Zero draw function
def draw():  
    screen.fill((128, 128, 128))
    #print(game.state)
    
    if game.state == GAME_MENU:
        screen.draw.text("Press up arrow to start", (100, 100), color=(255, 255, 255), fontsize = 40 )
        screen.draw.text("Press down arrow to open an inputs file", (100, 200), color=(255, 255, 255), fontsize = 40 )
    if game.state == GAME_DRIVING:
        #print("draw driving")
        car.draw()
        b = 0
        while b < len(game.trackLeft):
            game.trackLeft[b].draw()
            game.trackRight[b].draw()
            b += 1
        screen.draw.text("Your Current Score : " + str(game.trackCount), (10, 10), color=(255, 255, 255))
    if game.state == GAME_LOST:
        #Red Flag
        screen.blit("redflag", (230, 230))
        screen.draw.text("You lost!",(350, 60), color=(255, 128, 0), fontsize = 50 )
        screen.draw.text(f"Inputs saved in {game.inputs_file}", (100, 130), color=(255, 255, 255), fontsize = 30 )
        screen.draw.text("Drive again? Press up arrow", (250, 600), color=(255, 255, 255), fontsize = 40 )
        screen.draw.text("Try to TAS? Press down arrow", (250, 630), color=(255, 255, 255), fontsize = 40 )
    if game.state == GAME_WON:
        #Chequered Flag
        screen.blit("finishflag", (230, 230))

# pygame Zero update function
def update():            
    if game.state == GAME_DRIVING:
        cur_input = 0
        if keyboard.left:
            car.x -= 8
            cur_input -= 1
        if keyboard.right:
            car.x += 8
            cur_input += 1
        game.updateTrack()
        game.inputs.append(cur_input)
        
    else:
        if keyboard.up:
            game.drive()
        if keyboard.down:
            game.tas()
   # rise the speed of the game
   # if trackCount > 50   : SPEED = 5
   # if trackCount > 150  : trackWidth = 150     # low the track width
   # if trackCount > 250  : SPEED = 6
   # if trackCount > 350  : trackWidth = 150
   # if trackCount > 500  : game_state = 2       # you win: pass 500 barriers


# Script
game = Game()

car = Actor("racecar")              # load the race car image
car.pos = 350,560                   # position of the race car

pgzrun.go()
