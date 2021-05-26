
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
GAME_TAS = 2
GAME_LOST = 3
GAME_WON = 4

OVERRIDE_TRACK = False
TRACK_NAME = "track_2.txt"
INPUTS_FILE = "last_inputs.txt"

# Classes
class Game:
    state = GAME_MENU
    car = Actor("racecar")              # load the race car image
    #trail = pygame.image.load('images/racecar.png').convert_alpha()
    
    def drive(self):
        self.track_file = f"tracks/{TRACK_NAME}"
        self.inputs_file = f"inputs/{INPUTS_FILE}"
        self.SPEED = 16                  # vertical scrolling speed
        self.trackCenter = 350
        self.trackWidth = 100            # width between center and edge of track
        
        self.timing = 0
        
        if OVERRIDE_TRACK:
            self.generate_track()
            
        self.load_track()  # Track layout
        
        self.inputs = []
        
        self.car.pos = 350, 560                   # position of the race car
        self.state = GAME_DRIVING

    
    def tas(self):
        self.track_file = f"tracks/{TRACK_NAME}"
        self.inputs_file = f"inputs/{INPUTS_FILE}"
        self.SPEED = 16                  # vertical scrolling speed
        self.trackCenter = 350
        self.trackWidth = 150            # width between center and edge of track
        
        self.timing = 0
            
        self.load_track()  # Track layout
        
        self.load_inputs()
        
        self.car_trails = []
        self.car.pos = 350, 560                   # position of the race car
        self.state = GAME_TAS

    def updateTrack(self):
        #print(f"updateTrack game.timing={game.timing}")
        
        if game.state == GAME_DRIVING:
            # Check obstacle collision and place obstacles depending on game.timing
            for obst in self.obstacles:
                if self.car.colliderect(obst):
                    self.save_inputs()
                    self.state = GAME_LOST
                obst.y = obst.start_y + game.timing
                
            game.timing += self.SPEED
            if game.timing >= 500 * self.SPEED:
                self.state = GAME_WON
                
        if game.state == GAME_TAS:
            for obst in self.obstacles:
                obst.y = obst.start_y + game.timing
                
            self.car_trails = []
            
            # Draw start car
            x = 350
            y = 560 + game.timing
            # self.makeCar(x, y)
            
            # Draw car after every input
            for timing, input in self.inputs:
                #print(input)
                if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
                    self.makeCar(x, y, timing, input)
                    
                    # Check obstacle collision
                    for obst in self.obstacles:
                        if self.car_trails[-1].colliderect(obst):
                            return
            
                if input == -1:
                    x -= 8
                if input == 1:
                    x += 8
                y -= self.SPEED
        
    def makeCar(self, x, y, timing, input):
        car = Actor("racecar", (x, y))
        car.timing = timing
        car.input = input
        self.car_trails.append(car)
        
    def makeObstacle(self, pos):
        x, y = pos
        obst = Actor("bare", pos)
        obst.start_x = x
        obst.start_y = y
        self.obstacles.append(obst)
        
    def get_cur_input(self):
        timing, input = self.inputs[int(self.timing / self.SPEED)]
        return input
        
    def set_cur_input(self, cur_input):
        timing, input = self.inputs[int(self.timing / self.SPEED)]
        self.inputs[int(self.timing / self.SPEED)] = (timing, cur_input)
        
        for timing, stored_input in self.inputs:
            if timing == self.timing:
                self.inputs[int(timing / self.SPEED)] = (timing, cur_input)
                #print(self.inputs)
                break
    
    # Read self.track_file
    def load_track(self):                
        self.obstacles = []
        
        with open(self.track_file) as file:
            for line in file:
                x = int(line.split(" ")[-2].strip())
                y = int(line.split(" ")[-1].strip())
                #print((x, y))
                self.makeObstacle((x, y))
    
    # Read self.inputs_file
    def load_inputs(self):
        self.inputs = []
        self.input_nb = 0
        
        with open(self.inputs_file) as file:
            for line in file:
                timing = int(line.split(" ")[0])
                input = int(line.split(" = ")[-1].strip())
                #print(input)
                self.inputs.append((timing, input))
    
    # Write self.track_file
    def generate_track(self):
        self.trackDirection = True
        
        f = open(self.track_file, "w")
        for i in range(500):
            y = i * (-32)
            x = self.trackCenter - self.trackWidth
            f.write(f"x y = {x} {y}\n")
            x = self.trackCenter + self.trackWidth
            f.write(f"x y = {x} {y}\n")
            
            if self.trackDirection:  
                self.trackCenter += 16
            else:
                self.trackCenter -= 16
                
            if random.random() < 0.2:
                self.trackDirection = not self.trackDirection
            if self.trackCenter > WIDTH - self.trackWidth:
                self.trackDirection = False
            if self.trackCenter < self.trackWidth:
                self.trackDirection = True
        f.close()
    
    # Write self.inputs_file
    def save_inputs(self):
        # Add extra empty inputs so TAS can keep going after crash
        if game.state == GAME_DRIVING:
            timing = game.timing
            while timing < 500 * 32:
                timing += self.SPEED
                self.inputs.append(((timing, 0)))
            
        f = open(self.inputs_file, "w")
        for timing, input in self.inputs:
            f.write(f"{timing} steer = {input}\n")
        f.close()

