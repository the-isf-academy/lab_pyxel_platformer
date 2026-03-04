class Camera:
    def __init__(self, x, y, max_x, max_y):
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y

        self.scroll_border = 64

    def follow_player(self, player_x, player_y):
        '''Update camera to keep player centered'''

        # Horizontal
        if player_x > self.x + self.scroll_border:
            self.x = min(player_x - self.scroll_border, self.max_x)
        elif player_x < self.x + self.scroll_border:
            self.x = max(player_x - self.scroll_border, 0)

        # Vertical
        if player_y > self.y + self.scroll_border:
            self.y = min(player_y - self.scroll_border, self.max_y)
        elif player_y < self.y + self.scroll_border:
            self.y = max(player_y - self.scroll_border, 0)