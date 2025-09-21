from tkinter import *
import time, random
from Obstacles import Obstacles
from Dino import Dino
import os
class DinoGame:
    
    #-------------------------------------------------------------------------
    # Initialization and Setup
    #-------------------------------------------------------------------------
    
    def __init__(self, root, nrow, ncol, scale):
        self.root = root
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.canvas = Canvas(root, width= ncol * scale, height=nrow*scale, bg='black')
        self.canvas.pack()
        self.__game_over = False
        self.__pause = False
        self.__started = False
        self.__next_spawn_time = 0
        self.__score = 0
        self.__start_time = 0
        self.__pause_time = 0
        self.stop_update = False # ihave to do this because the obstacle get too fast after many restart
        self.dino = Dino(self.canvas, nrow, ncol, scale,c=2)
        self.obstacles = []
        self.dino.activate()
        self.spawn_interval = 3 
        self.obstacles_speed = 1
        self.highscore = self.load_high_score()
        self.better_visual() #i make some label for easier score tracking
        self.start_screen()
        
        
    # Remove the pass statement and implement the __init__ method as described in the PDF.
    
    #-------------------------------------------------------------------------
    # Game State Methods
    #-------------------------------------------------------------------------
    def reset(self):
        self.__game_over = False
        self.__pause = False
        self.__started = False
        self.__next_spawn_time = 0
        self.__score = 0
        self.__start_time = 0
        self.__pause_time = 0

        # Clear all game objects
        for obstacle in self.obstacles:
            for pixel in obstacle.pixels:
                pixel.delete()
        self.obstacles.clear()
        
        # Recreate dino
        for pixel in self.dino.pixels:
            pixel.delete()
        self.dino = Dino(self.canvas, self.nrow, self.ncol, self.scale, c=2)
        self.dino.activate()
        
        #recreat the start screen
        self.canvas.itemconfig("score_display", text="0")
        self.canvas.delete("score_display")
        self.canvas.create_text(60, 30, text="0",font=('Arial', 18, 'bold'), fill='white', tags="score_display")
        self.canvas.delete("high_score_display")
        self.high_score_display = self.canvas.create_text(
            300, 30,
            text=f"{self.highscore}s",
            font=('Arial', 18, 'bold'),
            fill='white',
            tag="high_score_display"
        )
    
    def better_visual(self):

        # Score display text
        score_x = 60  # Positioned 60px from left edge
        score_y = 30   # 30px from top
        
        # Score display background (semi-transparent)
        self.canvas.create_rectangle(
            score_x - 50, score_y - 20,
            score_x + 50, score_y + 20,
            fill='#333333', outline='#555555', width=1,
            tag="score_bg"
        )
        
        # Score display text (white for contrast)
        self.score_display = self.canvas.create_text(
            score_x, score_y,
            text="0", font=('Arial', 18, 'bold'),
            fill='white', tag="score_display"
        )
        self.canvas.create_text(
            200, 30,
            text="Highscore:",
            font=('Arial', 18, 'bold'),
            fill='white',
        )
        self.high_score_display = self.canvas.create_text(
            300, 30,
            text=f"{self.highscore}s",
            font=('Arial', 18, 'bold'),
            fill='white',
            tag="high_score_display"
        )
    def start_screen(self):
        self.canvas.create_text(
            self.ncol*self.scale/2, self.nrow*self.scale/2,
            text="DINO RUN",
            font=('Arial', 32, 'bold'),
            fill='white',
            tag="start_text"
        )
        self.canvas.create_text(
            self.ncol*self.scale/2, self.nrow*self.scale/2 + 50,
            text="Press S to Start",
            font=('Arial', 18),
            fill='#AAAAAA',
            tag="start_subtext"
        )
        self.canvas.create_text(
            self.ncol*self.scale/2, self.nrow*self.scale/2 + 90,
            text="Space to Jump | P to Pause",
            font=('Arial', 14),
            fill='#777777',
            tag="start_controls")
        
        self.canvas.create_text(
            self.ncol*self.scale/2, self.nrow*self.scale/2 + 130,
            text="R to Restart",
            font=('Arial', 14),
            fill='#777777',
            tag="start_controls")
        
    def is_game_over(self):
        return self.__game_over
    # Remove the pass statement and implement the is_game_over method as described in the PDF.
    
    def set_game_over(self, value):
        self.__game_over = value
    # Remove the pass statement and implement the set_game_over method as described in the PDF.
    
    def is_pause(self):
        return self.__pause
    # Remove the pass statement and implement the is_pause method as described in the PDF.
    
    def set_pause(self, value):
        self.__pause = value
    # Remove the pass statement and implement the set_pause method as described in the PDF.
    
    def is_started(self):
        return self.__started
    # Remove the pass statement and implement the is_started method as described in the PDF.
    
    def set_started(self, value):
        self.__started = value
    # Remove the pass statement and implement the set_started method as described in the PDF.
    
    def get_next_spawn_time(self):
        return self.__next_spawn_time
    # Remove the pass statement and implement the get_next_spawn_time method as described in the PDF.
    
    def set_next_spawn_time(self, value):
        self.__next_spawn_time = value
    # Remove the pass statement and implement the set_next_spawn_time method as described in the PDF.

    def get_score(self):
        return self.__score
    # Remove the pass statement and implement the get_score method as described in the PDF.
    
    def set_score(self, value):
        self.__score = value
    # Remove the pass statement and implement the set_score method as described in the PDF.

    def get_pause_time(self):
        return self.__pause_time
    # Remove the pass statement and implement the get_pause_time method as described in the PDF.
    
    def set_pause_time(self, value):
        self.__pause_time = value
    # Remove the pass statement and implement the set_pause_time method as described in the PDF.
    
    #-------------------------------------------------------------------------
    # Game Logic
    #-------------------------------------------------------------------------
    @staticmethod  #check the file if it exist or not if does then it rewrite with highscore
    def load_high_score():
    # Check if file exists, if not create it with 0
        if not os.path.exists("highscore.txt"):
            file = open("highscore.txt", "w")
            file.write("0")
            file.close()

    # Read high score value
        file = open("highscore.txt", "r")
        highscore = int(file.read())
        file.close()

        return highscore
    
    def save_highscore(self,highscore):
        if self.__score > highscore:
            highscore = self.__score
            file = open("highscore.txt", "w")
            file.write(str(highscore))
            file.close()
        self.canvas.itemconfig(
                "high_score_display",
                text=f"{highscore}s"
            )
    def start_game(self):
        if not self.__started and not self.__game_over:
            self.__started = True
            self.__game_over = False
            self.__score = 0
            self.canvas.delete('start_text','start_subtext')
            self.__start_time = time.time()
            self.__next_spawn_time = time.time() + 1
            self.update_survival_score()
    # Remove the pass statement and implement the start_game method as described in the PDF.
    def restart_game(self):
        self.reset()
        self.canvas.delete("game_over", "game_over_bg")
        self.start_screen()
        self.start_game()
        self.root.after(10, update_obstacles, self, self.root)

    
    def next(self):
        if not self.__started or self.__game_over or self.__pause:
            return
            
        # Move existing obstacles
        for obstacle in self.obstacles[:]:
            obstacle.left(step = self.obstacle_speed)
            if obstacle.j + obstacle.w < 0:  # Obstacle off screen
                self.obstacles.remove(obstacle)
        
        # Spawn new obstacles
        current_time = time.time()
        if self.__score > 45:
            self.spawn_interval = 1.0
            self.obstacle_speed = 1.5
        elif self.__score > 30:
            self.spawn_interval = 1.5
            self.obstacle_speed = 1.3
        elif self.__score > 15:
            self.spawn_interval = 2.0
            self.obstacle_speed = 1.2
        else:
            self.spawn_interval = 2.5
            self.obstacle_speed = 1
        if current_time >= self.__next_spawn_time:
            next_obstacle = Obstacles.random_select(self.canvas, self.nrow, self.ncol, self.scale)
            next_obstacle.activate()
            self.obstacles.append(next_obstacle)
            self.__next_spawn_time = current_time + random.uniform(1, self.spawn_interval)  # 1-3 seconds (will be less as the level progress)
        # Check collisions
        if self.check_collision():
            self.game_over_screen()
        
    # Remove the pass statement and implement the next method as described in the PDF.
    def game_over_screen(self):
        self.__game_over = True
        self.__started = False 
        self.stop_update = False
 
        if self.__score > self.highscore:
            self.highscore = self.__score
            file = open("highscore.txt", "w")
            file.write(str(self.highscore))
            file.close()
        self.canvas.create_rectangle(
            0, 0, 
            self.ncol*self.scale, 
            self.nrow*self.scale,
            fill='black', stipple='gray25', tag="game_over_bg"
            )
        
        # Game over text (positioned higher)
        self.canvas.create_text(
            self.ncol*self.scale/2, 
            self.nrow*self.scale/4,
            text="GAME OVER", 
            font=('Arial', 40, 'bold'),
            fill='red', 
            tag="game_over"
            )
        
        # Move score to center below game over text
        self.canvas.itemconfig("score_display", 
                             font=('Arial', 24, 'bold'),
                             fill='white')
        self.canvas.coords("score_display",
                         self.ncol*self.scale/2,
                         self.nrow*self.scale/4 + 50)
        self.canvas.itemconfig("high_score_display",
            text=f"High Score: {self.highscore}s"
        )
        self.canvas.coords("high_score_display",
            self.ncol * self.scale / 2,
            self.nrow * self.scale / 4 + 100
        )
    
    def check_collision(self):
        if not self.obstacles:
            return False
            
        for obs in self.obstacles:
            
            dino_left = self.dino.j
            dino_right = self.dino.j + self.dino.w
            dino_top = self.dino.i
            dino_bottom = self.dino.i + self.dino.h
            
            obs_left = obs.j
            obs_right = obs.j + obs.w
            obs_top = obs.i
            obs_bottom = obs.i + obs.h
            
            if dino_right > obs_left and dino_left < obs_right and dino_bottom > obs_top and dino_top < obs_bottom:
                return True
        return False
    # Remove the pass statement and implement the check_collision method as described in the PDF.
    

    def jump(self):
        if self.__started and not self.__game_over and not self.__pause:
            self.dino.jump()
    # Remove the pass statement and implement the jump method as described in the PDF.


    def pause(self):
        if not self.__started or self.__game_over:
            return
            
        self.__pause = not self.__pause
        if self.__pause:
            self.__pause_time = time.time()
        else:
            pause_duration = time.time() - self.__pause_time
            self.__start_time += pause_duration
    # Remove the pass statement and implement the pause method as described in the PDF.

    def update_survival_score(self):
        if self.__started and not self.__pause and not self.__game_over:
            self.__score = int(time.time() - self.__start_time)
            self.canvas.itemconfig(
                "score_display",
                text=f"Time: {self.__score}s"
            )  
        self.canvas.after(1000, self.update_survival_score)
    # Remove the pass statement and implement the update_survival_score method as described in the PDF.


#=============================================================================
# Main Game Runner - DO NOT MODIFY
#=============================================================================

def update_obstacles(game, root):
    if not game.is_pause() and (game.is_started() or game.is_game_over()):
        game.next()  # Unified method with feature flag
            
        if game.is_game_over():
            return  # Don't schedule another update if game is over
    
    # Schedule next update (50ms = 20 FPS)
    root.after(50, update_obstacles, game, root)

def main():
    """
    Main function to set up and run the game.
    """
    # Create the main window
    root = Tk()
    root.title("Dino Run Game")
    
    # Create the game instance
    game = DinoGame(root, nrow=80, ncol=160, scale=10)

    # Set up key bindings
    root.bind("<space>", lambda e: game.jump())
    root.bind("<p>", lambda e: game.pause())
    root.bind("<s>", lambda e: game.start_game())
    root.bind("<r>", lambda e: game.restart_game())
    # Start the game loop
    root.after(10, update_obstacles, game, root)
    
    # Start Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()