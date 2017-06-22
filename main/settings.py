import pygame
import libtcodpy as libtcod

# initialise pygame
pygame.init()

# window sizes
SURFACE_WIDTH = 800
SURFACE_HEIGHT = 600

# game sizes
CELL_WIDTH = 32
CELL_HEIGHT = 32

#FPS LIMIT
G_FPS = 60

# map variables
MAP_WIDTH = 20
MAP_HEIGHT = 20

# colour definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
RED = (255, 0, 0)

# game colours
DEFAULT_BG_COLOUR = GREY

# sprites
S_PLAYER = pygame.image.load("res/player.png")
S_ENEMY = pygame.image.load("res/enemy.png")
S_WALL = pygame.image.load("res/wall_v2.jpg")
S_WALL_EXPLORED = pygame.image.load("res/wall_unseen.png")
S_FLOOR = pygame.image.load("res/floor.png")
S_FLOOR_EXPLORED = pygame.image.load("res/floor_unseen.png")

# sprite default positions
PLAYER_POS_DEFAULT = (200, 200)

# game values
ATT_DAMAGE = 5

#FOV settings
FOV_ALGO = libtcod.FOV_BASIC
FOV_LIGHT_WALLS = True
FOV_RADIUS = 10

# Font settings
FONT_DEBUG_MESSAGE = pygame.font.Font("res/joystix.ttf", 20)
