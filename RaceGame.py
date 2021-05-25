
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
INPUTS_FILE = "last_inputs.txt"

# Classes
class Game:
    state = GAME_MENU
    car = Actor("racecar")              # load the race car image
    
    def drive(self):
        self.track_file = f"tracks/{TRACK_NAME}"
        self.inputs_file = f"inputs/{INPUTS_FILE}"
        self.SPEED = 16                  # vertical scrolling speed
        self.trackCenter = 350
        self.trackWidth = 150            # width between center and edge of track
        
        self.trackLeft = []              # list to store left barriers
        self.trackRight = []             # list to store right barriers
        self.trackCount = 0              # count the number of barriers
        
        if OVERRIDE_TRACK:
            self.generate_track()
            
        self.load_track()  # Track layout
        
        self.inputs = []
        
        self.car.pos = 350,560                   # position of the race car
        self.state = GAME_DRIVING

    
    def tas(self):
        self.track_file = f"tracks/{TRACK_NAME}"
        self.inputs_file = f"inputs/{INPUTS_FILE}"
        self.SPEED = 16                   # vertical scrolling speed
        self.trackCenter = 350
        self.trackWidth = 150            # width between center and edge of track
        
        self.trackLeft = []              # list to store left barriers
        self.trackRight = []             # list to store right barriers
        self.trackCount = 0              # count the number of barriers
            
        self.load_track()  # Track layout
        
        self.load_inputs()
        
        self.car.pos = 350,560                   # position of the race car
        self.state = GAME_TAS
        
    # function to make one barrier at the left and right
    def makeObstacle(self):
        #print("makeObstacle")
        if self.trackCount < len(self.track_centers):
            track_center = self.track_centers[self.trackCount]
            self.trackLeft.append(Actor("bare", pos = (track_center - self.trackWidth, 0)))
            self.trackRight.append(Actor("bare", pos = (track_center + self.trackWidth, 0)))
            self.trackCount += 1
        else:
            self.state = GAME_WON

    def updateTrack(self):
        # Check obstacle collision and move obstacles down
        for i in range(len(self.trackLeft)):
            if self.car.colliderect(self.trackLeft[i]) or self.car.colliderect(self.trackRight[i]):
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
    
    # Read self.inputs_file
    def load_inputs(self):
        self.inputs = []
        self.input_nb = 0
        
        with open(self.inputs_file) as file:
            for line in file:
                input = int(line.split(" = ")[-1].strip())
                #print(input)
                self.inputs.append(input)
    
    # Write self.track_file
    def generate_track(self):
        self.trackDirection = True
        
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
                self.trackDirection = False
            if self.trackCenter < self.trackWidth:
                self.trackDirection = True
        f.close()
    
    # Write self.inputs_file
    def save_inputs(self):        
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
        game.car.draw()
        for i in range(len(game.trackLeft)):
            game.trackLeft[i].draw()
            game.trackRight[i].draw()
        
        screen.draw.text("Your Current Score : " + str(game.trackCount), (10, 10), color=(255, 255, 255))
    if game.state == GAME_TAS:
        #print("draw tas")
        game.car.draw()
        for i in range(len(game.trackLeft)):
            game.trackLeft[i].draw()
            game.trackRight[i].draw()
        
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
            cur_input -= 1
        if keyboard.right:
            cur_input += 1
        game.inputs.append(cur_input)
        
        if cur_input == -1:
            game.car.x -= 8
        if cur_input == 1:
            game.car.x += 8
        game.updateTrack()
        
    elif game.state == GAME_TAS:
        cur_input = game.inputs[game.input_nb]
        game.input_nb += 1
        
        if cur_input == -1:
            game.car.x -= 8
        if cur_input == 1:
            game.car.x += 8
        game.updateTrack()
        
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

pgzrun.go()
