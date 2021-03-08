import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from pygame.sprite import Group
# from bullet import BulletFromAlien
from random import randint

class Ufos:
    def __init__(self, ship_height, game, barriers):
        self.settings = game.settings
        self.screen = game.screen
        self.ship_height = ship_height
        self.game = game
        self.barriers = barriers
        self.ufo_group = Group()
        self.ship_group = Group()
        self.create_fleet()
        self.bullet_group_that_kill_ship = Group()
        self.last_bullet_shot = pg.time.get_ticks()
        self.ship = None

    def create_fleet(self):
        settings, screen = self.settings, self.screen
        ufo = Ufo(parent=self, game=self.game)
        ufo_width = ufo.rect.width
        ufo_height = ufo.rect.height
        ufos_per_row = self.ufos_per_row(settings=settings, ufo_width=ufo_width)
        # rows_per_screen = self.rows_per_screen(settings=settings, ufo_height=ufo_height)


        for x in range(ufos_per_row):
            ufo = Ufo(parent=self, game=self.game, number=1, x=ufo_width * (3 + 1.5 * x))
            self.ufo_group.add(ufo)

    def ufos_per_row(self, settings, ufo_width):
        space_x = settings.screen_width - 2 * ufo_width
        return int(space_x / (2 * ufo_width))

    # def rows_per_screen(self, settings, ufo_height): return 6

    # def add_bullet(self, game, x, y):
    #     self.bullet_group_that_kill_ship.add(BulletFromUfo(game=game, x=x, y=y))

    def add(self, ufo): self.ufo_group.add(ufo)

    def add_ship(self, ship):
        self.ship = ship
        self.ship_group.add(self.ship)

    def empty(self): self.ufo_group.empty()

    def bullet_group(self): return self.bullet_group_that_kill_ship

    def group(self): return self.ufo_group

    def remove(self, ufo): self.ufo_group.remove(ufo)

    # def change_direction(self):
    #     for ufo in self.ufo_group:
    #         ufo.rect.y += self.settings.fleet_drop_speed
    #     self.settings.fleet_direction *= -1

    # def check_edges(self):
    #     for ufo in self.ufo_group.sprites():
    #         if ufo.check_edges():
    #             return True
    #     return False

    def check_ufos_bottom(self):
        r = self.screen.get_rect()
        for ufo in self.ufo_group.sprites():
            if ufo.rect.bottom > r.bottom:
                return True
        return False

    # def one_ufo_shoots_if_time(self):
    #     now = pg.time.get_ticks()
    #     if now > self.last_bullet_shot + self.settings.ufo_bullets_every * 1000:
    #         li = self.ufo_group.sprites()
    #         length = len(li)
    #         shooter = li[randint(0, length - 1)]
    #         self.add_bullet(game=self.game, x=shooter.x + 34, y=shooter.y)
    #         self.last_bullet_shot = now

    def update(self):
        self.ufo_group.update()

        bullet_bullet_collisions = pg.sprite.groupcollide(self.bullet_group_that_kill_ship,
                                                          self.ship.bullet_group(),
                                                          True, True)
        if bullet_bullet_collisions:
            for bullet in bullet_bullet_collisions:
                bullet.killed()

        self.bullet_group_that_kill_ship.update()
        bullet_ship_collisions = pg.sprite.groupcollide(self.bullet_group_that_kill_ship,
                                                        self.ship.group(), True, False)
        if bullet_ship_collisions:
            print('ship was killed')
            self.ship.killed()

        bullet_barrier_collisions = pg.sprite.groupcollide(self.barriers.group(),
                                                           self.bullet_group_that_kill_ship,
                                                           False, True)
        # TODO: you MUST change True, True to False, True on the previous line if you only damage the barrier block

        if bullet_barrier_collisions:
            for barrier_block in bullet_barrier_collisions:
                barrier_block.damaged()

        for bullet in self.bullet_group_that_kill_ship.copy():
            if bullet.rect.top >= self.screen.get_rect().height:
                self.bullet_group_that_kill_ship.remove(bullet)

        # self.one_ufo_shoots_if_time()
        # if self.check_edges():
        #     self.change_direction()
        if self.check_ufos_bottom() or pg.sprite.spritecollideany(self.game.ship, self.ufo_group):
            self.game.reset()
            return
        for ufo in self.ufo_group.copy():
            ufo.update()
            if ufo.rect.bottom >= self.screen.get_rect().height or ufo.reallydead:
                self.ufo_group.remove(ufo)

    def draw(self):
        for ufo in self.ufo_group:
            ufo.draw()
        for bullet in self.bullet_group_that_kill_ship:
            bullet.draw()


class Ufo(Sprite):   # INHERITS from SPRITE
    images = [[pg.image.load('images/ufo' + str(number) + str(i) + '.png') for i in range(2)] for number in range(3)]
    images_boom = [pg.image.load('images/alien_boom' + str(i) + '.png') for i in range(4)]
    timers = []

    for i in range(3):
        timers.append(Timer(frames=images[0]))
    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    def __init__(self, game, parent, number=0, x=0, y=0, speed=0):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        self.parent = parent
        self.number = number
        self.update_requests = 0
        self.dead, self.reallydead, self.timer_switched = False, False, False

        self.timer = Ufo.timers[number]
        self.rect = self.timer.imagerect().get_rect()
        self.rect.x = self.x = x
        self.rect.y = self.y = y
        self.x = float(self.rect.x)
        self.speed = speed

    # def check_edges(self):
    #     r, rscreen = self.rect, self.screen.get_rect()
    #     return r.right >= rscreen.right or r.left <= 0

    def killed(self):
        if not self.dead and not self.reallydead: self.dead = True
        if self.dead and not self.timer_switched:
            self.timer = Timer(frames=Ufo.images_boom, wait=400, looponce=True)
            self.timer_switched = True
            # self.game.stats.score += self.settings.alien_points * len(self.parent.alien_group)
            self.game.stats.score += self.settings.ufo_points
            # print('self.parent.alien_group', self.game.stats.score)
            # print('self.parent.alien_group', self.settings.alien_points)
            # print('self.parent.alien_group', self.parent.alien_group)
            self.game.sb.check_high_score(self.game.stats.score)
            self.game.sb.prep_score()

    def update(self):
        if self.dead and self.timer_switched:
            if self.timer.frame_index() == len(Ufo.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
                self.parent.remove(self)
                self.timer.reset()
        delta = 1 * self.settings.fleet_direction
        self.rect.x += delta
        self.x = self.rect.x

    def draw(self):
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
