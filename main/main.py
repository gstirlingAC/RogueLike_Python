"""
2D Roguelike game
Author: Gordon Stirling
Python/Pygame project
http://www1.ayrshire.ac.uk

Tutorial 2 -  Pseudocode for main game loop
In this tutorial we begin to flesh out a structure for our code, 
specifically the main game loop.  

We begin that process by creating a 'blueprint' for our game 
loop through a process called pseudo-programming (or pseudocode).

"""

# 3rd party modules
import pygame
import libtcodpy as libtcod

# game modules


'''Pseudo-programming (pseudocode):
Pseudo-code is an informal way to express the design of a 
computer program or an algorithm.  The aim is to get the idea quickly 
and also easy to read without details.  It is like a young child 
putting sentences together without any grammar.  There are several ways 
of writing pseudo-code; there are no strict rules.  But to reduce ambiguity 
between what you are required to do and what you express let’s base the 
pseudo code on the few defined conventions'''

def game_main_loop():
    '''This function loops the main game'''

    #TODO create a variable to control when the game ends, set it to False

    #TODO game while loop:
        #TODO get player input
        #TODO process input
        #TODO draw the game

    #TODO quit the game

def game_init():
    '''This function initialises the main window and pygame'''

    #TODO make a global (available to all modules) variable to hold the game window (surface)
    #TODO initialise pygame
    #TODO create window (surface)

#TODO call the functions to make the game run