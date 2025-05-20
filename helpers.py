# adapted from example code at https://github.com/kitao/pyxel/tree/main/python/pyxel/examples

import pyxel

# pyxel color palette 
BLACK = 0
NAVY = 1
PURPLE = 2
GREEN = 3
BROWN = 4
GRAY_DARK = 5
GRAY_LIGHT = 6
WHITE = 7
RED = 8
ORANGE = 9
YELLOW = 10
LIME = 11
CYAN = 12
STEEL_BLUE = 13
PINK = 14
PEACH = 15

# map setup
COLKEY = BLACK
TRANSPARENT_TILE = (0,0)
COIN_TILE = (4,0)
PLAYER_TILE = (5,0)

FLOOR_Y = 16 * 8
MAP_WIDTH = 23 * 8 


WALL_TILE_POSITIONS = []
# SET RANGES BASED ON X,Y IN MAP EDITOR
for x in range(0,5):   
    for y in range(2,5):
        WALL_TILE_POSITIONS.append((x,y))

def get_tile(tile_x, tile_y):
    return pyxel.tilemaps[0].pget(tile_x, tile_y)



def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        """Helper function for calculating the start x value for centered text."""

        text_width = len(text) * char_width
        return (page_width - text_width) // 2
