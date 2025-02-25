import pygame
class Button:
    def __init__(self, x, y, width, height, image_path, text, action, actionSource):
        self.rect = pygame.Rect(x, y, width, height)
        self.base_image = pygame.image.load(image_path).convert_alpha()  # 原图
        self.base_image = pygame.transform.scale(self.base_image, (width, height))
        self.hover_image = self.create_hover_effect()  # 悬停特效图
        self.current_image = self.base_image  # 当前显示的图像
        self.action = action
        self.text = text
        self.actionSource = actionSource
        self.hovered = False  # 悬停状态标记

    def create_hover_effect(self):
        """创建悬停特效：增加亮度和添加光边（可根据需要自行调整）"""
        # 复制原图并提高亮度
        hover_img = self.base_image.copy()
        hover_img.fill((200, 200, 200, 0), special_flags=pygame.BLEND_RGB_ADD)
        
        '''
        # 添加黄色光边
        edge_width = 4
        edge_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(edge_surface, (255, 235, 50, 80), 
                        (0, 0, *self.rect.size), edge_width)
        hover_img.blit(edge_surface, (0, 0))'''
        
        return hover_img

    def update_hover_state(self, mouse_pos):
        """更新悬停状态"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.current_image = self.hover_image if self.hovered else self.base_image

    def draw(self, surface):
        """动态绘制不同状态的按钮"""
        surface.blit(self.current_image, self.rect.topleft)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def is_clicked(self, pos, button_state):
        if self.rect.collidepoint(pos) and button_state[0]:  # 检查是否点击
            self.action(self.actionSource)  # 执行按钮的动作