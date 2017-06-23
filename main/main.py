"""
2D Roguelike game
Author: Gordon Stirling
Python/Pygame project
http://www1.ayrshire.ac.uk

Sprites created by: DawnBringer
https://opengameart.org/content/dawnlike-16x16-universal-rogue-like-tileset-v181

Tutorial 15 -  In-game message console
Continuing on from the previous tutorial we are going to finish off creating the
in-game message console.  By the end of this tutorial the messages which previously
were printed to the console will now display on-screen.  We will limit the number of
messages on-screen to 4, with older messages disappearing.

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
        self.explored = False


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
        is_visible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)

        if is_visible:
            SURFACE_MAIN.blit(self.sprite, (self.x * settings.CELL_WIDTH, 
                                            self.y * settings.CELL_HEIGHT))


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
        game_message (self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage!", settings.WHITE)
        
        target.creature.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        game_message (self.name_instance + "'s health is " + str(self.hp) + "/" + str(self.maxhp), settings.RED)

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
    game_message (enemy.creature.name_instance + " is dead!", settings.GREY)

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

    map_make_fov(new_map)

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


def map_make_fov(incoming_map):
    global FOV_MAP

    FOV_MAP = libtcod.map_new(settings.MAP_WIDTH, settings.MAP_HEIGHT)

    for y in range(settings.MAP_HEIGHT):
        for x in range(settings.MAP_WIDTH):
            libtcod.map_set_properties(FOV_MAP, x, y, 
                                       not incoming_map[x][y].block_path,
                                       not incoming_map[x][y].block_path)


def map_calculate_fov():
    global FOV_CALCULATE

    if FOV_CALCULATE:
        FOV_CALCULATE = False
        libtcod.map_compute_fov(FOV_MAP, 
                                PLAYER.x, 
                                PLAYER.y, 
                                settings.FOV_RADIUS, 
                                settings.FOV_LIGHT_WALLS,
                                settings.FOV_ALGO)


def draw_map(map_to_draw):

    for x in range(0, settings.MAP_WIDTH):
        for y in range(0, settings.MAP_HEIGHT):

            is_visible = libtcod.map_is_in_fov(FOV_MAP, x, y)

            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path == True:
                    # draw wall
                    SURFACE_MAIN.blit(settings.S_WALL, (x * settings.CELL_WIDTH, y * settings.CELL_HEIGHT))
                else:
                    # draw floor
                    SURFACE_MAIN.blit(settings.S_FLOOR, (x * settings.CELL_WIDTH, y * settings.CELL_HEIGHT))

            elif map_to_draw[x][y].explored:

                if map_to_draw[x][y].block_path == True:
                    # draw wall
                    SURFACE_MAIN.blit(settings.S_WALL_EXPLORED, (x * settings.CELL_WIDTH, y * settings.CELL_HEIGHT))
                else:
                    # draw floor
                    SURFACE_MAIN.blit(settings.S_FLOOR_EXPLORED, (x * settings.CELL_WIDTH, y * settings.CELL_HEIGHT))


# function definitions
def draw_text(display_surface, text_to_display, T_coords, text_colour, back_colour = None):
    '''This function takes in some text, and displays it on the reference surface'''
    
    text_surf, text_rect = get_text_objs(text_to_display, text_colour, back_colour)

    text_rect.topleft = T_coords

    display_surface.blit(text_surf, text_rect)


# helper functions
def get_text_objs(incoming_text, incoming_colour, incoming_bg):
    if incoming_bg:
        text_surface = settings.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_colour, incoming_bg)
    else:
        text_surface = settings.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_colour)
    return text_surface, text_surface.get_rect()


def get_text_height(font):
    font_obj = font.render('a', False, (0, 0, 0))
    font_rect = font_obj.get_rect()

    return font_rect.height


def draw_game():
    '''We will use this function to draw objects to the surface'''

    # clear (reset) the surface
    SURFACE_MAIN.fill(settings.DEFAULT_BG_COLOUR)

    # draw the map
    draw_map(GAME_MAP)

    # draw the character
    for obj in GAME_OBJECTS:
        obj.draw()

    draw_debug()
    draw_messages()

    # update the display
    pygame.display.flip()


def draw_messages():
    if len(GAME_MESSAGES) <= settings.NUM_MESSAGES: 
        to_draw = GAME_MESSAGES
    else:
        to_draw = GAME_MESSAGES[-settings.NUM_MESSAGES:]

    text_height = get_text_height(settings.FONT_MESSAGE_TEXT)

    start_y = (settings.MAP_HEIGHT * settings.CELL_HEIGHT - (settings.NUM_MESSAGES * text_height)) - 10

    i = 0

    for message, colour in to_draw:
        draw_text(SURFACE_MAIN, message, (0, start_y + (i * text_height)), colour, settings.BLACK)
        i += 1


def draw_debug():
    draw_text(SURFACE_MAIN, "FPS: " + str(int(CLOCK.get_fps())), (0,0), settings.WHITE, settings.BLACK)


def game_player_input():
    global FOV_CALCULATE

    # get player input
    events = pygame.event.get()

    #  process input - more events to come
    for event in events:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player_moved"

            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player_moved"

            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player_moved"

            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player_moved"

    return "no action"


def game_message(game_msg, msg_colour):
    GAME_MESSAGES.append((game_msg, msg_colour))


def game_init():
    '''This function initialises the main window and pygame'''

    # make a global (available to all modules) variable to hold the game window (surface)
    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS, FOV_CALCULATE, CLOCK, GAME_MESSAGES

    # initialise pygame
    pygame.init()

    CLOCK = pygame.time.Clock()

    #create window (surface)
    SURFACE_MAIN = pygame.display.set_mode((settings.MAP_WIDTH * settings.CELL_WIDTH, settings.MAP_HEIGHT * settings.CELL_HEIGHT))

    GAME_MAP = create_map()

    GAME_MESSAGES = []

    FOV_CALCULATE = True

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

        map_calculate_fov()

        if player_action == "QUIT":
            game_quit = True

        if player_action != "no action":
            for obj in GAME_OBJECTS:
                if obj.ai:
                    obj.ai.take_turn()

        # draw the game
        draw_game()

        CLOCK.tick(settings.G_FPS)

    # quit the game
    pygame.quit()
    exit()


# call the initialisation functions to make the game run
if __name__ == '__main__':
    game_init()
    game_main_loop()