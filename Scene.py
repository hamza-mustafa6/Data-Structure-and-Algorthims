import arcade


class Scene:

    def __init__(self, background, key=float('inf'), current=None, left=None, right=None, up=None, down=None, cost_up=0, cost_down=0,
                 cost_left=0, cost_right=0, treasure=False):
        self.background = arcade.load_texture(background)
        self.key = key
        self.current = current
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.cost_up = cost_up
        self.cost_down = cost_down
        self.cost_left = cost_left
        self.cost_right = cost_right
        self.treasure = treasure

    def get_cost(self, direction):
        if direction == 'up':
            return self.cost_up
        elif direction == 'down':
            return self.cost_down
        elif direction == 'left':
            return self.cost_left
        elif direction == 'right':
            return self.cost_right
        else:
            return None
