import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (222, 90, 67)
DARK_BLUE = (15, 99, 255)
GREY = (92, 92, 92)
LIGHTER_GRAY = (145, 145, 145)
GREEN = (28, 252, 3)

class Player(pygame.sprite.Sprite):

    # the possible cells that a player can move to, if they are on the given cell.
    # "y+" IS DOWN AND "y-" IS UP. I REVERSE SO THAT APPEARS LOGICAL IN MOVEMENT DICT
    def getmovements(self, grid):

        self.movements.clear()

        cell = self.cell

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
                    self.movements[i].draw(self.screen)

    # draw player cell
    def draw(self):
        self.rect = pygame.Rect(
            self.cell.x * self.cell.cell_size,
            self.cell.y * self.cell.cell_size,
            self.cell.cell_size,
            self.cell.cell_size
        )
        pygame.draw.rect(self.screen, DARK_BLUE, self.rect)

    # regarding player/cell movement chronology:
    # on construction, define possible cells to move to, highlight.
    # move to that cell, in ONE call of the move function.
    # after player has moved then calculate possible cells again

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