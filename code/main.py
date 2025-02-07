import pygame, sys
from settings import *
from player import Player
from level import Level
from button import Button
from title import Title

def start_screen(self):
    background = pygame.image.load(BACKGROUND_BEGIN_PATH)
    self.screen.blit(background, (0, 0))
    titleUp = Title(625, 75, 452, 99, TITLE_START_1)
    titleDown = Title(551, 174, 600, 113, TITLE_START_2)
    titleUp.draw(self.screen)
    titleDown.draw(self.screen)


def help_screen(self):
    background = pygame.image.load(BACKGROUND_HELP_PATH)
    self.screen.blit(background, (0, 0))


def go_to_help_page(self):
    help_screen(self)

def go_to_game_page(self):
    self.run()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, COLOR_WIDTH)
        pygame.display.set_caption('小游戏')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def start(self):
        start_screen(self)

        # 按钮：start 按钮，点击后跳转到帮助页面
        button1 = Button(200, 600, 402, 250, BUTTON_START_PATH, "Go to Help", go_to_game_page, self)

        # 按钮：help 按钮，点击后跳转到游戏页面
        button2 = Button(678, 600, 402, 250, BUTTON_HELP_PATH, "Go to Game", go_to_help_page, self)

        button1.draw(self.screen)
        button2.draw(self.screen)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 监控鼠标点击事件
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # 获取鼠标当前位置
                    mouse_pos = pygame.mouse.get_pos()
                    button1.is_clicked(mouse_pos, pygame.mouse.get_pressed())
                    button2.is_clicked(mouse_pos, pygame.mouse.get_pressed())

            pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.start()
