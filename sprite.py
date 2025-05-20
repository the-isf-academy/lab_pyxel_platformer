import pyxel
import helpers

class Sprite:
    def __init__(self, img_bank, u, w, width, height, scale=1):
        self.img_bank = img_bank
        self.width = width
        self.height = height
        self.u = u
        self.w = w
        self.scale = scale
        self.x = 0
        self.y = 0

        self.active = True
    
    def set_xy(self, x, y):
        self.x = x
        self.y = y

    def set_active(self, bool):
        self.active = bool

    def draw(self):
        pyxel.blt(
            self.x, 
            self.y, 
            self.img_bank, 
            self.u, 
            self.w, 
            self.width, 
            self.height, 
            colkey=helpers.COLKEY,
            scale = self.scale
            )
    

    def push_back(self, x, y, dx, dy):
        # Vertical movement
        step_y = 1 if dy > 0 else -1
        for _ in range(abs(int(dy))):
            if self.is_colliding(x, y + step_y, helpers.WALL_TILE_POSITIONS):
                break
            y += step_y

        # Horizontal movement
        step_x = 1 if dx > 0 else -1
        for _ in range(abs(int(dx))):
            if self.is_colliding(x + step_x, y, helpers.WALL_TILE_POSITIONS):
                break
            x += step_x

        return x, y

    def is_colliding(self, x, y, tiles):
        """Check if the sprite at (x, y) collides with any solid tile."""
        x1 = x // 8
        y1 = y // 8
        x2 = (x + self.width - 1) // 8
        y2 = (y + self.height - 1) // 8

        for yi in range(y1, y2 + 1):
            for xi in range(x1, x2 + 1):
                if helpers.get_tile(xi, yi) in tiles:
                    return True
        return False

    def collides_with(self, other_sprite):

        return (
            self.x < other_sprite.x + other_sprite.width and
            self.x + self.width > other_sprite.x and
            self.y < other_sprite.y + other_sprite.height and
            self.y + self.height > other_sprite.y
        )
    
 