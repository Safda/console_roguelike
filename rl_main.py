global libtcod, GameOb, con, game_map, fov_recompute

import libtcodpy as libtcod
from classes import Object as GameOb
from classes import Tile as Tile

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 80
MAP_WIDTH = 80
MAP_HEIGHT = 45
LIMIT_FPS = 20
FOV_ALGO = 1
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 6

fov_recompute = True

colour_std_dark_wall = libtcod.Color(0,0,100)
colour_std_lit_wall = libtcod.Color(130,110,50)
colour_std_dark_ground = libtcod.Color(50,50,150)
colour_std_lit_ground = libtcod.Color(200,180,50)

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
#Primary Console, console 0
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)

#Offscreen console
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

centerx = int(SCREEN_WIDTH/2)
centery = int(SCREEN_HEIGHT/2)

player_name = 'Safda'
player = GameOb.Object(0, 0, 'O', player_name, libtcod.white, True)
objects = [player]

for object in objects:
    print(object)

playerx = player.x
playery = player.y

def fov_recompute_set():
    fov_recompute = True
    return fov_recompute

def render_all(fov_recompute):
#Print offscreen console, con, to console 0

    if fov_recompute:
        #recompute FOV if needed (the player moved or something)
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            
            visible = libtcod.map_is_in_fov(fov_map, x, y)
            wall = game_map[x][y].blocked
            if not visible:
                if game_map[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con,x,y,colour_std_dark_wall,libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con,x,y,colour_std_dark_ground, libtcod.BKGND_SET)
            else:
                if wall:
                    libtcod.console_set_char_background(con,x,y,colour_std_lit_wall,libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con,x,y,colour_std_lit_ground,libtcod.BKGND_SET)
                game_map[x][y].explored = True

    for object in objects:
        object.draw(con, fov_map)

    #Update screen
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def handle_keys():

    key = libtcod.console_check_for_keypress(True)

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'
    
    if game_state == 'playing':
        #Movement Keys
        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            player.move_attack(0,-1,game_map, objects)
            fov_recompute_set()
        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            player.move_attack(0,1,game_map, objects)
            fov_recompute_set()
        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            player.move_attack(-1,0,game_map, objects)
            fov_recompute_set()
        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            player.move_attack(1,0,game_map, objects)
            fov_recompute_set()
    else:
        return 'didnt-take-turn'

#Set up the Map
game_map = Tile.Tile.make_map(MAP_HEIGHT, MAP_WIDTH, player, objects)

#Set up Field of Vision map for Libtcodpy
fov_map = libtcod.map_new(MAP_WIDTH,MAP_HEIGHT)
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, x, y, not game_map[x][y].block_sight, not game_map[x][y].blocked)

game_state = 'playing'
player_action = None

#~~~~~~~~~~~~~~~~
#Primary Loop
#~~~~~~~~~~~~~~~~
while not libtcod.console_is_window_closed():
    render_all(fov_recompute)

    libtcod.console_flush()

    for object in objects:
        object.clear(con)

    player_action = handle_keys()
    if player_action == 'exit':
        break

    if game_state == 'playing' and player_action != 'didnt-take-turn':
        for object in objects:
            if object != player:
                #print('{} {} turn.'.format(object.name, objects.index(object)))
                bob = 5
        player_action = 'didnt-take-turn'