import pygame as pg
import pygame.font

from file_read_backwards import FileReadBackwards

class FormatText:
    def __init__(self, size, msg, color, x, y):
        self.font = pygame.font.SysFont(None, size)
        self.prep_txt = self.font.render(msg, True, color)
        self.prep_txt_rect = self.prep_txt.get_rect(topleft=(x, y))

    # def read_reverse_txt(self, filename):
    #     with open(filename) as

    def draw(self, prep_txt):
        prep_txt.blit(self.prep_txt, self.prep_txt_rect)


class StartUpScreen:
    def __init__(self, settings, screen, msg='Stuff'):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.background_image = pg.image.load('images/background.bmp')
        self.background_image = pg.transform.scale(self.background_image, (1200, 800))

        self.game_name = FormatText(80, 'Space Invaders', (255, 255, 255), 380, 155)

        self.alien_images = [pg.image.load('images/alien' + str(number) + '0' + '.png') for number in range(3)]
        self.alien01_pts = FormatText(40, '1 pts', (255, 255, 255), 170, 270)
        self.alien02_pts = FormatText(40, '1 pts', (255, 255, 255), 170, 345)
        self.alien03_pts = FormatText(40, '1 pts', (255, 255, 255), 170, 420)

        self.recent_scores = []
        with FileReadBackwards("high_score.txt", encoding="utf-8") as frb:
            for l in frb:
                # print(l)
                self.recent_scores.append(l[-1:])
                if len(self.recent_scores) == 5:
                    break
        # print(self.recent_scores)

        self.scoreboard = FormatText(50, 'Recent High Scores', (255, 255, 255), 800, 230)
        self.score01 = FormatText(40, '01. ' + self.recent_scores[0] + ' points', (255, 255, 255), 900, 300)
        self.score02 = FormatText(40, '02. ' + self.recent_scores[1] + ' points', (255, 255, 255), 900, 350)
        self.score03 = FormatText(40, '03. ' + self.recent_scores[2] + ' points', (255, 255, 255), 900, 400)
        self.score04 = FormatText(40, '04. ' + self.recent_scores[3] + ' points', (255, 255, 255), 900, 450)
        self.score05 = FormatText(40, '05. ' + self.recent_scores[4] + ' points', (255, 255, 255), 900, 500)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.game_name.draw(self.screen)
        self.screen.blit(self.alien_images[0], (100, 250))
        self.screen.blit(self.alien_images[1], (100, 325))
        self.screen.blit(self.alien_images[2], (100, 400))
        self.alien01_pts.draw(self.screen)
        self.alien02_pts.draw(self.screen)
        self.alien03_pts.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.score01.draw(self.screen)
        self.score02.draw(self.screen)
        self.score03.draw(self.screen)
        self.score04.draw(self.screen)
        self.score05.draw(self.screen)

        # self.screen.fill(self.button_color, self.rect)
        # self.screen.blit(self.msg_image, self.msg_image_rect)
