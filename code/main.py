import time
import pygame, sys
from CollisionManager import CollisionManager
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

def select_screen(self):
    background = pygame.image.load(BACKGROUND_SELECT_PATH)
    self.screen.blit(background, (0, 0))
    
def go_to_help_page(self):
    self.button_help_clicked = True

def go_to_game_page(self):
    self.select()
    
def go_back_start_page(self):
    self.button_back_clicked = True
    
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, COLOR_WIDTH)
        pygame.display.set_caption('小游戏')
        self.clock = pygame.time.Clock()
        self.button_help_clicked = False
        self.button_back_clicked = False
        self.buttons = []
        
    def start(self):
        start_screen(self)

        # 按钮：start 按钮，点击后跳转到帮助页面
        button1 = Button(200, 600, 402, 250, BUTTON_START_PATH, "Go to Game", go_to_game_page, self)
        # 按钮：help 按钮，点击后跳转到游戏页面
        button2 = Button(678, 600, 402, 250, BUTTON_HELP_PATH, "Go to Help", go_to_help_page, self)

        self.buttons.append(button1)
        self.buttons.append(button2)    
        
        for button in self.buttons:
            button.draw(self.screen)
                
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 监控鼠标点击事件
                if event.type == pygame.MOUSEBUTTONDOWN and not self.button_help_clicked:
                    # 获取鼠标当前位置
                    mouse_pos = pygame.mouse.get_pos()
                    button1.is_clicked(mouse_pos, pygame.mouse.get_pressed())
                    button2.is_clicked(mouse_pos, pygame.mouse.get_pressed())
            if self.button_help_clicked:
                self.button_help_clicked = False
                self.buttons = []
                self.help()
            pygame.display.update()
    
    def countDown(self):
        countdown_numbers = [3, 2, 1]
        font = pygame.font.Font(FONT_ALGER_PATH, 200)
        for num in countdown_numbers:
            background = pygame.image.load(BACKGROUND_BEGIN_PATH)
            self.screen.blit(background, (0, 0))        # 渲染倒计时数字
            text = font.render(str(num), True, (0,0,0))
            self.screen.blit(text, (540, 350))
            pygame.display.flip()
            time.sleep(1)  # 等待 1 秒钟
        # 倒计时结束，跳转到另一个页面
        self.run()
    
    def select(self):
        select_screen(self)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 监控鼠标点击事件
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # 检测 Enter 键
                        self.level = Level(1)
                        self.countDown()
            pygame.display.update()
            
    def help(self): # 帮助界面
        help_screen(self)
        # 按钮：返回按钮，在帮助界面点击后，跳转回游戏初始界面
        button3 = Button(439, 600, 402, 250, BUTTON_HELP_PATH, "Go back to Start", go_back_start_page, self)
        self.buttons.append(button3)
        for button in self.buttons:
            button.draw(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 监控鼠标点击事件
                if event.type == pygame.MOUSEBUTTONDOWN and not self.button_help_clicked:   
                    # 获取鼠标当前位置
                    mouse_pos = pygame.mouse.get_pos()
                    button3.is_clicked(mouse_pos, pygame.mouse.get_pressed())
            if self.button_back_clicked:
                self.button_back_clicked = False
                self.buttons = []
                self.start()
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
