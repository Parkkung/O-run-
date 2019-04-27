import arcade
from character import World
import pyglet.gl as gl

# import codecs
# with codecs.open('Orun.py', 'r', encoding='utf-8',
#                  errors='ignore') as fdata:


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class OrunGameWindow(arcade.Window):
    def __init__(self, width, height):

        super().__init__(width, height)

        self.world = World(width,height)
        self.background = None
        self.ora_sprite = ModelSprite('images/O-ra.png', model= self.world.ora)
        # arcade.set_background_color(arcade.color.BABY_BLUE)

        self.coin_texture = arcade.load_texture('images/coin.png')

    # def setup(self):
    #     self.background = arcade.load_texture("images/Background.png")


    def update(self, delta):
        self.world.update(delta)

    def draw_platforms(self, platforms):
        for p in platforms:
            arcade.draw_rectangle_filled(p.x + p.width // 2,
                                         p.y - p.height // 2,
                                         p.width, p.height,
                                         arcade.color.WHITE)

    def draw_coins(self, coins):
        for c in coins:
            if not c.is_collected:
                arcade.draw_texture_rectangle(c.x, c.y, c.width, c.height,
                                              self.coin_texture)

    def on_draw(self):
        arcade.set_viewport(self.world.ora.x - SCREEN_WIDTH // 2,
                            self.world.ora.x + SCREEN_WIDTH // 2,
                            0, SCREEN_HEIGHT)

        arcade.start_render()
        self.draw_platforms(self.world.platforms)
        self.draw_coins(self.world.coins)

        self.ora_sprite.draw()

        arcade.draw_text(str(self.world.score),
                         self.world.ora.x + (SCREEN_WIDTH // 2) - 60,
                         self.height - 30,
                         arcade.color.WHITE, 20)

        self.background = arcade.load_texture("images/Background.png")

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs, scale=0.5)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()

    def update(self,delta):
        self.wolrd.update(delta)


def main():
    window = OrunGameWindow(SCREEN_WIDTH,SCREEN_HEIGHT)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()