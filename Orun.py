import arcade
from modelss import World
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
        self.banana = arcade.load_texture('images/banana.png')
        self.background = arcade.load_texture("images/Background.png")
        self.current_state = 1

    # def setup(self):
    #     self.background = arcade.load_texture("images/Background.png")


    def update(self, delta):
        if self.current_state ==2:
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

    def draw_bananas(self,bananas):
        for i in bananas:
            if not i.is_collected:
                if i.effect == False:
                    arcade.draw_texture_rectangle(i.x, i.y, i.width, i.height,
                                              self.banana)

    def draw_game(self):
        arcade.start_render()
        arcade.set_viewport(self.world.ora.x - SCREEN_WIDTH // 2,
                            self.world.ora.x + SCREEN_WIDTH // 2,
                            0, SCREEN_HEIGHT)

        # arcade.start_render()
        arcade.draw_texture_rectangle(self.ora_sprite.center_x,SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH + 50, SCREEN_HEIGHT, self.background)
        self.draw_platforms(self.world.platforms)
        self.draw_coins(self.world.coins)

        self.ora_sprite.draw()
        self.draw_bananas(self.world.bananas)

        arcade.draw_text(str(self.world.score),
                         self.world.ora.x + (SCREEN_WIDTH // 2) - 60,
                         self.height - 30,
                         arcade.color.WHITE, 20)


    def draw_menu(self):
        arcade.start_render()
        background = arcade.load_texture("images/Startbackgroud.png")
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,SCREEN_WIDTH,SCREEN_HEIGHT,background)
        arcade.draw_text("Click to start",
                         (SCREEN_WIDTH//2)-150, SCREEN_HEIGHT //2,
                         arcade.color.BLACK, 50)

    def on_draw(self):
        if self.current_state ==1:
            self.draw_menu()
        elif self.current_state == 2 :
            self.draw_game()



# def on_draw(self):


    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_mouse_press(self, x, y, button, modifier):
        if self.current_state == 1:
            self.current_state = 2
        elif self.current_state == 2:
            pass
class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs, scale=0.35)

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
    arcade.run()

if __name__ == '__main__':
    main()