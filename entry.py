if __name__ == "__main__":
    import pygame
    import sys

    from utils.Player import Player
    from utils.Grid import Grid


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
    # CLASSES + FUNCTIONS
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def processBasicEvents(update_display=True):
        if pygame.event.peek(pygame.QUIT):
            pygame.quit()
            sys.exit()
        if update_display:
            pygame.display.flip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # GAME LOOP VARIABLES
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # while game window is active
    game_active = True

    # while user is playing game
    playing = True

    # keep track of key states
    arrow_key_state = {
        "up": True,
        "down": True,
        "left": True,
        "right": True
    }

    # main grid obj
    grid = Grid(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, SCREEN_SURFACE)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # GAME LOOP
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    while game_active:

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # GAME SETUP
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # create maze from grid
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