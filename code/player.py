import pygame
from settings import *
from bullet import Bullet
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, bullet_group):
        super().__init__(group)

        self.image = pygame.image.load(SHIRONO_PATH).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.screen = pygame.display.get_surface()

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 400
        self.health = 400  # 血量属性

        self.group = group
        
        self.player_bullet_group = bullet_group
        self.can_shoot = True
        self.reloading = False  # 新增：是否正在装弹
        self.reload_start_time = 0  # 新增：装弹开始时间
        self.bullet_wait_time = 0
        self.bullets = pygame.sprite.Group()
        self.bullet_waiting = False
        self.bullet_counts = 30
        self.shootSpeed = 0.2

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.can_shoot and not self.reloading:  # 只有在可以射击且不在装弹时才发射
            bullet = Bullet(self.rect.centerx, self.rect.centery - self.rect.height / 2, 10, 10, BULLET_PATH_1, 1000, (0, -1), group=(self.group, self.player_bullet_group))
            self.bullets.add(bullet)
            self.can_shoot = False
            self.bullet_waiting = True
            self.bullet_wait_time = time.time()
            self.bullet_counts -= 1
            if self.bullet_counts == 0:
                self.can_shoot = False
                self.reloading = True  # 开始装弹
                self.reload_start_time = time.time() # 记录装弹开始时间
            
    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def bullet_wait(self, shootTime):
        if self.bullet_waiting:
            current_time = time.time()
            if current_time - self.bullet_wait_time >= shootTime: 
                self.can_shoot = True
                self.bullet_waiting = False
               
    def reload(self):  # 新增：装弹方法
        if self.reloading:
            current_time = time.time()
            if current_time - self.reload_start_time >= 1: # 1秒装弹时间
                self.reloading = False
                self.can_shoot = True
                self.bullet_counts = 30
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def update(self, dt):
        self.input()
        self.move(dt)
        self.bullet_wait(self.shootSpeed)
        self.reload()  # 调用装弹方法
       

