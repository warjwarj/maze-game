# https://en.wikipedia.org/wiki/Maze_generation_algorithm

import pygame
import sys
import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS + GLOBALS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CELL_SIZE = 10 # in px
GRID_WIDTH = 69 # x
GRID_HEIGHT = 69 # y

WINDOW_TITLE = "Maze"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (222, 90, 67)

grid = []

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SETUP FOR GENERIC PYGAME STUFF
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pygame.init()
screen = pygame.display.set_mode((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clockspeed = pygame.time.Clock()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEFINE CLASSS AND FUNCTIONS
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

class PlayerSprite(pygame.sprite.Sprite):
    
    def __init__(self, cell):
        super.__init__()
        self.image = pygame.Surface(CELL_SIZE * 0.7, CELL_SIZE * 0.7)
        pygame.draw.circle(self.image, RED, [cell.x, cell.y], CELL_SIZE / 2)

def processBasicEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()

# maze generation
def recursiveBacktracker():

    # stack cells we have visited and take them off when a dead end is reached.
    cell_stack = [grid[random.randrange(2, GRID_WIDTH, 2)][random.randrange(2, GRID_HEIGHT, 2)]]

    # use to exit loop
    drawing_maze = True

    # recurse
    while drawing_maze:

        clockspeed.tick()

        # define cell we finished on last time
        startcell = cell_stack[-1]

        # define lists for possible cells to jump to and the walls inbetween
        possible_cells = []
        possible_walls = []

        # populate lists above, checking that the cell has not been visited before.
        try:
            possible_cell = grid[startcell.x + 2][startcell.y]
            if possible_cell.visited == False:
                possible_cells.append(possible_cell)
                possible_walls.append(grid[startcell.x + 1][startcell.y])
        except IndexError:
            pass
        try:
            possible_cell = grid[startcell.x - 2][startcell.y]
            if possible_cell.visited == False:
                possible_cells.append(possible_cell)
                possible_walls.append(grid[startcell.x - 1][startcell.y])
        except IndexError:
            pass
        try:
            possible_cell = grid[startcell.x][startcell.y - 2]
            if possible_cell.visited == False:
                possible_cells.append(possible_cell)
                possible_walls.append(grid[startcell.x][startcell.y - 1])
        except IndexError:
            pass
        try:
            possible_cell = grid[startcell.x][startcell.y + 2]
            if possible_cell.visited == False:
                possible_cells.append(possible_cell)
                possible_walls.append(grid[startcell.x][startcell.y + 1])
        except IndexError:
            pass

        # do after checking for possible cells
        startcell.visited = True

        # no dead end
        if len(possible_cells) != 0:

            # random number
            r = random.randint(0, len(possible_cells) - 1)

            # change colour of wall inbetween cells and append randomly chosen cell to the stack
            cell_stack.append(possible_cells[r])
            possible_walls[r].colour = WHITE
            possible_walls[r].draw(screen)

        # dead end
        else:

            # backtrack by one cell & check if we have finished, return if so
            cell_stack.pop()
            if len(cell_stack) == 0:
                drawing_maze = False

        processBasicEvents()

    return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GRID SETUP
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# create and populate the grid
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

# draw grid
for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
        cell = grid[x][y]
        cell.draw(screen)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GAME LOOP VARIABLES
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

game_active = True
draw_maze = True
cell_stack = [grid[random.randrange(2, GRID_WIDTH, 2)][random.randrange(2, GRID_HEIGHT, 2)]]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GAME LOOP
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

while game_active:

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # SETUP MAZE
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # check if finished
    if draw_maze:
        recursiveBacktracker()
        draw_maze = False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # HANDLE EVENTS
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    processBasicEvents()

pygame.quit()

# 1) select random (white) cell to start with
# 2) check that cell is not at edge of grid
# 3) select random neigboring (white) cell and remove wall between it and current cell, change current cell to new one and add previous to stack.
# 4) repeat step 3 until you find a cell with no unvisited neigbours (dead end)
# 5) when at a dead end backtrack until you find a cell with an unvisited neighbour. switch current cell to this one, and back to step 2.