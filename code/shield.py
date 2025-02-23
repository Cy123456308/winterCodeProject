import pygame
from settings import *

class Shield(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        # 基础属性初始化

        self.pos = pygame.math.Vector2(pos)  # 精确浮点位置
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load(SHIELD_PATH).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.screen = pygame.display.get_surface()
        self.group = group
