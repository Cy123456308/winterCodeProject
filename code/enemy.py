import random
import numpy as np
import pygame
import math
from settings import *
from bullet import Bullet
import time

# 敌人类基类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        # 基础属性初始化

        self.pos = pygame.math.Vector2(pos)  # 精确浮点位置
        self.screen = pygame.display.get_surface()
        self.group = group
        
        # 通用移动参数
        self.speed = 100
        self.direction = pygame.math.Vector2()

    def update(self, dt):
        """需要子类实现的更新逻辑"""
        raise NotImplementedError("必须实现update方法")

# 射击型敌人
class Drone(Enemy):
    def __init__(self, target_pos, type, group, bulletGruop):
        self.max_health = 100
        self.health = self.max_health
        self.type = type
        # 加载图像
        if type %4 == 1:
            image_path = DRONE_PATH_1
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 2:
            image_path = DRONE_PATH_2
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 3:
            image_path = DRONE_PATH_3
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 0:
            image_path = DRONE_PATH_4
            self.image = pygame.image.load(image_path).convert_alpha()

        # 初始位置在屏幕顶部中间
        self.rect = self.image.get_rect(center=target_pos)
        start_pos = (target_pos[0], 0)

        super().__init__(start_pos, group)
        
        # 移动参数
        self.target_pos = pygame.math.Vector2(target_pos)
        self.oscillation_range = 80  # 左右摆动范围
        self.oscillation_speed = 1.5  # 摆动速度（弧度/秒）
        self.oscillation_phase = 0    # 摆动相位
        self.ATK = 10
        
        # 射击参数
        self.burst_duration = 5.4    # 持续射击时间（秒）
        self.pause_duration = 3.2    # 射击间隔时间（秒）
        self.is_bursting = True      # 当前是否处于射击阶段
        self.last_phase_change = time.time()  # 上次阶段切换时间
        self.can_shoot = False
        self.shoot_cooldown = 0.3    # 射击间隔
        self.last_shot_time = 0
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets_group = bulletGruop  # 存储敌人子弹组

    def draw_health_bar(self, surface):
    # 血条的尺寸可根据敌人图像宽度或自定义
        bar_width = self.rect.width * 0.5
        bar_height = 5
        # 计算血条填充宽度，按比例显示剩余生命值
        fill_width = int((self.health / self.max_health) * bar_width)
    
        # 血条背景（灰色边框）
        background_rect = pygame.Rect(self.rect.left + bar_width * 0.5, self.rect.top + 25, bar_width, bar_height)
        pygame.draw.rect(surface, (60, 60, 60), background_rect)
        current_ratio = self.health / self.max_health

        # 血条填充（绿色）
        fill_rect = pygame.Rect(self.rect.left + bar_width * 0.5, self.rect.top + 25, fill_width, bar_height)
        color = (255 * (1 - current_ratio), 255 * current_ratio, 0)  # 红 -> 黄 -> 绿

        pygame.draw.rect(surface, color, fill_rect)

    def update(self, dt):
        # 第一阶段：移动到目标位置
        if not hasattr(self, '_reached_target'):
            self.oscillation_center = self.pos.copy()  # 记录摆动中心
            self._reached_target = True  # 标记到达目标位置
            self.oscillation_center = self.pos.copy()  # 记录摆动中心
            self.can_shoot = True
            self.last_shot_time = time.time()
            
                
        # 第二阶段：左右摆动并射击
        else:
            current_time = time.time()
            phase_duration = current_time - self.last_phase_change

            if self.is_bursting:
                # 射击阶段逻辑
                if phase_duration <= self.burst_duration:
                    # 正常射击（原冷却时间逻辑）
                    if current_time - self.last_shot_time >= self.shoot_cooldown:
                        self.shoot()
                        self.last_shot_time = current_time
                else:
                    # 结束射击阶段，进入间隔期
                    self.is_bursting = False
                    self.last_phase_change = current_time
            else:
                # 间隔阶段逻辑
                if phase_duration >= self.pause_duration:
                    # 结束间隔期，开始新射击周期
                    self.is_bursting = True
                    self.last_phase_change = current_time
                    self.last_shot_time = current_time  # 重置射击计时

            # 摆动逻辑保持不变
            self.oscillation_phase += self.oscillation_speed * dt
            offset_x = math.sin(self.oscillation_phase) * self.oscillation_range
            self.pos.x = self.oscillation_center.x + offset_x
            self.rect.centerx = int(self.pos.x)

        # 更新子弹

    def shoot(self):
        """向下发射子弹"""
        bullet = Bullet(
            self.rect.centerx,
            self.rect.centery + 20,  # 从底部下方发射
            15, 15, BULLET_PATH_2, 
            600, (0, 1),  # 方向向下
            self.ATK, # 攻击力
            group=[self.group, self.enemy_bullets_group]
        )
        self.bullets.add(bullet)
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

