"""
2D Roguelike game
Author: Gordon Stirling
Python/Pygame project
http://www1.ayrshire.ac.uk

Sprites created by: DawnBringer
https://opengameart.org/content/dawnlike-16x16-universal-rogue-like-tileset-v181

Tutorial 9 -  Thinking turn-based
In this tutorial we are going to implement the beginnings of a turn-based 
system.  We will be making mostly just minor changes existing code (refactoring).
Enemy objects will be controlled by a new ai component, and will only move
when the player has moved.

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


# object definitions
class obj_Actor:
    def __init__(self, x, y, name_object, sprite, creature = None, ai = None):
        self.x = x # map address
        self.y = y # map address
        self.sprite = sprite
        self.creature = creature
        self.ai = ai

        if creature:
            creature.owner = self
        
        if ai:
            ai.owner = self

    def draw(self):
        SURFACE_MAIN.blit(self.sprite, (self.x * settings.CELL_WIDTH, self.y * settings.CELL_HEIGHT))

    def move(self, dx, dy):
        if GAME_MAP[self.x + dx][self.y + dy].block_path == False:
            self.x += dx
            self.y += dy


# component definitions
class com_Creature:
    ''' Creatures have health, can attack and damage other objects '''
    def __init__(self, name_instance, hp = 10):
        self.name_instance = name_instance
        self.hp = hp


#TODO define Item component - consumables etc.
class com_Item:
    pass


#TODO define Container component - loot chests etc.
class com_Container:
    pass


#TODO define AI component - turns, attacking, moving etc.
class com_AI_Test:
    '''Once per turn, execute'''

    def take_turn(self):
        self.owner.move(-1, 0)


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
    for obj in GAME_OBJECTS:
        obj.draw()

    # update the display
    pygame.display.flip()


def game_player_input():
    # get player input
    events = pygame.event.get()

    #  process input - more events to come
    for event in events:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.move(0, -1)
                return "player_moved"

            if event.key == pygame.K_DOWN:
                PLAYER.move(0, 1)
                return "player_moved"

            if event.key == pygame.K_LEFT:
                PLAYER.move(-1, 0)
                return "player_moved"

            if event.key == pygame.K_RIGHT:
                PLAYER.move(1, 0)
                return "player_moved"

    return "no action"


def game_init():
    '''This function initialises the main window and pygame'''

    # make a global (available to all modules) variable to hold the game window (surface)
    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS

    # initialise pygame
    pygame.init()

    #create window (surface)
    SURFACE_MAIN = pygame.display.set_mode((settings.SURFACE_WIDTH, settings.SURFACE_HEIGHT))

    GAME_MAP = create_map()

    creature_com1 = com_Creature("Del")
    creature_com2 = com_Creature("Rodney")

    ai_com = com_AI_Test()

    PLAYER = obj_Actor(0, 0, "hero", settings.S_PLAYER, creature = creature_com1)
    ENEMY = obj_Actor(20, 10, "dark guard", settings.S_ENEMY, creature = creature_com2, ai = ai_com)

    GAME_OBJECTS = [PLAYER, ENEMY]


def game_main_loop():
    '''This function loops the main game'''

    game_quit = False

    # player action definition
    player_action = "no action"

    while not game_quit:
        
        # handle player input
        player_action = game_player_input()

        if player_action == "QUIT":
            game_quit = True

        if player_action != "no action":
            for obj in GAME_OBJECTS:
                if obj.ai:
                    obj.ai.take_turn()

        # draw the game
        draw_game()

    # quit the game
    pygame.quit()
    exit()


# call the initialisation functions to make the game run
if __name__ == '__main__':
    game_init()
    game_main_loop()