# this file is based of the offical documentation
# https://github.com/kitao/pyxel?tab=readme-ov-file#how-to-use
###################################################

import pyxel
from player import Player
from coin import Coin
import helpers

class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Pyxel Platformer")
        pyxel.load("assets.pyxres")

        self.player = Player(
            img_bank=0, 
            u=5*8,              # first number is X cordinate in map editor
            w=0, 
            width=8, 
            height=8)
        
        self.coin_list = []
        self.setup_map_sprites()

        # pyxel.playm(0, loop=True) #music
        
        self.camera_x = 0
        self.scroll_border_X = 80
        self.camera_y = 0
        self.scroll_border_Y = 80

        self.score = 0
        self.scene = "start"

        pyxel.run(self.update, self.draw)
    
    def setup_map_sprites(self):
        for y in range(pyxel.tilemap(0).height):
            for x in range(pyxel.tilemap(0).width):
                tile = helpers.get_tile(x, y)

                if tile == helpers.PLAYER_TILE:
                    self.player.set_xy(x * 8, y * 8)   
                    for yi in range(y, y + (self.player.height // 8)):
                        for xi in range(x, x + (self.player.width // 8)):
                            pyxel.tilemap(0).pset(xi, yi, helpers.TRANSPARENT_TILE)
 

                if tile == helpers.COIN_TILE:
                    coin = Coin(
                        img_bank=0, 
                        u=4 * 8,        # first number is X cordinate in map editor
                        w=0 * 8, 
                        width=8, 
                        height=8,
                        scale=0.5
                    )

                    coin.set_xy(x * 8, y * 8)              
                    self.coin_list.append(coin)
                
                    pyxel.tilemap(0).pset(x, y, helpers.TRANSPARENT_TILE)  

    def draw(self):
        pyxel.cls(0)    # clear screen

        if self.scene == "start":
            self.draw_start_scene()

        elif self.scene == "game":
            self.draw_game()

    
    def draw_start_scene(self):
        pyxel.text(35, 66, "Simple Platformer", pyxel.frame_count % 16)  #cycle through color options
        pyxel.text(31, 100, "- PRESS ENTER to start-", 13)

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = "game"

    def draw_game(self):
        pyxel.camera() #reset camera
        pyxel.rect(0, 0, 128, 128, helpers.NAVY)

        # draw map
        pyxel.bltm(0, 0, 0, self.camera_x, self.camera_y, 128, 128, colkey=helpers.COLKEY)

        pyxel.camera(self.camera_x, self.camera_y) #move camera 

        self.player.draw()

        for coin in self.coin_list:
            if coin.is_active() == True:
                coin.draw()

        pyxel.text(self.camera_x, self.camera_y, f"SCORE {self.score}",helpers.BLACK) # x, y, text, color


    def update(self):
  
        self.player.update(self.camera_x)

        self.camera_x, self.camera_y = self.player.update_scroll(
            self.camera_x, 
            self.scroll_border_X,
            self.camera_y, 
            self.scroll_border_Y)

        for coin in self.coin_list:
            if self.player.collides_with(coin) and coin.is_active():
                self.score += 1
                coin.inactivate()

Game()
