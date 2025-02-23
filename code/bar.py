import pygame
class Bar(pygame.sprite.Sprite):
    def __init__(self, host, offset_y=-30, width=60, height=8):
        super().__init__()
        self.host = host  # 宿主（敌人对象）
        self.offset_y = offset_y  # 血条相对宿主的位置偏移
        self.width = width
        self.height = height
        
        # 创建血条 Surface
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
        # 初始位置绑定
        self.update_position()

    def update_position(self):
        """根据宿主位置更新血条位置"""
        if self.host.alive():
            self.rect.center = (
                self.host.rect.centerx,
                self.host.rect.top + self.offset_y
            )
        else:
            self.kill()  # 宿主死亡时自动销毁

    def update(self, *args, **kwargs):
        """动态更新血条外观"""
        self.image.fill((0, 0, 0, 0))  # 透明背景
        
        if self.host.health <= 0:
            self.kill()
            return
        
        # 计算血量比例
        ratio = self.host.health / self.host.max_health
        
        # 绘制红色背景条
        pygame.draw.rect(self.image, (200, 0, 0), (0, 0, self.width, self.height), border_radius=3)
        # 绘制绿色当前血量
        pygame.draw.rect(self.image, (0, 200, 0), (0, 0, self.width * ratio, self.height), border_radius=3)
        
        # 更新位置
        self.update_position()