# https://en.wikipedia.org/wiki/Maze_generation_algorithm

import pygame
import sys
import random

# constants for window dimensions
CELL_SIZE = 10
GRID_WIDTH = 69 # x
GRID_HEIGHT = 69 # y

# window title
WINDOW_TITLE = "Maze"

# predifined colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (222, 90, 67)

# use to instantiate cells and refer back to them
class Cell(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.coordinates = str(str(x) + "," + str(y))
        self.visited = False
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
solid = False
for x in range(GRID_WIDTH):
    grid.append([])
    wall = False
    for y in range(GRID_HEIGHT):
        cell = Cell(x, y)
        if y == 0 or y == GRID_HEIGHT - 1:
            cell.colour = WHITE
            cell.visited = True
        else:
            if solid == True:
                cell.colour = BLACK
            elif wall == True:
                cell.colour = BLACK
            if x == 0 or x == GRID_WIDTH - 1:
                cell.colour = WHITE
                cell.visited = True
        wall = not wall
        grid[x].append(cell)
    solid = not solid

cellStack = [] # add visited cells to here
maze_is_drawing = True # change to exit loop
cell = grid[random.randrange(2, GRID_WIDTH, 2)][random.randrange(2, GRID_HEIGHT, 2)] # start at middle, reassign to current cell
cell.colour = RED
print(cell.x, cell.y)

# Game loop
while True:

    FramePerSec.tick(60)

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

    # move maze cursor per iteration of loop
    # if maze_is_drawing:
    #     possibleCells = [
    #         grid[cell.x + 2][cell.y],
    #         grid[cell.x - 2][cell.y],
    #         grid[cell.x][cell.y + 2],
    #         grid[cell.x][cell.y - 2]
    #     ]
    #     print(possibleCells)

    # Update the screen
    pygame.display.flip()



# Clean up
pygame.quit()

# 1) select random (white) cell to start with
# 2) check that cell is not at edge of grid
# 3) select random neigboring (white) cell and remove wall between it and current cell, change current cell to new one and add previous to stack.
# 4) repeat step 3 until you find a cell with no unvisited neigbours (dead end)
# 5) when at a dead end backtrack until you find a cell with an unvisited neighbour. switch current cell to this one, and back to step 2.