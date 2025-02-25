import pygame
from settings import *
from bullet import Bullet
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, bullet_group, penetrate_bullets_group, role):
        super().__init__(group)

        self.direction = pygame.math.Vector2()
        self.canEnhance = True
        self.enhanceTime = 5
        self.enhanceStart = 0

        if role == 1:
            self.image = pygame.image.load(SHIRONO_PATH).convert_alpha()
            self.speed = 400
            self.maxHealth = 400  
            self.health = self.maxHealth
            self.ATK = 15 
            self.bullet_counts = 40
            self.shootSpeed = 0.05
            self.penetrate = False
            self.canMultipleBullet = False
            self.canEnhance = False

        elif role == 2:
            self.image = pygame.image.load(ALICE_PATH).convert_alpha()
            self.speed = 400
            self.maxHealth = 320  
            self.health = self.maxHealth
            self.ATK = 20 
            self.bullet_counts = 5
            self.shootSpeed = 0.3
            self.penetrate = True
            self.canMultipleBullet = False
            self.canEnhance = False

        elif role == 3:
            self.image = pygame.image.load(MOMOI_PATH).convert_alpha()
            self.speed = 400
            self.maxHealth = 240  
            self.health = self.maxHealth
            self.ATK = 12 
            self.bullet_counts = 30
            self.shootSpeed = 0.1
            self.canMultipleBullet = True
            self.penetrate = False
            self.canEnhance = False

        elif role == 4:
            self.image = pygame.image.load(MIDORI_PATH).convert_alpha()
            self.speed = 400
            self.maxHealth = 240  
            self.health = self.maxHealth
            self.ATK = 27
            self.bullet_counts = 20
            self.shootSpeed = 0.05
            self.penetrate = False
            self.canMultipleBullet = False
            self.canEnhance = False            
            
        elif role == 5:
            self.image = pygame.image.load(YUZU_PATH).convert_alpha()
            self.speed = 500
            self.maxHealth = 200  
            self.health = self.maxHealth
            self.ATK = 20 
            self.bullet_counts = 5
            self.shootSpeed = 0.5
            self.penetrate = False
            self.canMultipleBullet = False
            
        elif role == 6:
            self.image = pygame.image.load(YUKARI_PATH).convert_alpha()
            self.speed = 300
            self.maxHealth = 3000
            self.health = self.maxHealth
            self.ATK = 5 
            self.bullet_counts = 30
            self.shootSpeed = 0.05
            self.penetrate = False
            self.canMultipleBullet = False
            self.canEnhance = False

        self.group = group
        self.penetrate_bullets_group = penetrate_bullets_group
        self.rect = self.image.get_rect(center = pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.screen = pygame.display.get_surface()
        
        self.player_bullet_group = bullet_group
        self.can_shoot = True
        self.reloading = False  # 新增：是否正在装弹
        self.reload_start_time = 0  # 新增：装弹开始时间
        self.bullet_wait_time = 0
        self.bullets = pygame.sprite.Group()
        self.bullet_waiting = False


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
            if not self.penetrate:
                if not self.canMultipleBullet:
                    bullet = Bullet(self.rect.centerx, self.rect.centery - self.rect.height / 2, 12, 28, BULLET_PATH_1, 1000, (0, -1), self.ATK, group=[self.group, self.player_bullet_group])
                    self.bullets.add(bullet)
                else:
                    bullet = Bullet(self.rect.centerx, self.rect.centery - self.rect.height / 2, 12, 28, BULLET_PATH_1, 400, (0, -1), self.ATK, group=[self.group, self.player_bullet_group])
                    self.bullets.add(bullet)
                    bullet = Bullet(self.rect.centerx - 15, self.rect.centery - self.rect.height / 2, 12, 28, BULLET_PATH_1, 400, (-1, -1), self.ATK, group=[self.group, self.player_bullet_group])
                    self.bullets.add(bullet)
                    bullet = Bullet(self.rect.centerx + 15, self.rect.centery - self.rect.height / 2, 12, 28, BULLET_PATH_1, 400, (1, -1), self.ATK, group=[self.group, self.player_bullet_group])
                    self.bullets.add(bullet)
                    bullet = Bullet(self.rect.centerx + 15, self.rect.centery - self.rect.height / 2, 12, 28, BULLET_PATH_1, 400, (2, -1), self.ATK, group=[self.group, self.player_bullet_group])
                    self.bullets.add(bullet)
                    bullet = Bullet(self.rect.centerx + 15, self.rect.centery - self.rect.height / 2, 12, 28, BULLET_PATH_1, 400, (-2, -1), self.ATK, group=[self.group, self.player_bullet_group])
                    self.bullets.add(bullet)
            else:
                bullet = Bullet(self.rect.centerx, self.rect.centery - self.rect.height / 2, 64, 182, BULLET_PATH_ALICE, 1000, (0, -1), self.ATK, group=[self.group, self.penetrate_bullets_group])
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

    def draw_health_bar(self, surface):
        
        bar_width = self.rect.width * 0.5
        bar_height = 5
        fill_width = int((self.health / self.maxHealth) * bar_width)
    
        background_rect = pygame.Rect(self.rect.left + bar_width * 0.25, self.rect.top + 25, bar_width, bar_height)
        pygame.draw.rect(surface, (60, 60, 60), background_rect)
        current_ratio = self.health / self.maxHealth

        fill_rect = pygame.Rect(self.rect.left + bar_width * 0.25, self.rect.top + 25, fill_width, bar_height)
        color = (255 * (1 - current_ratio), 255 * current_ratio, 0)  # 红 -> 黄 -> 绿

        pygame.draw.rect(surface, color, fill_rect)
        
    def update(self, dt):
        if self.canEnhance and self.enhanceStart >= self.enhanceTime:
            if self.ATK < 100:
                self.ATK += 3
            if(self.health + 5 < self.maxHealth):
                self.health += 5
            self.enhanceStart -= self.enhanceTime
        
        self.input()
        self.move(dt)
        self.bullet_wait(self.shootSpeed)
        self.reload()  # 调用装弹方法
        #print(self.ATK, self.health)
