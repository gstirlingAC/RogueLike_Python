import pygame

# initialise pygame
pygame.init()

# window sizes
SURFACE_WIDTH = 800
SURFACE_HEIGHT = 600

# colour definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)

# game colours
DEFAULT_BG_COLOUR = GREY

# sprites
S_PLAYER = pygame.image.load("res/player.png")

# sprite default positions
PLAYER_POS_DEFAULT = (200, 200)
