# https://en.wikipedia.org/wiki/Maze_generation_algorithm
# https://coderslegacy.com/python/python-pygame-tutorial/

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SETUP FOR GENERIC PYGAME STUFF
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pygame.init()
SCREEN_SURFACE = pygame.display.set_mode((CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clockspeed = pygame.time.Clock()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEFINE CLASSS AND FUNCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def processBasicEvents(update_display=True):
    if pygame.event.peek(pygame.QUIT):
        pygame.quit()
        sys.exit()
    if update_display:
        pygame.display.flip()

class Cell(pygame.sprite.Sprite):

    def __init__(self, x, y, cell_size):
        super().__init__()
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.visited = False
        self.colour = WHITE

    def draw(self, surface):
        rect = pygame.Rect(
            self.x * self.cell_size,
            self.y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(surface, self.colour, rect)

class Grid():

    @staticmethod
    def draw(cols, rows, cell_size):
        grid = []
        # setup grid
        solid = False
        for x in range(cols):
            grid.append([])
            wall = False
            for y in range(rows):
                cell = Cell(x, y, cell_size)
                if y == 0 or y == rows - 1:
                    cell.colour = RED
                    cell.visited = True
                else:
                    if solid == True:
                        cell.colour = BLACK
                    elif wall == True:
                        cell.colour = BLACK
                    if x == 0 or x == cols - 1:
                        cell.colour = RED
                        cell.visited = True
                wall = not wall
                grid[x].append(cell)
            solid = not solid

        # draw grid
        for x in range(cols):
            for y in range(rows):
                cell = grid[x][y]
                cell.draw(SCREEN_SURFACE)
            
        return grid
    
    # maze generation
    @staticmethod
    def backtrackRecursively(grid, draw_maze_visible):

        # stack cells we have visited and take them off when a dead end is reached.
        cell_stack = [grid.grid_array[random.randrange(2, grid.col_num, 2)][random.randrange(2, grid.row_num, 2)]]

        # use to exit loop
        drawing_maze = True

        # recurse
        while drawing_maze:

            # define cell we finished on last time
            startcell = cell_stack[-1]

            # define lists for possible cells to jump to and the walls inbetween
            possible_cells = []
            possible_walls = []

            # populate lists above, checking that the cell has not been visited before.
            try:
                possible_cell = grid.grid_array[startcell.x + 2][startcell.y]
                if possible_cell.visited == False:
                    possible_cells.append(possible_cell)
                    possible_walls.append(grid.grid_array[startcell.x + 1][startcell.y])
            except IndexError:
                pass
            try:
                possible_cell = grid.grid_array[startcell.x - 2][startcell.y]
                if possible_cell.visited == False:
                    possible_cells.append(possible_cell)
                    possible_walls.append(grid.grid_array[startcell.x - 1][startcell.y])
            except IndexError:
                pass
            try:
                possible_cell = grid.grid_array[startcell.x][startcell.y - 2]
                if possible_cell.visited == False:
                    possible_cells.append(possible_cell)
                    possible_walls.append(grid.grid_array[startcell.x][startcell.y - 1])
            except IndexError:
                pass
            try:
                possible_cell = grid.grid_array[startcell.x][startcell.y + 2]
                if possible_cell.visited == False:
                    possible_cells.append(possible_cell)
                    possible_walls.append(grid.grid_array[startcell.x][startcell.y + 1])
            except IndexError:
                pass

            # mark visited
            startcell.visited = True

            # no dead end
            if len(possible_cells) != 0:

                # random number
                r = random.randint(0, len(possible_cells) - 1)

                # change colour of wall inbetween cells and append randomly chosen cell to the stack
                cell_stack.append(possible_cells[r])
                possible_walls[r].colour = WHITE
                possible_walls[r].draw(SCREEN_SURFACE)

            # dead end
            else:

                # backtrack by one cell & check if we have finished, return if so
                cell_stack.pop()
                if len(cell_stack) == 0:
                    drawing_maze = False

            if draw_maze_visible:
                processBasicEvents()
            else:
                processBasicEvents(False)

        return

    def __init__(self, col_num, row_num, cell_size):
        self.grid_array = Grid.draw(col_num, row_num, cell_size)
        self.col_num = col_num
        self.row_num = row_num
        self.cell_size = cell_size

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GAME LOOP VARIABLES
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

game_active = True
draw_maze = True
grid = Grid(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GAME LOOP
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

while game_active:

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # SETUP MAZE
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # check if finished
    if draw_maze:
        grid.backtrackRecursively(grid, True)
        draw_maze = False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # HANDLE EVENTS
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    processBasicEvents()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# END OF GAME LOOP
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pygame.quit()