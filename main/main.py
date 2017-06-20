"""
2D Roguelike game
Author: Gordon Stirling
Python/Pygame project
http://www1.ayrshire.ac.uk

Sprites created by: DawnBringer
https://opengameart.org/content/dawnlike-16x16-universal-rogue-like-tileset-v181

Tutorial 12 -  Encapsulation
In this tutorial we are going to tidy up our existing code and focus on the principle
of code encapsulation.  We have created a number of classes, however we also have
chunks of code related to these classes, not being handled by the class itself.  
We are going to fix that.  In the process of doing this we will also refactor the 'move'
function and add an 'attack' function in order for the code to read a bit easier and 
make more sense.

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


# component definitions
class com_Creature:
    ''' Creatures have health, can attack and damage other objects '''
    def __init__(self, name_instance, hp = 10, has_died = None):
        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp
        self.has_died = has_died

    def move(self, dx, dy):
        tile_is_wall = GAME_MAP[self.owner.x + dx][self.owner.y + dy].block_path == True

        target = map_check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)
                
        if target:
            self.attack(target, settings.ATT_DAMAGE)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):
        print (self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage!")
        target.creature.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        print (self.name_instance + "'s health is " + str(self.hp) + "/" + str(self.maxhp))

        if self.hp <= 0:
            if self.has_died is not None:
                self.has_died(self.owner)


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
        self.owner.creature.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))


def death(enemy):
    '''On death, enemy stops moving'''
    print (enemy.creature.name_instance + " is dead!")

    enemy.creature = None
    enemy.ai = None


# map definition
def create_map():
    new_map = [[ struct_Tile(False) for y in range(0, settings.MAP_HEIGHT) ] for x in range(0, settings.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    for x in range(settings.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][settings.MAP_HEIGHT-1].block_path = True

    for y in range(settings.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[settings.MAP_WIDTH-1][y].block_path = True

    return new_map


def map_check_for_creature(x, y, exclude_obj = None):
    target = None

    if exclude_obj:
        # check object list to find creature at that location that isn't excluded
        for obj in GAME_OBJECTS:
            if (obj is not exclude_obj and 
                obj.x == x and 
                obj.y == y and 
                obj.creature):
                target = obj

            if target:
                return target

    else:
        # check object list to find any creature at that location
        for obj in GAME_OBJECTS:
            if (obj.x == x and 
                obj.y == y and 
                obj.creature):
                target = obj

            if target:
                return target


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
                PLAYER.creature.move(0, -1)
                return "player_moved"

            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                return "player_moved"

            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                return "player_moved"

            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                return "player_moved"

    return "no action"


def game_init():
    '''This function initialises the main window and pygame'''

    # make a global (available to all modules) variable to hold the game window (surface)
    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS

    # initialise pygame
    pygame.init()

    #create window (surface)
    SURFACE_MAIN = pygame.display.set_mode((settings.MAP_WIDTH * settings.CELL_WIDTH, settings.MAP_HEIGHT * settings.CELL_HEIGHT))

    GAME_MAP = create_map()

    creature_com1 = com_Creature("Del")
    creature_com2 = com_Creature("Rodney", has_died = death)

    ai_com = com_AI_Test()

    PLAYER = obj_Actor(1, 1, "hero", settings.S_PLAYER, creature = creature_com1)
    ENEMY = obj_Actor(15, 10, 
                      "dark guard", 
                      settings.S_ENEMY, 
                      creature = creature_com2, 
                      ai = ai_com)

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