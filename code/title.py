import pygame

class Title:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()  # 加载图像
        self.image = pygame.transform.scale(self.image, (width, height))  # 调整图像大小

    def draw(self, surface):
        # 绘制图像
        surface.blit(self.image, self.rect.topleft)

