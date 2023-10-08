if __name__ == "__main__":

    import pygame
    import sys

    pygame.init()

    from modules.Player import Player
    from modules.Grid import Grid
    from modules.Game import Game

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CONSTANTS + GLOBALS
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    game = Game()

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
    
    pygame.display.set_caption("Solve the maze!")
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
    running = True

    # keep track of key states
    arrow_key_state = {
        "up": True,
        "down": True,
        "left": True,
        "right": True
    }

    # main grid obj
    grid = Grid(game.grid_width, game.grid_height, game.cell_size, game.screen)

    # state
    state = Game.State.unknown

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # MAIN GAME LOOP
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    while running:

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # GAME SETUP
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # keep track of game state
        gamestate = Game.State.initialising

        # seperate from __init__() for easy redrawing
        grid.create()

        # create maze from grid
        maze = grid.backtrackRecursively(grid, True)
        
        # create player sprite, specifying cell to start on
        player = Player(grid, grid.grid_array[2][2], game.screen)
        player.draw()

        # update screen
        processBasicEvents(True)

        # keep track of time
        timer = pygame.time.get_ticks()

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # GAME PLAYING
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        gamestate = Game.State.playing 

        while gamestate == Game.State.playing:
            
            # 30 ms
            clockspeed.tick(60)

            # move if key pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or pygame.KEYUP:
                    arrow_key_state = player.move(grid, arrow_key_state, event)

            # check if at finish
            if player.cell == grid.finish:
                game.level += 1
                break

            pygame.display.flip()
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # END OF GAME LOOP
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    pygame.quit()