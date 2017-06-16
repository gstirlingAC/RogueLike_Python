"""
2D Roguelike game
Author: Gordon Stirling
Python/Pygame project
http://www1.ayrshire.ac.uk

Tutorial 3 -  Create the main game loop
In this tutorial we begin to flesh out a structure for our code, 
specifically the main game loop.  This time we will replace the
pseudocode with actual python code.  We will define the basic
game loop and give the player a way to quit out of the program. 

We will also create new file (module) which will hold all of our 
constant variables (variables whose values never change).

In the next tutorial we will draw something to the newly created
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


# call the functions to make the game run
if __name__ == '__main__':
    game_init()
    game_main_loop()