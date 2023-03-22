# https://en.wikipedia.org/wiki/Maze_generation_algorithm

import pygame
import sys
import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANT VARIABLES
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CELL_SIZE = 10
GRID_WIDTH = 69 # x
GRID_HEIGHT = 69 # y

WINDOW_TITLE = "Maze"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (222, 90, 67)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SETUP FOR GENERIC PYGAME STUFF
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pygame.init()
screen = pygame.display.set_mode((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clockspeed = pygame.time.Clock()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEFINE FUNCTIONS/CLASSES
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SETUP FOR THE GRID
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

grid = []
solid = False
for x in range(GRID_WIDTH):
    grid.append([])
    wall = False
    for y in range(GRID_HEIGHT):
        cell = Cell(x, y)
        if y == 0 or y == GRID_HEIGHT - 1:
            cell.colour = RED
            cell.visited = True
        else:
            if solid == True:
                cell.colour = BLACK
            elif wall == True:
                cell.colour = BLACK
            if x == 0 or x == GRID_WIDTH - 1:
                cell.colour = RED
                cell.visited = True
        wall = not wall
        grid[x].append(cell)
    solid = not solid

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GAME LOOP VARIABLES
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

game_active = True
cell_stack = [grid[random.randrange(2, GRID_WIDTH, 2)][random.randrange(2, GRID_HEIGHT, 2)]]
print(cell_stack)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GAME LOOP
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

while game_active:

    # how quick the loop tries to run
    clockspeed.tick(3)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # DRAW MAZE
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # cell we finished on last time
    startcell = cell_stack.pop()

    # possible cells to jump to and the walls inbetween
    possible_cells = []
    possible_walls = []

    # populate lists above, checking that the cell has not been visited before.
    try:
        possible_cell = grid[cell.y + 2][cell.x]
        if possible_cell.visited == False:
            possible_cells.append(possible_cell)
            possible_walls.append(grid[cell.y + 1][cell.x])
    except IndexError:
        pass
    try:
        possible_cell = grid[cell.y - 2][cell.x]
        if possible_cell.visited == False:
            possible_cells.append(possible_cell)
            possible_walls.append(grid[cell.y - 1][cell.x])
    except IndexError:
        pass
    try:
        possible_cell = grid[cell.y][cell.x - 2]
        if possible_cell.visited == False:
            possible_cells.append(possible_cell)
            possible_walls.append(grid[cell.y][cell.x - 1])
    except IndexError:
        pass
    try:
        possible_cell = grid[cell.y][cell.x + 2]
        if possible_cell.visited == False:
            possible_cells.append(possible_cell)
            possible_walls.append(grid[cell.y][cell.x + 1])
    except IndexError:
        pass

    # do after checking for possible cells
    startcell.visited = True

    # define the cell we move to, and the wall between it and current cell.
    endcell: Cell = None
    wall: Cell = None

    # handle possible cells if we have any, otherwise we are at a dead end.
    if len(possible_cells) != 0:
        r = random.randint(0, possible_cells.len())                   
        endcell = possible_cells[r]
        wall = possible_walls[r]
    else:
        # backtrack
        pass

    # change colour of the wall and append chosen cell to the stack
    wall.colour = WHITE
    cell_stack.append(endcell)
    
    pygame.display.flip()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False
            pygame.quit()
            sys.exit()

    # draw grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cell = grid[x][y]
            cell.draw(screen)

    pygame.display.flip()

pygame.quit()

# 1) select random (white) cell to start with
# 2) check that cell is not at edge of grid
# 3) select random neigboring (white) cell and remove wall between it and current cell, change current cell to new one and add previous to stack.
# 4) repeat step 3 until you find a cell with no unvisited neigbours (dead end)
# 5) when at a dead end backtrack until you find a cell with an unvisited neighbour. switch current cell to this one, and back to step 2.