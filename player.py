# adapted from example code with the help of Github copilot 
# https://github.com/kitao/pyxel/tree/main/python/pyxel/examples

import pyxel
import helpers 

class Player:
    def __init__(self, img_bank, editX, editY, width, height, scale):
        # drawing the Player
        self.img_bank = img_bank
        self.width = width
        self.height = height
        self.editX = editX
        self.editY = editY
        self.scale = scale

        # position
        self.posX = 0
        self.posY = 0

        # movement
        self.velocityX = 0
        self.velocityY = 0
        self.speed = 2
        self.gravity = .8
        self.direction = 1  # 1 = right; -1 = left

        # jumping and falling
        self.jump_strength = 10
        self.max_fall_speed = 8 
        self.is_falling = False
        self.is_jumping = False

    def set_pos(self, x, y):
        '''Set posX, posY position'''

        self.posX = x
        self.posY = y

    def draw(self):
        '''Draw Player at current location'''

        pyxel.blt(
            self.posX, 
            self.posY, 
            self.img_bank, 
            self.editX, 
            self.editY, 
            self.width, 
            self.height, 
            colkey=helpers.COLKEY,
            scale = self.scale)

    def movement(self, tile_map):
        """Controls how the Player moves"""

        last_y = self.posY

        # Handle horizontal movement
        if pyxel.btn(pyxel.KEY_LEFT):
            self.velocityX = -self.speed
            self.direction = -1

        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.velocityX = self.speed
            self.direction = 1
        else:
            self.velocityX = 0
        
        # Apply gravity 
        self.apply_gravity()
        
        # Handle jumping
        self.jumping()

        # Ensure player stops at walls
        self.push_back(tile_map)

        # Update falling state
        self.is_falling = self.posY > last_y

    def apply_gravity(self):
        """Controls the gravity effects"""

        self.velocityY += self.gravity
        
        # Cap falling speed to prevent too-drastic falls
        self.velocityY = min(self.velocityY, self.max_fall_speed)
      
            

    def jumping(self):
        """Controls keyboard press for jumping and jumping mechanic"""

        if pyxel.btnp(pyxel.KEY_SPACE) and not self.is_falling and not self.is_jumping:
            self.velocityY = -self.jump_strength
            self.is_jumping = True

        if self.velocityY >= self.gravity:
            self.is_jumping = False


    def push_back(self, tile_map):
        """Moves Player back if it hits a wall
        
            Do not edit this method.
        """
        
        # Vertical movement
        step_y = 1 if self.velocityY > 0 else -1
        for i in range(abs(int(self.velocityY))):
            if self.is_colliding(self.posX, self.posY + step_y, helpers.WALL_TILE_POSITIONS, tile_map):
                break
            self.posY += step_y

        # Horizontal movement
        step_x = 1 if self.velocityX > 0 else -1
        for i in range(abs(int(self.velocityX))):
            if self.is_colliding(self.posX + step_x, self.posY, helpers.WALL_TILE_POSITIONS, tile_map):
                break
            self.posX += step_x
                    
    
    def is_colliding(self, x, y, tiles, tile_map):
        '''Checks if Player is colliding with a specific tiles
        
            Do not edit this method.
        '''

        # Calculate the tile range based on the sprite's width and height
        x1 = pyxel.floor(x) // 8
        y1 = pyxel.floor(y) // 8
        x2 = pyxel.floor(x + self.width - 1) // 8
        y2 = pyxel.floor(y + self.height - 1) // 8

        # Check for collisions within the tile range
        for tileY in range(y1, y2 + 1):
            for tileX in range(x1, x2 + 1):
                if pyxel.tilemaps[tile_map].pget(tileX, tileY) in tiles:
                    return True

        return False


    def collides_with(self, other_sprite):
        '''Check is Player collides with another Sprite
        
            Do not edit this method.
        '''

        return (
            self.posX < other_sprite.posX + other_sprite.width and
            self.posX + self.width > other_sprite.posX and
            self.posY < other_sprite.posY + other_sprite.height and
            self.posY + self.height > other_sprite.posY
        )



        