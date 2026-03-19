# this file is based of the offical documentation
# https://github.com/kitao/pyxel?tab=readme-ov-file#how-to-use
# https://kitao.github.io/pyxel/wasm/api-reference/
###################################################

import pyxel
from player import Player
from coin import Coin
from camera import Camera
import helpers

class Game:
    def __init__(self):
        self.width = 64*2
        self.height = 64*2

        pyxel.init(self.width, self.height, title="Pyxel Platformer")
        pyxel.load("assets.pyxres")

        self.player = Player(
            img_bank = 0, 
            editX = 40, 
            editY = 0, 
            width = 8, 
            height = 8*2,
            scale = 1)
          
        self.coin_list = []
        
        self.level = 0

        self.setup_map_sprites(self.level )
        
        self.camera = Camera(
            x = 0,
            y = 0,
            max_x = self.width,
            max_y = self.height,
        )

        self.score = 0

        self.scene = "start_screen"

        print(pyxel.tilemaps)

        pyxel.run(self.update, self.draw)
    
    def setup_map_sprites(self, tile_map):
        """Reads in the map data and sets up Sprites"""
    
        for y in range(pyxel.tilemap(tile_map).height):
            for x in range(pyxel.tilemap(tile_map).width):
                tile = pyxel.tilemaps[tile_map].pget(x, y)

                if tile == helpers.PLAYER_TILE:
                    self.player.set_pos(x * 8, y * 8)   

                    for tileY in range(y, y + (self.player.height // 8)):
                        for tileX in range(x, x + (self.player.width // 8)):
                            pyxel.tilemaps[tile_map].pset(tileX, tileY, helpers.TRANSPARENT_TILE)
 

                if tile == helpers.COIN_TILE:
                    coin = Coin(
                        img_bank = 0, 
                        editX = 26, 
                        editY = 2, 
                        width = 4, 
                        height = 4,
                        scale = 1)

                    coin.set_pos(x * 8, y * 8)              
                    self.coin_list.append(coin)
                
                    pyxel.tilemap(tile_map).pset(x, y, helpers.TRANSPARENT_TILE)  

    def draw(self):
        """Controls what is drawn on the screen"""

        pyxel.cls(0)    # clear screen

        if self.scene == "start_screen":
            self.draw_start_scene()

        elif self.scene == "play_game":
            self.draw_play()

    def draw_map(self, mapX, mapY, cameraX, cameraY, tile_map):
        """Handles how the map is drawn"""

        pyxel.bltm(
            x= mapX, 
            y = mapY, 
            tm = tile_map, 
            u = cameraX, 
            v = cameraY, 
            w = self.width, 
            h = self.height, 
            colkey=helpers.COLKEY)
        

        
    def draw_start_scene(self):
        """Controls what is drawn on the start screen"""

        pyxel.text(
            x = self.width//2 - 30,
            y = self.height/2, 
            s= "Simple Platformer", 
            col = pyxel.frame_count % 16)  #cycle through color options
        
        pyxel.text(
            x = self.width//2 - 40, 
            y = self.height/1.5, 
            s = "- PRESS ENTER to start-", 
            col = 13)

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = "play_game"

    def draw_play(self):
        """Controls what is drawn when the game is being played"""

        pyxel.camera() #reset camera
        pyxel.rect(0, 0, 128, 128, helpers.NAVY)    # draws background

        # draw map
        self.draw_map(0, 0, self.camera.x, self.camera.y, self.level)

        # draw camera
        pyxel.camera(self.camera.x, self.camera.y)

        # draws Player
        self.player.draw()

        # draws Coins if active
        for coin in self.coin_list:
            if coin.active == True:
                coin.draw()

        # draws score relative to camera position 
        pyxel.text(self.camera.x, self.camera.y, f"SCORE {self.score}", helpers.BLACK) # x, y, text, color



    def update(self):
        """Controls what happens each frame of the game"""

        # Moves the Player
        self.player.movement(self.level)
        
        # Checks if Player collides with a Coin
        for coin in self.coin_list:
            if self.player.collides_with(coin) and coin.active == True:
                self.score += 1
                coin.set_active(False)
                self.level = 1


        # update camera based on Player position
        self.camera.follow_player(self.player.posX, self.player.posY)


Game()
