import pygame
from settings import *

class RoleChoose:
    def __init__(self, x, y, image_path, text, dialog_text, action, actionSource):
        self.image = pygame.image.load(image_path).convert_alpha()  # 加载图像
        self.pos = (x, y)
        self.rect = self.image.get_rect(center = self.pos)        
        self.action = action  # 按钮点击后执行的动作
        self.text = text  # 按钮上的文字
        self.actionSource = actionSource

        # 对话框相关属性
        self.dialog_active = False  # 是否正在显示对话框
        self.dialog_text = dialog_text  # 对话框中的提示文字
        self.dialog_rect = None
        self.confirm_button_rect = None

    def draw(self, surface):
        # 绘制按钮图像
        surface.blit(self.image, self.rect.topleft)
        # 如果需要，也可以在按钮上绘制文字（示例中未作处理）

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def is_clicked(self, pos, button_state):
        # 如果按钮区域内鼠标左键被按下，并且未处于对话框状态，则显示对话框
        if self.rect.collidepoint(pos) and button_state[0] and not self.dialog_active:
            self.dialog_active = True

    def draw_dialog(self, surface):
        """绘制提示对话框"""
        if not self.dialog_active:
            return

        # 设置对话框尺寸，位于屏幕中心
        dialog_width, dialog_height = 300, 150
        screen_rect = surface.get_rect()
        self.dialog_rect = pygame.Rect(
            screen_rect.centerx - dialog_width // 2,
            screen_rect.centery - dialog_height // 2,
            dialog_width, dialog_height
        )

        # 绘制对话框背景与边框
        pygame.draw.rect(surface, (200, 200, 200), self.dialog_rect)
        pygame.draw.rect(surface, (0, 0, 0), self.dialog_rect, 2)

        # 使用系统默认字体绘制提示文字
        font = pygame.font.Font(resource_path(FONT_SONGTI), 24)
        text_surface = font.render(self.dialog_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.dialog_rect.centerx, self.dialog_rect.centery - 20))
        surface.blit(text_surface, text_rect)

        # 绘制确认按钮，按钮位于对话框底部
        button_width, button_height = 80, 30
        self.confirm_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.confirm_button_rect.center = (self.dialog_rect.centerx, self.dialog_rect.bottom - 30)
        pygame.draw.rect(surface, (100, 100, 100), self.confirm_button_rect)
        pygame.draw.rect(surface, (0, 0, 0), self.confirm_button_rect, 2)

        confirm_text = font.render("确认", True, (255, 255, 255))
        confirm_rect = confirm_text.get_rect(center=self.confirm_button_rect.center)
        surface.blit(confirm_text, confirm_rect)

    def handle_dialog_event(self, event):
        """在对话框显示期间处理鼠标事件，确认后执行动作"""
        if not self.dialog_active:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # 如果点击确认按钮区域，则关闭对话框并执行动作
            if self.confirm_button_rect and self.confirm_button_rect.collidepoint(pos):
                self.dialog_active = False
                self.action(self.actionSource)