class Shooter(Enemy):
    def __init__(self, target_pos, type, group, bulletGruop):
        self.max_health = 200
        self.health = self.max_health
        self.type = type
        # 加载图像
        if type %4 == 1:
            image_path = SHOOTER_1
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 2:
            image_path = SHOOTER_2
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 3:
            image_path = SHOOTER_3
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 0:
            image_path = SHOOTER_4
            self.image = pygame.image.load(image_path).convert_alpha()

        # 初始位置在屏幕顶部中间
        self.rect = self.image.get_rect(center=target_pos)
        start_pos = (target_pos[0], 0)

        super().__init__(start_pos, group)
        
        # 固定位置参数
        self.pos = pygame.math.Vector2(target_pos)  # 直接锁定目标位置
        self.oscillation_range = 0  # 关闭摆动
                        
        # 调整射击参数
        self.burst_duration = 4.0    # 更长的射击周期
        self.pause_duration = 2.5
        self.shoot_cooldown = 0.2   # 更快的射速
        self.ATK = 8
        
        self.is_bursting = True      # 当前是否处于射击阶段
        self.last_phase_change = time.time()  # 上次阶段切换时间
        self.can_shoot = False
        self.last_shot_time = 0
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets_group = bulletGruop  # 存储敌人子弹组

    def draw_health_bar(self, surface):
    # 血条的尺寸可根据敌人图像宽度或自定义
        bar_width = self.rect.width * 0.5
        bar_height = 5
        # 计算血条填充宽度，按比例显示剩余生命值
        fill_width = int((self.health / self.max_health) * bar_width)
    
        # 血条背景（灰色边框）
        background_rect = pygame.Rect(self.rect.left + bar_width * 0.5, self.rect.top + 25, bar_width, bar_height)
        pygame.draw.rect(surface, (60, 60, 60), background_rect)
        current_ratio = self.health / self.max_health

        # 血条填充（绿色）
        fill_rect = pygame.Rect(self.rect.left + bar_width * 0.5, self.rect.top + 25, fill_width, bar_height)
        color = (255 * (1 - current_ratio), 255 * current_ratio, 0)  # 红 -> 黄 -> 绿

        pygame.draw.rect(surface, color, fill_rect)

    def update(self, dt):
        # 直接进入射击逻辑（跳过所有移动阶段判断）
        current_time = time.time()
        phase_duration = current_time - self.last_phase_change

        if self.is_bursting:
            if phase_duration <= self.burst_duration:
                if current_time - self.last_shot_time >= self.shoot_cooldown:
                    self.shoot()
                    self.last_shot_time = current_time
            else:
                self.is_bursting = False
                self.last_phase_change = current_time
        else:
            if phase_duration >= self.pause_duration:
                self.is_bursting = True
                self.last_phase_change = current_time
                self.last_shot_time = current_time

    def shoot(self):
        # 在角色宽度范围内生成随机偏移
        random_number = 2 * np.random.random() - 1
        bullet = Bullet(
            self.rect.centerx,  # 添加横向随机偏移
            self.rect.centery + 20,
            19, 19, BULLET_PATH_2, 
            500, (random_number, 1),  # 稍慢的子弹速度
            self.ATK,
            group=[self.group, self.enemy_bullets_group]
        )
        self.bullets.add(bullet)
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

