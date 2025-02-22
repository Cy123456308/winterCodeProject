import random
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
        self.health = 100
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
        if type <= 4:
            start_pos = (target_pos[0], 0)
        else:
            start_pos = target_pos
        super().__init__(start_pos, group)
        
        # 移动参数
        self.target_pos = pygame.math.Vector2(target_pos)
        self.oscillation_range = 80  # 左右摆动范围
        self.oscillation_speed = 1.5  # 摆动速度（弧度/秒）
        self.oscillation_phase = 0    # 摆动相位
        self.ATK = 10
        
        # 射击参数
        self.can_shoot = False
        self.shoot_cooldown = 0.4     # 射击间隔
        self.last_shot_time = 0
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets_group = bulletGruop  # 存储敌人子弹组

    def update(self, dt):
        # 第一阶段：移动到目标位置
        if not hasattr(self, '_reached_target'):
            if self.type <= 4:
                move_vector = self.target_pos - self.pos
                if move_vector.length() > 2:
                    move_vector = move_vector.normalize()
                    self.pos += move_vector * self.speed * dt
                    self.rect.center = self.pos
                else:
                    self._reached_target = True  # 标记到达目标位置
                    self.oscillation_center = self.pos.copy()  # 记录摆动中心
                    self.can_shoot = True
                    self.last_shot_time = time.time()
            else:
                self.oscillation_center = self.pos.copy()  # 记录摆动中心
                self._reached_target = True  # 标记到达目标位置
                self.oscillation_center = self.pos.copy()  # 记录摆动中心
                self.can_shoot = True
                self.last_shot_time = time.time()
                
        # 第二阶段：左右摆动并射击
        else:
            # 摆动逻辑（正弦曲线运动）
            self.oscillation_phase += self.oscillation_speed * dt
            offset_x = math.sin(self.oscillation_phase) * self.oscillation_range
            self.pos.x = self.oscillation_center.x + offset_x
            self.rect.centerx = int(self.pos.x)
            
            # 射击逻辑
            if time.time() - self.last_shot_time >= self.shoot_cooldown:
                self.shoot()
                self.last_shot_time = time.time()

        # 更新子弹

    def shoot(self):
        """向下发射子弹"""
        bullet = Bullet(
            self.rect.centerx,
            self.rect.centery + 20,  # 从底部下方发射
            10, 10, BULLET_PATH_2, 
            800, (0, 1),  # 方向向下
            self.ATK, # 攻击力
            group=[self.group, self.enemy_bullets_group]
        )
        self.bullets.add(bullet)
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

class Robot(Enemy):
    def __init__(self, start_point, end_point, type, group, speed=0.5):
        self.health = 200
        """
        :param start_point: 起点坐标 (x, y)
        :param end_point:   终点坐标 (x, y)
        :param type:        机器人类型（用于选择图像）
        :param group:       精灵所属组
        :param speed:       运动速度（控制单位时间内插值进度的变化量）
        """
        # 使用起点作为初始位置
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
        self.rect = self.image.get_rect()
        
        # 将起点和终点转换为 Vector2
        self.start_point = pygame.math.Vector2(start_point)
        self.end_point = pygame.math.Vector2(end_point)
        
        # 初始位置设为起点
        self.pos = self.start_point.copy()
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        
        # 记录沿直线移动的进度（0.0 表示完全在起点，1.0 表示完全到达终点）
        self.progress = 0.0
        # 控制运动速度（单位：每秒进度变化量）
        self.speed = speed
        # 运动方向，1 表示从起点向终点运动，-1 表示反方向
        self.direction = 1

    def update(self, dt):
        """
        dt: 帧间时间间隔（单位秒）
        """
        # 根据时间增量更新进度
        self.progress += self.direction * dt * self.speed
        
        # 当超过 0~1 范围时反向
        if self.progress >= 1.0:
            self.progress = 1.0
            self.direction = -1  # 到达终点后，改变方向
        elif self.progress <= 0.0:
            self.progress = 0.0
            self.direction = 1   # 到达起点后，改变方向
        
        # 利用线性插值计算当前位置
        self.pos = self.start_point.lerp(self.end_point, self.progress)
        self.rect.center = (int(self.pos.x), int(self.pos.y))
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
