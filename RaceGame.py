#!/usr/bin/python3

import os
# MUST BE DONE BEFORE IMPORTING pgzrun OR DOESN'T WORK
window_pos_x = 400
window_pos_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_pos_x, window_pos_y)

# imports
import pgzrun
import random

# Constants
WIDTH = 700                 # width of the window
HEIGHT = 800                # height of the window

GAME_MENU = 0
GAME_DRIVING = 1
GAME_LOST = 2
GAME_WON = 3
GAME_TAS = 4

# Classes
class Game:
    state = GAME_MENU
    
    def drive(self):
        self.trackLeft = []              # list to store left barriers
        self.trackRight = []             # list to store right barriers
        self.trackCount = 0              # count the number of barriers
        self.trackPosition = 350
        self.trackWidth = 150            # width between left and right barriers
        self.trackDirection = False
        self.SPEED = 16                 # sets speed of the game
        
        self.makeTrack()  # Make first block of track
        
        self.inputs = []
        self.state = GAME_DRIVING
    
    def tas(self):
        pass
        
    def makeTrack(self):                    # function to make one barrie at the left and right
        #print("makeTrack")
        self.trackLeft.append(Actor("bare", pos = (self.trackPosition - self.trackWidth, 0)))
        self.trackRight.append(Actor("bare", pos = (self.trackPosition + self.trackWidth, 0)))
        self.trackCount += 1

    def updateTrack(self):
        b = 0
        while b < len(self.trackLeft):
            if car.colliderect(self.trackLeft[b]) or car.colliderect(self.trackRight[b]):
                self.state = GAME_LOST
                self.save_inputs()
            self.trackLeft[b].y += self.SPEED
            self.trackRight[b].y += self.SPEED
            b += 1
			
		# Create new barriers when last one is far enough
        if self.trackLeft[-1].y > 32:
            if self.trackDirection == True:  
                self.trackPosition -= 16
            else:
                self.trackPosition += 16
            if random.random() < 0.2:
                self.trackDirection = not self.trackDirection
            if self.trackPosition > 700 - self.trackWidth:
                self.trackDirection = True
            if self.trackPosition < self.trackWidth:
                self.trackDirection = False
            self.makeTrack()

    def save_track(self):
        self.inputs_file = f"tracks/track_1.txt"
        
        f = open(self.inputs_file, "w")
        for input in self.inputs:
            f.write(f"steer = {input}\n")
        f.close()

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
