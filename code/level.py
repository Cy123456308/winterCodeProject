import time
import pygame
import random
import settings
from settings import *

from player import Player
from CollisionManager import CollisionManager
from enemy import Drone, Robot, Shooter, Girl, RocketShooter
from shield import Shield

class Level:
    def __init__(self, roleNum):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.player_penetrate_bullets_group = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()
        self.role = roleNum

        # 添加刷新计时器
        self.enemy_timer = 0
        self.enemy_interval = 20
        self.shield_timer = 0
        self.shield_interval = 30

        # 用于增加敌人血量的难度因子
        self.enemy_health_multiplier = 1.0

        self.setup()

    def setup(self):
        self.player = Player((640, 800), self.all_sprites, self.player_bullets, self.player_penetrate_bullets_group, self.role)

        # 初始生成掩体
        self.spawn_shields()

        # 初始化碰撞管理器
        self.collision_manager = CollisionManager(
            player=self.player,
            enemies_group=self.enemies,
            shields_group=self.shields,
            player_bullets_group=self.player_bullets,
            player_penetrate_bullets_group=self.player_penetrate_bullets_group,
            enemy_bullets_group=self.enemy_bullets,
            playerATK=self.player.ATK
        )

    def spawn_enemies(self):
        # 增加敌人难度（例如：血量乘以一个因子）
        self.enemy_health_multiplier += 0.1
        # 根据需要生成敌人，这里举例生成三个不同类型的敌人
        enemy_types = [Girl, RocketShooter, Shooter, Drone]
        for _ in range(min(int((8 + (self.enemy_health_multiplier - 1) * 3) // 2), 10)):
            enemy_class = random.choice(enemy_types)
            x = random.randint(100, 1100)  # 你可以调整屏幕范围
            y = random.randint(100, 300)  # 你可以调整屏幕范围
            self.enemies.add(enemy_class((x, y), random.randint(1, 5), self.all_sprites, self.enemy_bullets))
        for enemy in self.enemies:
            enemy.max_health = int(enemy.max_health * self.enemy_health_multiplier)
            enemy.health = int(enemy.health * self.enemy_health_multiplier)

    def spawn_shields(self):
        """在随机位置生成新的掩体"""
        # 清空当前掩体
        for shield in self.shields:
            shield.kill()

        # 随机生成一个新的掩体
        # 假设屏幕宽高分别为 WIDTH 和 HEIGHT，可以从 settings 导入
        x = random.randint(100, 400)
        y = random.randint(400, SCREEN_HEIGHT - 100)
        self.shields.add(Shield((x, y), self.all_sprites))
        x = random.randint(500, 800)
        y = random.randint(400, SCREEN_HEIGHT - 100)
        self.shields.add(Shield((x, y), self.all_sprites))
        x = random.randint(900, 1200)
        y = random.randint(400, SCREEN_HEIGHT - 100)
        self.shields.add(Shield((x, y), self.all_sprites))
    
    def run(self, dt, paused):
        if not paused and not settings.ending:
            self.display_surface.blit(pygame.image.load(BACKGROUND_FIGHT_PATH_FINAL), (0, 0))

            # 累加计时器（dt单位需与设定间隔一致，若 dt 为毫秒则无需转换）
            self.enemy_timer += dt
            self.shield_timer += dt
            
            # 每隔一定时间刷新敌人，并增加难度
            if self.enemy_timer >= self.enemy_interval:
                self.spawn_enemies()
                self.enemy_timer = 0
                self.player.health = min(self.player.health + 20, self.player.maxHealth)

            # 如果场上敌人全部消失，也重新生成敌人
            if len(self.enemies) == 0:
                time.sleep(1)
                self.spawn_enemies()
                self.enemy_timer = 0

            # 每隔一定时间刷新掩体
            if self.shield_timer >= self.shield_interval:
                self.spawn_shields()
                self.shield_timer = 0

            self.collision_manager.check_collisions()
            self.all_sprites.update(dt)

        self.all_sprites.draw(self.display_surface)
        for sprite in self.all_sprites:
            if hasattr(sprite, 'draw_health_bar'):
                sprite.draw_health_bar(self.display_surface)
