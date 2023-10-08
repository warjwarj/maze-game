import pygame
import random
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (222, 90, 67)
DARK_BLUE = (15, 99, 255)
GREY = (92, 92, 92)
LIGHTER_GRAY = (145, 145, 145)
GREEN = (28, 252, 3)

class Grid():

    class Cell(pygame.sprite.Sprite):

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
            self.draw(self.screen)
        
        def __init__(self, x, y, cell_size, screen):
            super().__init__()
            self.screen = screen
            self.x = x
            self.y = y
            self.cell_size = cell_size
            self.visited = False
            self.colour = WHITE
            self.wall = False
            self.finish = False

    def draw(self, cols, rows, cell_size):
        grid = []
        # setup grid
        solid = False
        for x in range(cols):
            grid.append([])
            wall = False
            for y in range(rows):
                cell = Grid.Cell(x, y, cell_size, self.screen)
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
                cell.draw(self.screen)

        self.finish = grid[rows - 3][cols - 3]
        self.finish.finish = True
        self.finish.colour = GREEN
        self.finish.draw(self.screen)
            
        return grid
    
    # maze generation
    def backtrackRecursively(self, grid, draw_maze_visible):

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
                possible_walls[r].draw(self.screen)

            # dead end
            else:

                # backtrack by one cell & check if we have finished, return if so
                cell_stack.pop()
                if len(cell_stack) == 0:
                    drawing_maze = False

            if draw_maze_visible:
                if pygame.event.peek(pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                pygame.display.flip()
            else:
                if pygame.event.peek(pygame.QUIT):
                    pygame.quit()
                    sys.exit()

    def create(self):
        self.grid_array = Grid.draw(self, self.col_num, self.row_num, self.cell_size)
        self.higlighted_cells = pygame.sprite.Group()

    def __init__(self, col_num, row_num, cell_size, screen):
        self.screen = screen
        self.col_num = col_num
        self.row_num = row_num
        self.cell_size = cell_size