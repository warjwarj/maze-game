# https://en.wikipedia.org/wiki/Maze_generation_algorithm
# https://coderslegacy.com/python/python-pygame-tutorial/

import pygame
import sys
import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS + GLOBALS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CELL_SIZE = 30 # in px
GRID_WIDTH = 29 # x
GRID_HEIGHT = 29 # y

WINDOW_TITLE = "Maze"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (222, 90, 67)
BLUE = (3, 198, 252)

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

class Player(pygame.sprite.Sprite):

    # the possible cells that a player can move to, if they are on the given cell.
    @staticmethod
    def possibleCells(cell, grid):

        # single operator = one cell in specified direction
        # double operator = furthest reachable cell in specified direction
        possibleCells = { "x+": 0, "x-": 0, "y+": 0, "y-": 0, "x++": 0, "x--": 0, "y++": 0, "y--": 0 }

        if grid.grid_array[cell.x + 1][cell.y].wall == False:
            possibleCells["x+"] = grid.grid_array[cell.x + 1][cell.y]
        if grid.grid_array[cell.x - 1][cell.y].wall == False:
            possibleCells["x-"] = grid.grid_array[cell.x - 1][cell.y]
        if grid.grid_array[cell.x][cell.y + 1].wall == False:
            possibleCells["y+"] = grid.grid_array[cell.x][cell.y + 1]
        if grid.grid_array[cell.x][cell.y - 1].wall == False:
            possibleCells["y-"] = grid.grid_array[cell.x][cell.y - 1]
        
        populated = False
              
        # loop for no more than the max width/height of the grid
        for i in range(grid.col_num if grid.col_num > grid.row_num else grid.row_num, 1):

            if not possibleCells["x++"] and grid[cell.x + i][cell.y].wall == False:
                possibleCells["x++"] = grid[cell.x + 1][cell.y]
            if not possibleCells["x--"] and grid[cell.x - i][cell.y].wall == False:
                possibleCells["x--"] = grid[cell.x - i][cell.y]
            if not possibleCells["y++"] and grid[cell.x][cell.y + i].wall == False:
                possibleCells["y++"] = grid[cell.x][cell.y + i]
            if not possibleCells["y--"] and grid[cell.x][cell.y - i].wall == False:
                possibleCells["y--"] = grid[cell.x][cell.y - i]

        vlas = list(possibleCells.values())
        print(vlas)
        for i in vlas:
            vlas[i].colour = BLUE
        
        pygame.display.flip()
            
        

    def __init__(self, grid, start_cell, surface):
        super().__init__()
        self.cell = start_cell
        self.surface = pygame.Surface((start_cell.cell_size, start_cell.cell_size))
        surface.blit(self.surface, self.surface.get_rect())
        self.possibleCells(self.cell, grid)

    def move(self, grid):

        processBasicEvents(False)

        #self.possibleCells(grid)

        for event in pygame.event.get():
            if event == pygame.event.K_UP:
                self.cell
            if event == pygame.event.K_DOWN:
                self.rect.move_ip(0, 5)
            if event == pygame.eventK_LEFT:
                self.rect.move_ip(-5, 0)
            if event == pygame.eventK_RIGHT:
                self.rect.move_ip(5, 0)


class Grid():

    class Cell(pygame.sprite.Sprite):

        def __init__(self, x, y, cell_size):
            super().__init__()
            self.x = x
            self.y = y
            self.cell_size = cell_size
            self.visited = False
            self.colour = WHITE
            self.wall = False

        def draw(self, surface):
            self.rect = pygame.Rect(
                self.x * self.cell_size,
                self.y * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(surface, self.colour, self.rect)

    @staticmethod
    def draw(cols, rows, cell_size):
        grid = []
        # setup grid
        solid = False
        for x in range(cols):
            grid.append([])
            wall = False
            for y in range(rows):
                cell = Grid.Cell(x, y, cell_size)
                if y == 0 or y == rows - 1:
                    cell.colour = RED
                    cell.visited = True
                else:
                    if solid == True:
                        cell.colour = BLACK
                        cell.wall = True
                    elif wall == True:
                        cell.colour = BLACK
                        cell.wall = True
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
playing = True

draw_maze = True
grid = Grid(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GAME LOOP
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

while game_active:

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # GAME SETUP
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # check if finished
    if draw_maze:
        grid.backtrackRecursively(grid, False)
        draw_maze = False
    
    # create player sprite, passing cell to start on
    player = Player(grid, grid.grid_array[2][2], SCREEN_SURFACE)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # PLAY GAME
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    while playing:
        
        # 30 ms
        clockspeed.tick(30)

        # process input for movement of the player sprite
        player.move()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# END OF GAME LOOP
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pygame.quit()