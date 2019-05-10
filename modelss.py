import arcade.key
from random import randint,random
import time

GRAVITY = -1
MAX_VX = 8
ACCX = 2
JUMP_VY = 15

ORA_RADIUS = 40
PLATFORM_MARGIN = 5

COIN_RADIUS = 32
COIN_Y_OFFSET = 20
COIN_MARGIN = 12
COIN_HIT_MARGIN = 12

BANANA_RADIUS = 36
BANANA_Y_OFFSET = 22
BANANA_MARGIN = 15
BANANA_HIT_MARGIN = 15

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

    def update(self,delta):
        pass

class Ora(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        self.vx = 0
        self.vy = 0
        self.is_jump = False
        self.is_die = False
        self.platform = None

    def jump(self):
        if not self.platform:
            return

        if not self.is_jump:
            self.is_jump = True
            self.vy = JUMP_VY

    def update(self, delta):
        if self.vx < MAX_VX:
            self.vx += ACCX

        self.x += self.vx

        if self.is_jump:
            self.y += self.vy
            self.vy += GRAVITY

            new_platform = self.find_touching_platform()
            if new_platform:
                self.vy = 0
                self.set_platform(new_platform)
        else:
            if (self.platform) and (not self.is_on_platform(self.platform)):
                self.platform = None
                self.is_jump = True
                self.vy = 0

    def bottom_y(self):
        return self.y - (ORA_RADIUS // 2)

    def top_y(self):
        return self.y + (ORA_RADIUS // 2)

    def set_platform(self, platform):
        self.is_jump = False
        self.platform = platform
        self.y = platform.y + (ORA_RADIUS // 2)

    def is_on_platform(self, platform, margin=PLATFORM_MARGIN):
        if not platform.in_top_range(self.x):
            return False

        if abs(platform.y - self.bottom_y()) <= PLATFORM_MARGIN:
            return True

        return False

    def is_falling_on_platform(self, platform):
        if not platform.in_top_range(self.x):
            return False

        if self.bottom_y() - self.vy > platform.y > self.bottom_y():
            return True

        return False

    def find_touching_platform(self):
        platforms = self.world.platforms
        for p in platforms:
            if self.is_falling_on_platform(p):
                return p
        return None

    def die(self, banana_hit=False):
        if self.top_y() < 0 :
            return True
        if banana_hit == True:
            return True

        return False

class Banana:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.effect = False
        self.is_collected = False

    def banana_hit(self,ora):
        return ((abs(self.x - ora.x) < BANANA_HIT_MARGIN) and
                (abs(self.y - ora.y) < BANANA_HIT_MARGIN))

class Coin:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_collected = False
        if random() > 0.975:
            self.effect = True

    def hit(self, dot):
        return ((abs(self.x - dot.x) < COIN_HIT_MARGIN) and
                (abs(self.y - dot.y) < COIN_HIT_MARGIN))

class Platform:
    def __init__(self, world, x, y, width, height):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def in_top_range(self, x):
        return self.x <= x <= self.x + self.width

    def right_most_x(self):
        return self.x + self.width

    def spawn_coins(self):
        chance = randint(40,300)
        coins = []
        x = self.x + COIN_MARGIN
        while x + COIN_MARGIN <= self.right_most_x():
            coins.append(Coin(self.x+chance, self.y + COIN_Y_OFFSET,
                              COIN_RADIUS, COIN_RADIUS))
            x += COIN_MARGIN + COIN_RADIUS + 100
        return coins

    def spawn_banana(self):

        p = randint(0,self.width) + self.x

        bananas = []

        x = self.x + BANANA_MARGIN

        while x + BANANA_MARGIN <= self.right_most_x():
            bananas.append(Banana(p, self.y + BANANA_Y_OFFSET, BANANA_RADIUS + 20, BANANA_RADIUS + 20))
            x += BANANA_MARGIN + BANANA_RADIUS

        return bananas

class World():
    MENU = 0
    GAME = 1
    DEAD = 2

    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.score = 0
        self.ora = Ora(self, 100,100)

        self.state = World.MENU
        self.init_platforms()

        self.ora.set_platform(self.platforms[0])

    def menu(self):
        self.state = World.MENU

    def game(self):
        self.state = World.GAME

    def dead(self):
        self.state = World.DEAD

    def init_platforms(self):
        self.platforms = [
            Platform(self, 0, 100, 300, 70),
            Platform(self, 400, 200, 400, 45),
            Platform(self, 900, 200, 350, 60),
            Platform(self, 1350, 300, 250, 50),
            Platform(self, 1700, 100, 300, 40),
            ]

        self.coins = []
        for p in self.platforms:
            self.coins += p.spawn_coins()

        self.bananas = []
        for i in self.platforms:
            a = randint(1, 10)
            if a < 5:
                self.bananas += i.spawn_banana()

    def update(self, delta):
        self.is_start()
        if self.state == World.MENU:
            self.ora.update(delta)
            self.recycle_platform()
            self.collect_coins()
            self.collect_bananas()
            self.remove_old_coins()

    def is_start(self):
        if self.ora.bottom_y() < 0:
            self.state = World.GAME

    def collect_coins(self):
        for c in self.coins:
            if (not c.is_collected) and (c.hit(self.ora)):
                c.is_collected = True
                self.score += 5

    def collect_bananas(self):
        for i in self.bananas:
            if (not i.is_collected) and (i.banana_hit(self.ora)):
                i.is_collected = True
                if i.effect == False:
                    self.dead()


    def too_far_left_x(self):
        return self.ora.x - self.width

    def remove_old_coins(self):
        far_x = self.too_far_left_x()
        if self.coins[0].x >= far_x:
            return
        self.coins = [c for c in self.coins if c.x >= far_x]

    def recycle_platform(self):
        far_x = self.too_far_left_x()
        for p in self.platforms:
            if p.right_most_x() < far_x:
                last_x = max([pp.right_most_x() for pp in self.platforms])
                p.x = last_x + randint(50, 200)
                p.y = randint(100, 200)
                self.coins += p.spawn_coins()
                a = randint(1, 10)
                if a < 5:
                    self.bananas += p.spawn_banana()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.ora.jump()