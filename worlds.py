import arcade
from character import Ora, World

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



class OrunGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.world = World(width,height)

        arcade.set_background_color(arcade.color.BABY_BLUE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.world.score),
                         self.width - 30, self.height - 30,
                         arcade.color.YELLOW_ORANGE, 20)

    def update(self, delta):
        self.world.update(delta)

def main():
    OrunGameWindow(SCREEN_WIDTH,SCREEN_HEIGHT)
    arcade.run

if __name__ == '__main__':
    window = OrunGameWindow(SCREEN_WIDTH,SCREEN_HEIGHT)
    arcade.run()