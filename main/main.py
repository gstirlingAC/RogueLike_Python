"""
2D Roguelike game
Author: Gordon Stirling
Python/Pygame project
http://www1.ayrshire.ac.uk

Tutorial 4 -  Draw to the surface - Pseudocode
In this tutorial we will create a pseudocode blueprint 
for a function which will be used to draw objects to the 
surface.

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

        #process input
        for event in events:
            if event.type == pygame.QUIT:
                game_quit = True

        #TODO draw the game

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

    #TODO clear the surface
    #TODO draw the map
    #TODO draw the character
    # update the display
    pygame.display.flip()

# call the functions to make the game run
if __name__ == '__main__':
    game_init()
    game_main_loop()