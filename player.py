# adapted from example code at https://github.com/kitao/pyxel/tree/main/python/pyxel/examples

import pyxel
from sprite import Sprite
import helpers 

class Player(Sprite):
    def __init__(self, img_bank, u, w, width, height, scale=1):
        super().__init__(img_bank, u, w, width, height, scale)

        self.x = 0
        self.y = 0

        self.dx = 0
        self.dy = 0
        
        self.speed = 2
        self.gravity = 5
        self.direction = 1

        self.jump_strength = 10
        self.is_falling = False

        self.is_jumping = False

    def update(self, scroll_x):
        last_y = self.y

        # Handle horizontal movement
        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -self.speed
            self.direction = -1

        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = self.speed
            self.direction = 1
        else:
            self.dx = 0
        
        # Ensure player stays within screen bounds
        self.x = max(self.x, scroll_x)
        self.y = max(self.y, 0)

        # Update falling state
        self.is_falling = self.y > last_y
        # Apply gravity
        self.dy = min(self.dy + 1, self.gravity)

        # Update position with collision handling
        self.x, self.y = self.push_back(self.x, self.y, self.dx, self.dy)

    
        if self.dy >= self.gravity:
            self.is_jumping = False

        # Handle jumping
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.is_falling and not self.is_jumping:
            self.dy = -self.jump_strength
            self.is_jumping = True
                        

    def update_scroll(self, camera_x, scroll_border_x, camera_y, scroll_border_y):
         #right scroll
        if self.x > camera_x + scroll_border_x:
            camera_x = min(self.x - scroll_border_x, 184)

        # left scroll
        elif self.x + 20 > scroll_border_x:  
            camera_x = max(self.x - scroll_border_x,0)

        # down scroll
        if self.y >= helpers.FLOOR_Y:
            target_camera_y = abs(helpers.FLOOR_Y - self.y) + 16
            camera_y += min(5, target_camera_y - camera_y)
            
        # up scroll
        elif self.y < helpers.FLOOR_Y:
            camera_y -= min(2, camera_y) 

        return (camera_x,camera_y)


        