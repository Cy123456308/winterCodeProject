import pygame
from settings import *

# 选择框的类
class Option:
    def __init__(self, x, y, width, height, text, action, actionSource, border_radius=15):
        self.rect = pygame.Rect(x - width // 2, y, width, height)  # 选项矩形区域
        self.text = text  # 显示的文本
        self.action = action  # 点击后执行的动作
        self.font = pygame.font.Font(FONT_SONGTI, 30)  # 字体设置
        self.color = (255, 255, 255)  # 默认颜色：白色
        self.hover_color = (200, 200, 200)  # 悬停时的颜色：灰色
        self.border_color = (0, 0, 0)  # 边框颜色：黑色
        self.border_width = 3  # 边框宽度
        self.border_radius = border_radius  # 圆角半径
        self.actionSource = actionSource

    def draw(self, surface):
        # 创建一个表面，用于绘制带有圆角的矩形
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # 如果鼠标悬停，改变按钮背景色
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            button_surface.fill(self.hover_color)  # 悬停时背景色
        else:
            button_surface.fill(self.color)  # 默认背景色

        # 绘制圆角矩形（边框宽度为 self.border_width）
        pygame.draw.rect(button_surface, self.border_color, button_surface.get_rect(), self.border_width, border_radius=self.border_radius)

        # 将圆角矩形表面绘制到主屏幕表面
        surface.blit(button_surface, self.rect.topleft)

        # 绘制文本
        text_surface = self.font.render(self.text, True, self.border_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        # 检查是否点击
        if self.rect.collidepoint(pos):
            self.action(self.actionSource)  # 执行对应的行为
