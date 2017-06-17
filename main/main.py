"""
2D Roguelike game
Author: Gordon Stirling
Python/Pygame project
http://www1.ayrshire.ac.uk

Sprites created by: DawnBringer
https://opengameart.org/content/dawnlike-16x16-universal-rogue-like-tileset-v181

Tutorial 5 -  Draw to the surface
In this tutorial we will swap out the pseudocode with python code to 
define the draw_game() function which will be used to draw objects to the 
surface.  For this tutorial, we will concentrate on drawing the player
sprite to the main surface and giving it a default position.

"""

# 3rd party modules
import pygame
import libtcodpy as libtcod

# game modules
import settings

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


def game_init():
    '''This function initialises the main window and pygame'''

    # make a global (available to all modules) variable to hold the game window (surface)
    global SURFACE_MAIN

    # initialise pygame
    pygame.init()

    #create window (surface)
    SURFACE_MAIN = pygame.display.set_mode((settings.SURFACE_WIDTH, settings.SURFACE_HEIGHT))


def draw_game():
    '''We will use this function to draw objects to the surface'''

    # clear (reset) the surface
    SURFACE_MAIN.fill(settings.DEFAULT_BG_COLOUR)

    #TODO draw the map

    # draw the character
    SURFACE_MAIN.blit(settings.S_PLAYER, (settings.PLAYER_POS_DEFAULT))

    # update the display
    pygame.display.flip()

# call the functions to make the game run
if __name__ == '__main__':
    game_init()
    game_main_loop()