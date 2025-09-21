from tkinter import *
from Pixel import Pixel
import random
import numpy as np

class Obstacles:
    def __init__(self, canv, nrow, ncol, scale, c=2, pattern=None):
        self.canvas = canv
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.c = c
        if pattern:
            self.pattern = pattern
        else:
            self.pattern=self.get_pattern()
        self.h = len(self.pattern)
        self.w = len(self.pattern[0])  
        self.pixels = []
    # Remove the pass statement and implement the __init__ method as described in the PDF.


    def get_pattern(self):
        return np.array([
        [1, 1, 1],
        [1, 1, 1], 
        [1, 1, 1]
    ])  
    # Remove the pass statement and implement the get_pattern method as described in the PDF.
    

    def activate(self):
        self.pixels = []
        self.i = self.nrow // 2 - self.h // 2
        self.j = self.ncol - self.w

        for row in range(self.h):
            for col in range(self.w):
                if self.pattern[row][col]:
                    pixel = Pixel(
                        self.canvas,
                        self.i + row,
                        self.j + col,
                        self.nrow,
                        self.ncol,
                        self.scale,
                        self.c
                    )
                    self.pixels.append(pixel)
    # Remove the pass statement and implement the activate method as described in the PDF.
            

    def left(self,step=1):
        for pixel in self.pixels:
            pixel.left(step)
        self.j -= step    
        
    # Remove the pass statement and implement the left method as described in the PDF.


    @staticmethod
    def random_select(canv, nrow, ncol, scale):
        obstacle_class = random.choice([Box, Tree, Pencil])
        return obstacle_class(canv, nrow, ncol, scale)

    # Remove the pass statement and implement the random_select method as described in the PDF.


#=============================================================================
# All Child Classes
#=============================================================================

class Box(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        pattern = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]
        super().__init__(canv, nrow, ncol, scale, c=2, pattern=pattern)
    # Remove the pass statement and implement the __init__ method as described in the PDF.


class Tree(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        pattern = [
            [1, 1, 1],
            [1, 1, 1],
            [0, 1, 0]
        ]
        super().__init__(canv, nrow, ncol, scale, c=3, pattern=pattern)
    # Remove the pass statement and implement the __init__ method as described in the PDF.

        
class Pencil(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        pattern = [
            [1],
            [1],
            [1],
            [1]
        ]
        super().__init__(canv, nrow, ncol, scale, c=5, pattern=pattern)
    # Remove the pass statement and implement the __init__ method as described in the PDF.



#=============================================================================
# Testing Functions for Obstacles Class - DO NOT MODIFY
#=============================================================================

def delete_all(canvas):
    """Clear all elements from the canvas."""
    canvas.delete("all")
    print("Canvas cleared")


def test1(root, canvas, nrow, ncol, scale):
    print("\nPress left arrow key to move the obstacle left\n")
    obs = Obstacles.random_select(canvas, nrow, ncol, scale)
    obs.activate()

    def left():
        obs.left()  # Move the obstacle left

    root.bind("<Left>", lambda e: left())  # Bind left arrow key to move obstacle

def test2(root, canvas, nrow, ncol, scale):
    obstacle = None  # Only one obstacle active at a time
    paused = False   # Pause flag
    print("\nPress 'p' to pause/resume the obstacle movement\n")

    def toggle_pause(event=None):
        nonlocal paused
        paused = not paused
        print("Paused" if paused else "Resumed")

    # Bind the "p" key to toggle pause
    root.bind("<p>", toggle_pause)

    def update():
        nonlocal obstacle, paused
        if not paused:
            if obstacle is None:
                obstacle = Obstacles.random_select(canvas, nrow, ncol, scale)
                obstacle.activate()
            else:
                obstacle.left()  # Move the obstacle one step left using your updated left() method
                # Check if the obstacle is completely off-screen
                if obstacle.j + obstacle.w <= 0:  # Clear the canvas when the obstacle leaves
                    obstacle = None
                    
        # Schedule the next update after 20 milliseconds (adjust as needed)
        root.after(20, update)

    update()  # Start the update loop


def main():
    """
    Main function to set up and run the obstacle testing interface.
    """
    root = Tk()
    root.title("Obstacle Test")
    nrow = 40
    ncol = 80
    scale = 10
    canvas = Canvas(root, width=ncol*scale, height=nrow*scale, bg="black")
    canvas.pack()

    # Key bindings
    root.bind("1", lambda e: test1(root, canvas, nrow, ncol, scale))
    root.bind("2", lambda e: test2(root, canvas, nrow, ncol, scale))
    root.bind("<d>", lambda e: delete_all(canvas))

    instructions = """
    Press '1' to simulate Dino Run obstacles moving left
    Press '2' to simulate Dino Run obstacles continuously moving left
    Press 'd' to clear the canvas
    """
    print(instructions)
    
    root.mainloop()

if __name__ == "__main__":
    main()