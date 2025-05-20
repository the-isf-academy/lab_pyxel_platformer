from sprite import Sprite

class Coin(Sprite):
    def __init__(self, img_bank, u, w, width, height, scale=1):
        super().__init__(img_bank, u, w, width, height, scale)

        self.active = True

    def inactivate(self):
        self.active = False

    def is_active(self):
        return self.active

    


