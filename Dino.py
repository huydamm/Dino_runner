from tkinter import *
from Pixel import Pixel
import numpy as np

class Dino(Pixel):
    def __init__(self, canv, nrow, ncol, scale, c=2):
        self.canvas = canv
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.c = c
        self.pattern = self.get_pattern()
        self.h = len(self.pattern)
        self.w = len(self.pattern[0])
        self.jumping = False
    # Remove the pass statement and implement the __init__ method as described in the PDF.


    def get_pattern(self):
        return np.array([
            [0, 0, 1, 1, 1, 1],
            [0, 0, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 1],
            [0, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 0, 0],
            [1, 1, 1, 1, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 0]
        ])
    # Remove the pass statement and implement the get_pattern method as described in the PDF.


    def activate(self):
        self.pixels = []
        self.i = self.nrow // 2 - self.h // 2 - 3
        self.j = 10
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
        

    def down(self):
        for pixel in self.pixels:
            self.canvas.delete(pixel.shape)
        self.i += 1
        self.pixels.clear()
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
        for pixel in self.pixels:
            pixel.i += 1
    # Remove the pass statement and implement the down method as described in the PDF.


    def up(self):
        for pixel in self.pixels:
            self.canvas.delete(pixel.shape)
        self.i -= 1
        self.pixels.clear()
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
        for pixel in self.pixels:
            pixel.i -= 1
    # Remove the pass statement and implement the up method as described in the PDF.


    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.steps = 0
            self.activate_jump()
    # Remove the pass statement and implement the jump method as described in the PDF.


    def activate_jump(self):
        if self.jumping and self.steps < 20:  
            if self.steps < 10:  
                self.up()
            else:  
                self.down()
            
            self.steps += 1
            self.canvas.after(40, self.activate_jump)
        else:
            self.jumping = False
            
                
    # Remove the pass statement and implement the perform_jump method as described in the PDF.
    

#=============================================================================
# Testing Functions for Dinosaur Class - DO NOT MODIFY
#=============================================================================

def delete_all(canvas):
    canvas.delete("all")

def test1(root, canvas, nrow, ncol, scale):
    d = Dino(canvas, nrow, ncol, scale)
    # Activate the dino in the middle left of the canvas
    d.activate()
    
    # Bind only up and down arrow keys to test basic movement
    root.bind("<Up>", lambda e: d.up())
    root.bind("<Down>", lambda e: d.down())
    
    # Add a visual indicator for test1
    print("\nPress Up/Down arrow keys to move the dinosaur up and down.\n")

def test2(root, canvas, nrow, ncol, scale):
    d = Dino(canvas, nrow, ncol, scale)
    # Activate the dino in the middle of the canvas.
    d.activate()
    
    # Bind arrow keys to move the dino
    root.bind("<space>", lambda e: d.jump())  # Bind spacebar to jump

    print("\nPress Spacebar to make the dinosaur jump.\n")



def main():
    """Initialize the game window and start the application."""
    root = Tk()
    nrow = 40
    ncol = 80
    scale = 20
    canvas = Canvas(root, width=ncol * scale, height=nrow * scale, bg="black")
    canvas.pack()

    # Bind a key for clearing the canvas.
    root.bind("1", lambda e: test1(root, canvas, nrow, ncol, scale))
    root.bind("2", lambda e: test2(root, canvas, nrow, ncol, scale))
    root.bind("d", lambda e: delete_all(canvas))

    instructions = """
    Press '1' to test basic up/down movement.
    Press '2' to test jump movement.
    Press 'd' to clear the canvas.
    """
    print(instructions)

    root.mainloop()

if __name__ == "__main__":
    main()