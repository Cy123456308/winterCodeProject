import pygame

class Bullet(pygame.sprite.Sprite): 
    def __init__(self, x, y, width, height, image_path, speed, direction, group=None):
        super().__init__(group)
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()  # 加载图像
        self.image = pygame.transform.scale(self.image, (width, height))  # 调整图像大小
        self.speed = speed
        self.direction = direction

    def draw(self, surface):
        # 绘制图像
        surface.blit(self.image, self.rect.topleft)

    def update(self, dt):
        self.rect.x += self.speed * self.direction[0] * dt
        self.rect.y += self.speed * self.direction[1] * dt