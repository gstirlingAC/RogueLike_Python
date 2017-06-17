"""
2D Roguelike game
Author: Gordon Stirling
Python/Pygame project
http://www1.ayrshire.ac.uk

Sprites created by: DawnBringer
https://opengameart.org/content/dawnlike-16x16-universal-rogue-like-tileset-v181

Tutorial 6 -  Tiles and Maps
In this tutorial we are going to create individual tiles which we will then use to
construct a map to form the game world.  We will begin by defining a 'struct' type 
object (Python doesn't technically support Structs, but any C-based language does.
Python does support Classes (Classes and Structs are very similar) however so we 
will use a Class in order to create our struct-type tile object.  We will then
define a function which will let us generate an empty map.

"""

# 3rd party modules
import pygame
import libtcodpy as libtcod

# game modules
import settings


# struct definition
class struct_Tile:
    def __init__(self, block_path):
        self.block_path = block_path

# map definition
def create_map():
    new_map = [[ struct_Tile(False) for y in range(0, settings.MAP_HEIGHT) ] for x in range(0, settings.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    return new_map

def draw_map(map_to_draw):

    for x in range(0, settings.MAP_WIDTH):
        for y in range(0, settings.MAP_HEIGHT):
            if map_to_draw[x][y].block_path == True:
                # draw wall
                SURFACE_MAIN.blit(settings.S_WALL, (x * settings.CELL_WIDTH, y * settings.CELL_HEIGHT))

            else:
                # draw floor
                SURFACE_MAIN.blit(settings.S_FLOOR, (x * settings.CELL_WIDTH, y * settings.CELL_HEIGHT))

# function definitions
def draw_game():
    '''We will use this function to draw objects to the surface'''

    # clear (reset) the surface
    SURFACE_MAIN.fill(settings.DEFAULT_BG_COLOUR)

    # draw the map
    draw_map(GAME_MAP)

    # draw the character
    SURFACE_MAIN.blit(settings.S_PLAYER, (settings.PLAYER_POS_DEFAULT))

    # update the display
    pygame.display.flip()

def game_init():
    '''This function initialises the main window and pygame'''

    # make a global (available to all modules) variable to hold the game window (surface)
    global SURFACE_MAIN, GAME_MAP

    # initialise pygame
    pygame.init()

    #create window (surface)
    SURFACE_MAIN = pygame.display.set_mode((settings.SURFACE_WIDTH, settings.SURFACE_HEIGHT))

    GAME_MAP = create_map()

def game_main_loop():
    '''This function loops the main game'''

    game_quit = False

    while not game_quit:
        # get player input
        events = pygame.event.get()

        # TODO process input - more events to come
        for event in events:
            if event.type == pygame.QUIT:
                game_quit = True

        # draw the game
        draw_game()

    # quit the game
    pygame.quit()
    exit()


# call the initialisation functions to make the game run
if __name__ == '__main__':
    game_init()
    game_main_loop()