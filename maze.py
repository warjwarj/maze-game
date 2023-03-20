# https://en.wikipedia.org/wiki/Maze_generation_algorithm

import pygame
import sys
import random

# constants for window dimensions
CELL_SIZE = 20
GRID_WIDTH = 41
GRID_HEIGHT = 41

# window title
WINDOW_TITLE = "Maze"

# predifined colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# use to instantiate cells and refer back to them
class Cell(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.colour = WHITE

    def draw(self, surface):
        rect = pygame.Rect(
            self.x * CELL_SIZE,
            self.y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(surface, self.colour, rect)

# Initialize Pygame
pygame.init()

# Set up the screen = cell size in px * how many there are
screen = pygame.display.set_mode((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# use this variable to tick the frames along (FramePerSec.tick(60))
FramePerSec = pygame.time.Clock()

# Create the 2D list used to store the instances of cells
grid = []
solid = True
for x in range(GRID_WIDTH):
    grid.append([])
    wall = True
    for y in range(GRID_HEIGHT):
        cell = Cell(x, y)
        if solid == True:
            cell.colour = BLACK
        elif wall == True:
            cell.colour = BLACK
        wall = not wall
        grid[x].append(cell)
    solid = not solid

# Game loop
while True:

    FramePerSec.tick(10)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # draw the grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cell = grid[x][y]
            cell.draw(screen)

    # start drawing maze
    all_cells_visited = False # change to exit loop
    cell = grid[round(GRID_WIDTH / 2)][round(GRID_HEIGHT / 2)] # start at middle, reassign to current cell

    #while not all_cells_visited:
        # do something

    # Update the screen
    pygame.display.flip()

# Clean up
pygame.quit()

# 1) select random (white) cell to start with
# 2) check that cell is not at edge of grid
# 3) select random neigboring (white) cell and remove wall between it and current cell, change current cell to new one and add previous to stack.
# 4) repeat step 3 until you find a cell with no unvisited neigbours (dead end)
# 5) when at a dead end backtrack until you find a cell with an unvisited neighbour. switch current cell to this one, and back to step 2.