class Girl(Shooter):
    def __init__(self, target_pos, type, group, bulletGruop):
        # 继承父类初始化，并修改血量和攻击力
        super().__init__(target_pos, type, group, bulletGruop)
        
        # 修改弱版Shooter的血量和攻击力
        self.max_health = 120  # 较弱的血量
        self.health = self.max_health  # 设置当前血量
        self.ATK = 5  # 较弱的攻击力
        self.pause_duration = 3.0
        self.type = type
        # 加载图像
        if type %4 == 1:
            image_path = GIRL_1
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 2:
            image_path = GIRL_2
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 3:
            image_path = GIRL_3
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 0:
            image_path = GIRL_4
            self.image = pygame.image.load(image_path).convert_alpha()

class RocketShooter(Shooter):
    def __init__(self, target_pos, type, group, bulletGruop):
        # 继承父类初始化，并修改血量和攻击力
        super().__init__(target_pos, type, group, bulletGruop)
        
        # 修改弱版Shooter的血量和攻击力
        self.max_health = 120  
        self.health = self.max_health  # 设置当前血量
        self.burst_duration = 4.0    
        self.pause_duration = 2.5
        self.shoot_cooldown = 1.0   
        self.ATK = 30
        
        self.type = type
        # 加载图像
        if type %4 == 1:
            image_path = ROCKETSHOOERT_1
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 2:
            image_path = ROCKETSHOOERT_2
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 3:
            image_path = ROCKETSHOOERT_3
            self.image = pygame.image.load(image_path).convert_alpha()
        elif type %4 == 0:
            image_path = ROCKETSHOOERT_4
            self.image = pygame.image.load(image_path).convert_alpha()
            
    def shoot(self):
        random_number = 2 * np.random.random() - 1
        bullet = Bullet(
            self.rect.centerx + random_number,  
            self.rect.centery + 20,
            36, 98, BULLET_PATH_3, 
            500, (random_number, 1),  
            self.ATK,
            group=[self.group, self.enemy_bullets_group]
        )
        self.bullets.add(bullet)

class Robot(Enemy):
    def __init__(self, start_point, type, group, speed=300):
        
        self.max_health = 200
        self.health = self.max_health

        super().__init__(start_point, group)
        
        # 根据 type 加载对应的图像
        if type % 4 == 1:
            image_path = ROBOT_1
        elif type % 4 == 2:
            image_path = ROBOT_2
        elif type % 4 == 3:
            image_path = ROBOT_3
        elif type % 4 == 0:
            image_path = ROBOT_4
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=start_point)
        
        # 初始位置
        self.pos = pygame.math.Vector2(start_point)
        
        # 随机生成初始方向向量，并归一化后乘以速度
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * speed
        
    def update(self, dt):
        # 根据速度和时间增量更新位置
        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        
        # 获取屏幕边界
        screen_rect = self.screen.get_rect()
        
        # 左右边界碰撞检测与反弹
        if self.rect.left < screen_rect.left:
            self.velocity.x *= -1  # 反转水平速度
            self.pos.x = screen_rect.left + self.rect.width / 2  # 调整到左边界内侧
        elif self.rect.right > screen_rect.right:
            self.velocity.x *= -1
            self.pos.x = screen_rect.right - self.rect.width / 2  # 调整到右边界内侧
        
        # 上下边界碰撞检测与反弹
        if self.rect.top < screen_rect.top:
            self.velocity.y *= -1  # 反转垂直速度
            self.pos.y = screen_rect.top + self.rect.height / 2  # 调整到上边界内侧
        elif self.rect.bottom > screen_rect.bottom:
            self.velocity.y *= -1
            self.pos.y = screen_rect.bottom - self.rect.height / 2  # 调整到下边界内侧

    def draw_health_bar(self, surface):
        # 血条绘制逻辑（保持不变）
        bar_width = self.rect.width * 0.5
        bar_height = 5
        fill_width = int((self.health / self.max_health) * bar_width)
    
        background_rect = pygame.Rect(self.rect.left + bar_width * 0.5, self.rect.top + 25, bar_width, bar_height)
        pygame.draw.rect(surface, (60, 60, 60), background_rect)
        current_ratio = self.health / self.max_health

        fill_rect = pygame.Rect(self.rect.left + bar_width * 0.5, self.rect.top + 25, fill_width, bar_height)
        color = (255 * (1 - current_ratio), 255 * current_ratio, 0)
        pygame.draw.rect(surface, color, fill_rect)
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()