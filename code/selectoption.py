import pygame
from settings import *

# 选择框的类
class Option:
    def __init__(self, x, y, width, height, text, action, actionSource):
        self.rect = pygame.Rect(x - width // 2, y, width, height)  # 选项矩形区域
        self.text = text  # 显示的文本
        self.action = action  # 点击后执行的动作
        self.font = pygame.font.Font(FONT_SONGTI, 30)  # 字体设置
        self.color = (255, 255, 255)  # 默认颜色：白色
        self.hover_color = (200, 200, 200)  # 悬停时的颜色：灰色
        self.border_color = (0, 0, 0)  # 边框颜色：黑色
        self.border_width = 3  # 边框宽度
        self.actionSource = actionSource

    def draw(self, surface):
        # 创建一个表面，用于绘制按钮
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
    
        # 如果鼠标悬停，改变按钮背景色
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            button_surface.fill(self.hover_color)  # 悬停时背景色
        else:
            button_surface.fill(self.color)  # 默认背景色

        # 绘制方形矩形边框（不使用圆角）
        pygame.draw.rect(button_surface, self.border_color, button_surface.get_rect(), self.border_width)

        # 将带有颜色和边框的按钮绘制到主屏幕表面
        surface.blit(button_surface, self.rect.topleft)

        # 绘制文本
        text_surface = self.font.render(self.text, True, self.border_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        # 检查是否点击
        if self.rect.collidepoint(pos):
            self.action(self.actionSource)  # 执行对应的行为
