import pygame
from settings import *

class CollisionManager:
    def __init__(self, 
                 player, 
                 enemies_group, 
                 player_bullets_group, 
                 enemy_bullets_group
                ):
        self.player = player
        self.enemies = enemies_group
        self.player_bullets = player_bullets_group
        self.enemy_bullets = enemy_bullets_group
    
    def check_collisions(self):
        # 玩家与敌方子弹碰撞
        player_hit = pygame.sprite.spritecollide(
            self.player, 
            self.enemy_bullets, 
            dokill=True,  # 碰撞后移除子弹
            collided=pygame.sprite.collide_mask  # 80%重叠视为碰撞
        )
        if player_hit:
            self.player.take_damage(len(player_hit))
        
        # 敌方与玩家子弹碰撞
        enemies_hit = pygame.sprite.groupcollide(
            self.enemies,
            self.player_bullets,
            dokilla=False,  # 不自动移除敌人
            dokillb=True,   # 自动移除子弹
            collided=pygame.sprite.collide_mask  # 精确碰撞检测
        )
        for enemy, bullets in enemies_hit.items():
            enemy.take_damage(len(bullets))
