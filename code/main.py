import random
import time
import pygame, sys
from CollisionManager import CollisionManager
import settings
from settings import *
from player import Player
from level import Level
from button import Button
from title import Title
from rolechoose import RoleChoose
from selectoption import Option

def start_screen(self):
    background = pygame.image.load(BACKGROUND_BEGIN_PATH)
    self.screen.blit(background, (0, 0))
    pygame.mixer.music.load(AUDIO_START_PATH)  # 替换为你的音乐文件路径
    pygame.mixer.music.play()  # 播放音乐
    title = Title(300, 0, 906, 250, TITLE_START_3)
    title.draw(self.screen)
    #titleUp = Title(625, 75, 452, 99, TITLE_START_1)
    #titleDown = Title(551, 174, 600, 113, TITLE_START_2)
    #titleUp.draw(self.screen)
    #titleDown.draw(self.screen)

def help_screen(self):
    background = pygame.image.load(BACKGROUND_HELP_PATH)
    self.screen.blit(background, (0, 0))
    pygame.mixer.music.load(AUDIO_HELP_PATH)  # 替换为你的音乐文件路径
    pygame.mixer.music.play()  # 播放音乐

def select_screen(self):
    background = pygame.image.load(BACKGROUND_SELECT_PATH)
    self.screen.blit(background, (0, 0))
    pygame.mixer.music.load(AUDIO_SELECT_PATH)  # 替换为你的音乐文件路径
    pygame.mixer.music.play()  # 播放音乐

def end_screen(self):
    ranSum = random.randint(1, 6)
    if ranSum % 6 == 1:
        background = pygame.image.load(BACKGROUND_SUCCESS_PATH)
    elif ranSum % 6 == 2:
        background = pygame.image.load(BACKGROUND_END_PATH_1)
    elif ranSum % 6 == 3:
        background = pygame.image.load(BACKGROUND_END_PATH_2)
    elif ranSum % 6 == 4:
        background = pygame.image.load(BACKGROUND_END_PATH_3)
    elif ranSum % 6 == 5:
        background = pygame.image.load(BACKGROUND_END_PATH_4)
    elif ranSum % 6 == 0:
        background = pygame.image.load(BACKGROUND_END_PATH_5)
    self.screen.blit(background, (0, 0))
    pygame.mixer.music.load(AUDIO_FAIL_PATH)  # 替换为你的音乐文件路径
    pygame.mixer.music.play()  # 播放音乐
    
def pause_screen(self):
    self.pause()
            
def go_to_help_page(self):
    self.button_help_clicked = True

def go_to_game_page(self):
    self.select()
    
def go_back_start_page(self):
    self.button_back_clicked = True

def go_to_countdown_1(self):
    self.roleNum = 1
    self.button_select_clicked = True

def go_to_countdown_2(self):
    self.roleNum = 2
    self.button_select_clicked = True

def go_to_countdown_3(self):
    self.roleNum = 3
    self.button_select_clicked = True

def go_to_countdown_4(self):
    self.roleNum = 4
    self.button_select_clicked = True

def go_to_countdown_5(self):
    self.roleNum = 5
    self.button_select_clicked = True

def go_to_countdown_6(self):
    self.roleNum = 6
    self.button_select_clicked = True
