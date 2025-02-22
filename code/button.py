import pygame

class Button:
    def __init__(self, x, y, width, height, image_path, text, action, actionSource):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path).convert_alpha()  # 加载图像
        self.image = pygame.transform.scale(self.image, (width, height))  # 调整图像大小
        self.action = action  # 按钮点击后执行的动作
        self.text = text  # 按钮上的文字
        self.actionSource = actionSource

    def draw(self, surface):
        # 绘制图像
        surface.blit(self.image, self.rect.topleft)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def is_clicked(self, pos, button_state):
        if self.rect.collidepoint(pos) and button_state[0]:  # 检查是否点击
            self.action(self.actionSource)  # 执行按钮的动作
