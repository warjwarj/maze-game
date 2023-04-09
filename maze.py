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
DARK_BLUE = (15, 99, 255)
GREY = (92, 92, 92)
LIGHTER_GRAY = (145, 145, 145)
GREEN = (28, 252, 3)

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

# regarding player/cell movement chronology:
# on construction, define possible cells to move to, highlight.
# move to that cell, in ONE call of the move function.
# after player has moved then calculate possible cells again

class Player(pygame.sprite.Sprite):

    # the possible cells that a player can move to, if they are on the given cell.
    # "y+" IS DOWN AND "y-" IS UP. I REVERSE SO THAT APPEARS LOGICAL IN MOVEMENT DICT
    def getmovements(self, grid):

        self.movements.clear()

        cell = self.cell

        print(cell)

        xposition = cell.x
        yposition = cell.y

        # single operator = one cell in specified direction
        # double operator = furthest reachable cell in specified direction
        if grid.grid_array[xposition + 1][yposition].wall == False:
            self.movements["x+"] = grid.grid_array[xposition + 1][yposition]
        
        if grid.grid_array[xposition - 1][yposition].wall == False:
            self.movements["x-"] = grid.grid_array[xposition - 1][yposition]

        if grid.grid_array[xposition][yposition - 1].wall == False:
            self.movements["y+"] = grid.grid_array[xposition][yposition - 1]

        if grid.grid_array[xposition][yposition + 1].wall == False:
            self.movements["y-"] = grid.grid_array[xposition][yposition + 1]
                  
        # set these flags when we reach a wall in a direction | positive, negative
        xPos, xNeg, yPos, yNeg = True, True, True, True

        # loop for no more than the max width/height of the grid
        for i in range(1, grid.col_num if grid.col_num > grid.row_num else grid.row_num):

            if xPos:
                try:
                    if grid.grid_array[xposition + i][yposition].wall == False:
                        self.movements["x++"] = grid.grid_array[xposition + i][yposition]
                    else:
                        xPos = False
                except IndexError:
                    self.movements["x++"] = 0
                    pass
            if xNeg:
                try:
                    if grid.grid_array[xposition - i][yposition].wall == False:
                        self.movements["x--"] = grid.grid_array[xposition - i][yposition]
                    else:
                        xNeg = False
                except IndexError:
                    self.movements["x--"] = 0
                    pass
            if yPos:
                try:
                    if grid.grid_array[xposition][yposition + i].wall == False:
                        self.movements["y--"] = grid.grid_array[xposition][yposition + i]
                    else:
                        yPos = False
                except IndexError:
                    self.movements["y--"] = 0
                    pass
            if yNeg:
                try:
                    if grid.grid_array[xposition][yposition - i].wall == False:
                        self.movements["y++"] = grid.grid_array[xposition][yposition - i]
                    else:
                        yNeg = False
                except IndexError:
                    self.movements["y++"] = 0
                    pass

        for i in self.movements.keys():
            if self.movements[i]:
                grid.higlighted_cells.add(self.movements[i])
                if len(i) == 3:
                    self.movements[i].colour = LIGHTER_GRAY
                    self.movements[i].draw(SCREEN_SURFACE)

        print(self.movements)
 

    # draw player cell
    def draw(self):
        self.rect = pygame.Rect(
            self.cell.x * self.cell.cell_size,
            self.cell.y * self.cell.cell_size,
            self.cell.cell_size,
            self.cell.cell_size
        )
        pygame.draw.rect(self.screen, DARK_BLUE, self.rect)

    def move(self, grid, arrow_key_state, event):

        print(event.type)
        
        grid.higlighted_cells.update()

        mods = pygame.key.get_mods()

        if event.type == pygame.KEYDOWN:
            if mods and pygame.KMOD_SHIFT:
                if event.key == pygame.K_LEFT and arrow_key_state["left"] and "x--" in self.movements and self.movements["x--"]:
                        # move left
                        self.cell = self.movements["x--"]
                        arrow_key_state["left"] = False
                elif event.key == pygame.K_RIGHT and arrow_key_state["right"] and "x++" in self.movements and self.movements["x++"]:
                        # move right
                        self.cell = self.movements["x++"]
                        arrow_key_state["right"] = False
                elif event.key == pygame.K_UP and arrow_key_state["up"] and "y++" in self.movements and self.movements["y++"]:
                        # move up
                        self.cell = self.movements["y++"]
                        arrow_key_state["up"] = False
                elif event.key == pygame.K_DOWN and arrow_key_state["down"] and "y--" in self.movements and self.movements["y--"]:
                        # move down
                        self.cell = self.movements["y--"]
                        arrow_key_state["down"] = False
            else:
                if event.key == pygame.K_LEFT and arrow_key_state["left"] and "x-" in self.movements and self.movements["x-"]:
                        # move left
                        self.cell = self.movements["x-"]
                        arrow_key_state["left"] = False
                elif event.key == pygame.K_RIGHT and arrow_key_state["right"] and "x+" in self.movements and self.movements["x+"]:
                        # move right
                        self.cell = self.movements["x+"]
                        arrow_key_state["right"] = False
                elif event.key == pygame.K_UP and arrow_key_state["up"] and "y+" in self.movements and self.movements["y+"]:
                        # move up
                        self.cell = self.movements["y+"]
                        arrow_key_state["up"] = False
                elif event.key == pygame.K_DOWN and arrow_key_state["down"] and "y-" in self.movements and self.movements["y-"]:
                        # move down
                        self.cell = self.movements["y-"]
                        arrow_key_state["down"] = False
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                arrow_key_state = { key: True for key in arrow_key_state }

        self.getmovements(grid)

        self.draw()

        return arrow_key_state

    def __init__(self, grid, start_cell, surface):
        super().__init__()
        self.cell = start_cell
        self.screen = surface
        self.surface = pygame.Surface((start_cell.cell_size, start_cell.cell_size))
        self.rect = self.surface.get_rect()
        self.rect.topleft = (start_cell.x * grid.cell_size, start_cell.y * grid.cell_size)
        surface.blit(self.surface, self.rect)
        self.movements = { "x+": 0, "x-": 0, "y+": 0, "y-": 0, "x++": 0, "x--": 0, "y++": 0, "y--": 0 }
        self.getmovements(grid)

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
        
        def update(self, colour=WHITE):
            self.colour = colour
            self.draw(SCREEN_SURFACE)

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
                        cell.wall = True
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
                possible_walls[r].wall = False
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
        self.higlighted_cells = pygame.sprite.Group()
        self.col_num = col_num
        self.row_num = row_num
        self.cell_size = cell_size

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GAME LOOP VARIABLES
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

game_active = True

playing = True

# keep track of key states
arrow_key_state = {
    "up": True,
    "down": True,
    "left": True,
    "right": True
}

# main grid obj
grid = Grid(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GAME LOOP
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

while game_active:

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # GAME SETUP
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    grid.backtrackRecursively(grid, False)
    
    # create player sprite, specifying cell to start on
    player = Player(grid, grid.grid_array[2][2], SCREEN_SURFACE)
    player.draw()

    # update screen
    processBasicEvents(True)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # PLAY GAME
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    while playing:
        
        # 30 ms
        clockspeed.tick(10)

        # move if key pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or pygame.KEYUP:
                arrow_key_state = player.move(grid, arrow_key_state, event)

        pygame.display.flip()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# END OF GAME LOOP
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pygame.quit()