class Game:
    def __init__(self):
        settings.ending = False
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, COLOR_WIDTH)
        pygame.display.set_caption('小游戏')
        self.clock = pygame.time.Clock()
        self.button_help_clicked = False
        self.button_back_clicked = False
        self.buttons = []
        self.paused = False  # 新增暂停状态标志

        # 加载自定义鼠标
        cursor_image = pygame.image.load(MOUSE_PATH_3).convert_alpha()  # 支持透明通道
        hotspot = (cursor_image.get_width() // 4, cursor_image.get_height() // 4)
        custom_cursor = pygame.cursors.Cursor(hotspot, cursor_image)
        pygame.mouse.set_cursor(custom_cursor)
        
    def start(self):
        start_screen(self)

        # 按钮：start 按钮，点击后跳转到帮助页面
        button1 = Button(200, 600, 402, 250, BUTTON_START_PATH, "Go to Game", go_to_game_page, self)
        # 按钮：help 按钮，点击后跳转到游戏页面
        button2 = Button(678, 600, 402, 250, BUTTON_HELP_PATH, "Go to Help", go_to_help_page, self)

        self.buttons.append(button1)
        self.buttons.append(button2)    

        while True:
            # 获取鼠标当前位置
            mouse_pos = pygame.mouse.get_pos()

            # 更新所有按钮的悬停状态
            for button in self.buttons:
                button.update_hover_state(mouse_pos)

            # 绘制所有按钮
            for button in self.buttons:
                button.draw(self.screen)

            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 监控鼠标点击事件
                if event.type == pygame.MOUSEBUTTONDOWN and not self.button_help_clicked:
                    # 检测按钮点击
                    button1.is_clicked(mouse_pos, pygame.mouse.get_pressed())
                    button2.is_clicked(mouse_pos, pygame.mouse.get_pressed())

            # 如果点击了帮助按钮，跳转到帮助页面
            if self.button_help_clicked:
                self.button_help_clicked = False
                self.buttons = []
                self.help()

            # 更新显示
            pygame.display.update()
    
    def countDown(self):
        countdown_numbers = [3, 2, 1]
        font = pygame.font.Font(FONT_ALGER_PATH, 200)

    # 渲染倒计时 3, 2, 1
        for num in countdown_numbers:
            background = pygame.image.load(BACKGROUND_BEGIN_PATH)
            self.screen.blit(background, (0, 0))  # 渲染背景
            text = font.render(str(num), True, (0, 0, 0))  # 渲染数字
            self.screen.blit(text, (540, 350))  # 显示数字
            pygame.display.flip()
            time.sleep(1)  # 等待 1 秒钟

    # 渲染 "Go!" 字符
        background = pygame.image.load(BACKGROUND_BEGIN_PATH)
        self.screen.blit(background, (0, 0))  # 渲染背景
        text = font.render("Go!", True, (0, 0, 0))  # 渲染 "Go!" 文本
        self.screen.blit(text, (440, 350))  # 显示 "Go!"
        pygame.display.flip()
        time.sleep(1)  # 等待 1 秒钟

    # 倒计时结束，跳转到另一个页面
        self.run()
    
    def select(self):
        select_screen(self)
        text = "请选择你的角色："
        self.font = pygame.font.Font(FONT_FANGZHENGXIETI, 64)  # 字体设置
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(640,150))
        self.screen.blit(text_surface, text_rect)
        
        self.buttons = [
            Option(640, 250, 572, 50, SHIRONO_LINES, go_to_countdown_1, self),
            Option(640, 350, 572, 50, ALICE_LINES, go_to_countdown_2, self),
            Option(640, 450, 572, 50, MOMOI_LINES, go_to_countdown_3, self),
            Option(640, 550, 572, 50, MIDORI_LINES, go_to_countdown_4, self),
            Option(640, 650, 572, 50, YUZU_LINES, go_to_countdown_5, self),
            Option(640, 750, 572, 50, YUKARI_LINES, go_to_countdown_6, self),
            Option(640, 750, 572, 50, YUKARI_LINES, go_to_countdown_6, self),
            Option(640, 850, 572, 50, "返回初始界面", go_back_start_page, self),
        ]
    
        self.button_select_clicked = False
        self.roleNum = 0

        while True:
            for btn in self.buttons:
                btn.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.button_select_clicked:
                    mouse_pos = pygame.mouse.get_pos()
                    for btn in self.buttons:
                        btn.is_clicked(mouse_pos)

            if self.button_select_clicked:
                self.button_select_clicked = False
                self.buttons = []
                self.level = Level(self.roleNum)
                self.countDown()
                
            elif self.button_back_clicked:
                self.button_back_clicked = False
                self.buttons = []
                self.start()
                
            pygame.display.update()
            
    def help(self): # 帮助界面
        help_screen(self)
        # 按钮：返回按钮，在帮助界面点击后，跳转回游戏初始界面
        button3 = Button(800, 600, 234, 250, BUTTON_BACK_PATH, "Go back to Start", go_back_start_page, self)
        self.buttons.append(button3)
        
        # 添加文字说明
        font = pygame.font.Font(FONT_FANGZHENGXIETI, 36)  # 使用默认字体，字号36
        text_lines = [
            "本游戏是基于蔚蓝档案素材的射击小游戏",
            "以下是游玩提示：",
            "点击“开始冒险”进入角色选择界面",
            "通过上下左右键移动，空格键射击",
            "不同角色有不同的特性，如血量，射速等",
            "选择角色后开始游戏",
            "注意躲避敌人射出的子弹，观察换弹时机",
            "同时注意不要碰到游荡的机器人，否则带来大量伤害",
            "利用掩体作为掩护，保护自己",
            "如果撑不住了，可以摁esc暂停游戏，休息一下；再摁esc可继续",
            "分数将上传网络",
            "祝您玩得愉快！"
        ]
        y_position = 90  # 文字起始Y坐标
        for line in text_lines:
            text_surface = font.render(line, True, (0, 0, 0))  # 白色文字
            text_rect = text_surface.get_rect(center=(self.screen.get_width()//2, y_position))
            self.screen.blit(text_surface, text_rect)
            y_position += 40  # 行间距

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update_hover_state(mouse_pos)
            for button in self.buttons:
                button.draw(self.screen)
                
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
        pygame.mixer.music.load(AUDIO_FIGHT_PATH)  # 替换为你的音乐文件路径
        pygame.mixer.music.play()  # 播放音乐
        while True:
            if settings.ending:
                self.end()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.paused = not self.paused
            dt = self.clock.tick() / 1000
            self.level.run(dt, self.paused)
            if self.paused:
                self.pause()  # 渲染暂停界面
            pygame.display.update()

    def pause(self):
        self.screen.fill((0, 0, 0))
        text = "游戏暂停，按“esc”继续"
        self.font = pygame.font.Font(FONT_SONGTI, 64)  # 字体设置
        text_surface = self.font.render(text, True, (200, 200, 200))
        text_rect = text_surface.get_rect(center=(640,450))
        self.screen.blit(text_surface, text_rect)

    def end(self):
        end_screen(self)
        text = f"游戏结束！本次你的得分为: {presentMark}, 之前你的最高分为: {hightstMark}"
        self.font = pygame.font.Font(FONT_FANGZHENGXIETI, 48)  # 字体设置
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(640,200))
        self.screen.blit(text_surface, text_rect)
        if presentMark >= hightstMark:
            text = f"恭喜你创造了新纪录！"
            self.font = pygame.font.Font(FONT_SONGTI, 48)  # 字体设置
            text_surface = self.font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(640,360))
            self.screen.blit(text_surface, text_rect)
        settings.hightstMark = max(settings.hightstMark, settings.presentMark)
        settings.presentMark = 0
        self.buttons = [
            Option(320, 650, 120, 50, "退出游戏", self.returnStart, self),
            Option(960, 650, 120, 50, "返回开头", self.exitGame, self),
        ]
        while True:
            for btn in self.buttons:
                btn.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.button_select_clicked:
                    mouse_pos = pygame.mouse.get_pos()
                    for btn in self.buttons:
                        btn.is_clicked(mouse_pos)

            if self.button_select_clicked:
                self.button_select_clicked = False
                self.buttons = []
                self.level = Level(self.roleNum)
                self.countDown()

            pygame.display.update()
    
    def returnStart(self):
        game = Game()
        game.start()
    
    def exitGame(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.start()
