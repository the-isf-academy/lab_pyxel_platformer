# this file is based of the offical documentation
# https://github.com/kitao/pyxel?tab=readme-ov-file#how-to-use
###################################################

import pyxel
from player import Player
from coin import Coin
import helpers

class Game:
    def __init__(self):
        self.width = 128
        self.height = 128

        pyxel.init(self.width, self.height, title="Pyxel Platformer")
        pyxel.load("assets.pyxres")

        self.player = Player(
            img_bank=0, 
            u=5*8,              # first number is X cordinate in map editor
            w=0, 
            width=8, 
            height=16)          # each square is 1 pixel
        
        self.coin_list = []
        self.setup_map_sprites()
        
        self.camera_x = 0
        self.camera_y = 0
        self.scroll_border_X = 80
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
                        width=4, 
                        height=4                    )

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
        pyxel.text(
            x=helpers.center_text("Simple Platformer", self.width, char_width=pyxel.FONT_WIDTH),
            y = self.height/2, 
            s= "Simple Platformer", 
            col = pyxel.frame_count % 16)  #cycle through color options
        
        pyxel.text(
            x = helpers.center_text("- PRESS ENTER to start-", self.width, char_width=pyxel.FONT_WIDTH), 
            y = self.height/1.5, 
            s = "- PRESS ENTER to start-", 
            col = 13)

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = "game"

    def draw_game(self):
        pyxel.camera() #reset camera
        pyxel.rect(0, 0, 128, 128, helpers.NAVY)

        # draw map
        pyxel.bltm(0, 0, 0, self.camera_x, self.camera_y, 128, 128, colkey=helpers.COLKEY)

        # draw camera
        pyxel.camera(self.camera_x, self.camera_y) 

        self.player.draw()

        for coin in self.coin_list:
            if coin.is_active() == True:
                coin.draw()

        pyxel.text(self.camera_x, self.camera_y, f"SCORE {self.score}",helpers.BLACK) # x, y, text, color


    def update(self):
  
        self.player.update(self.camera_x)

        # update camera based on player
        self.camera_x, self.camera_y = self.player.update_scroll(
            self.camera_x, 
            self.camera_y, 
            self.scroll_border_X,
            self.scroll_border_Y)
        
        for coin in self.coin_list:
            if self.player.collides_with(coin) and coin.is_active():
                self.score += 1
                coin.inactivate()

Game()
