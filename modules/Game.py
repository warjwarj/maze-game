import pygame
import enum

class Game():
    
    #font = pygame.font.Font(None, 36)

    def __init__(self):

        # default
        self.score = 0
        self.level = 0

        # screen 'Surface' object
        self.screen = pygame.display.set_mode((900, 900))

        # initialise as easy maze
        self.grid_width = 25
        self.grid_height = 25
        self.cell_size = 36

        # font
        self.font = pygame.font.Font(None, 36)

    class State(enum.Enum):

        initialising = "initialising"

        initialised = "initialised"

        playing = "playing"

        unknown = "unknown"