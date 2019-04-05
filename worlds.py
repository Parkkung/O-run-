import arcade
from character import Ora, World
# import codecs
# with codecs.open('worlds.py', 'r', encoding='utf-8',
#                  errors='ignore') as fdata:


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



class OrunGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.world = World(width,height)
        self.background = None
        # arcade.set_background_color(arcade.color.BABY_BLUE)

    def setup(self):
        self.background = arcade.load_texture("images/Background.png")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2,
                                      SCREEN_WIDTH,SCREEN_HEIGHT, self.background)

        arcade.draw_text(str(self.world.score),
                         self.width - 30, self.height - 30,
                         arcade.color.GREEN, 20)

    def update(self, delta):
        self.world.update(delta)

def main():
    window = OrunGameWindow(SCREEN_WIDTH,SCREEN_HEIGHT)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()