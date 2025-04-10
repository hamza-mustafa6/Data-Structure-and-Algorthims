import arcade

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.x_pos = 200
        self.y_pos = 300
        self.x_dir = 1
        self.y_dir = 1

        self.rect_width = 200
        self.rect_height = 40
        self.xr_pos = 500
        self.yr_pos = 50


    def on_draw(self):
        self.clear(arcade.color.BLUE_GRAY)
        arcade.draw_circle_filled(self.x_pos, self.y_pos, 30, arcade.color.GHOST_WHITE)
        self.x_pos += 2 * self.x_dir
        self.y_pos += 4 * self.y_dir

        arcade.draw_rectangle_filled(self.xr_pos, self.yr_pos, self.rect_width, self.rect_height, arcade.color.BLUE)

        if self.x_pos > self.width or self.x_pos < 0:
            self.x_dir *= -1

        if self.y_pos > self.height or self.y_pos < 0:
            self.y_dir *= -1

        self.collide()



    # def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
    #     self.xr_pos = x

    def collide(self):
        if (self.x_pos <= self.xr_pos+(self.rect_width/2) and self.x_pos >= self.xr_pos-(self.rect_width/2)) and (self.y_pos <= self.yr_pos+(self.rect_height/2) and self.y_pos >= self.yr_pos-self.rect_height/2):
            self.y_dir *= -1
            self.x_dir *= -1

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.x_dir = -1
        elif symbol == arcade.key.RIGHT:
            self.x_dir = 1

arcade.window = MyGame(1000, 600, 'blahblah')
arcade.run()