# pygame Zero draw function
def draw():  
    screen.fill((128, 128, 128))
    #print(game.state)
    
    if game.state == GAME_MENU:
        screen.draw.text("Press up arrow to drive", (100, 100), color=(255, 255, 255), fontsize = 40 )
        screen.draw.text("Commands to drive: left & right arrows", (100, 150), color=(255, 255, 255), fontsize = 20 )
        screen.draw.text("Press down arrow to TAS", (100, 250), color=(255, 255, 255), fontsize = 40 )
        screen.draw.text("Commands to nagivate the inputs: j & l", (100, 300), color=(255, 255, 255), fontsize = 20 )
        screen.draw.text("Commands to change the inputs: left, up & right arrows", (100, 350), color=(255, 255, 255), fontsize = 20 )
    if game.state == GAME_DRIVING:
        #print("draw driving")
        game.car.draw()
        for obst in game.obstacles:
            obst.draw()
        
        screen.draw.text("Your Current Score : " + str(game.timing / 32), (10, 10), color=(255, 255, 255))
    if game.state == GAME_TAS:
        #print("draw tas")
        for trail in game.car_trails:
            trail.draw()
            screen.draw.text(f"Input={trail.input}",(trail.x + 32, trail.y + 32), color=(255, 128, 0), fontsize = 20 )
        # game.car.draw()
        for obst in game.obstacles:
            obst.draw()
        
        screen.draw.text("Your Current Score : " + str(game.timing / 32), (10, 10), color=(255, 255, 255))
    if game.state == GAME_LOST:
        #Red Flag
        screen.blit("redflag", (230, 230))
        screen.draw.text("You lost!",(350, 60), color=(255, 128, 0), fontsize = 50 )
        screen.draw.text("Your Score : " + str(game.timing / 32), (100, 130), color=(255, 255, 255), fontsize = 40 )
        screen.draw.text("Drive again? Press up arrow", (250, 600), color=(255, 255, 255), fontsize = 40 )
        screen.draw.text("Try to TAS? Press down arrow", (250, 630), color=(255, 255, 255), fontsize = 40 )
    if game.state == GAME_WON:
        #Chequered Flag
        screen.blit("finishflag", (230, 230))

# pygame Zero update function
def update():            
    if game.state == GAME_DRIVING:
        if keyboard.escape:
            game.save_inputs()
            game.state = GAME_MENU
        cur_input = 0
        if keyboard.left:
            cur_input -= 1
        if keyboard.right:
            cur_input += 1
        game.inputs.append((game.timing, cur_input))
        
        if cur_input == -1:
            game.car.x -= 8
        if cur_input == 1:
            game.car.x += 8
        game.updateTrack()
        
    elif game.state == GAME_TAS:
        if keyboard.escape:
            game.save_inputs()
            game.state = GAME_MENU
        if keyboard.j:
            game.timing -= game.SPEED
            if game.timing < 0:
                game.timing = 0
        if keyboard.l:
            game.timing += game.SPEED
        
        cur_input = -2
        if keyboard.left:
            cur_input = -1
        if keyboard.up:
            cur_input = 0
        if keyboard.right:
            cur_input = 1
        
        if cur_input != -2:
            game.set_cur_input(cur_input)
        #print(f"{timing} {game.timing} {cur_input}")
        
        # Check if time to update
        # while timing < game.timing:              
            # if cur_input == -1:
                # game.car.x -= 8
            # if cur_input == 1:
                # game.car.x += 8
            
            # game.input_nb += 1
            # timing, cur_input = game.inputs[game.input_nb]
            
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
