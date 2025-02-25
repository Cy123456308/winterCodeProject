import pygame
from settings import *

class CollisionManager:
    def __init__(self, 
                 player, 
                 enemies_group, 
                 shields_group,
                 player_bullets_group,
                 player_penetrate_bullets_group,
                 enemy_bullets_group,
                 playerATK
                ):
        self.player = player
        self.enemies = enemies_group
        self.shields = shields_group
        self.player_bullets = player_bullets_group
        self.player_penetrate_bullets_group = player_penetrate_bullets_group
        self.enemy_bullets = enemy_bullets_group
        self.playerATK = playerATK
        self.enemyATK = 10
    
    def check_collisions(self):
        # 子弹与掩体碰撞
        shield_hit_player = pygame.sprite.groupcollide(
            self.shields, 
            self.player_bullets, 
            dokilla=False,  
            dokillb=True,  # 碰撞后移除子弹
            collided=pygame.sprite.collide_mask  
        )
        
        shield_hit_enemy = pygame.sprite.groupcollide(
            self.shields, 
            self.enemy_bullets, 
            dokilla=False,  
            dokillb=True,  # 碰撞后移除子弹
            collided=pygame.sprite.collide_mask  
        )
            
        # 玩家与敌方子弹碰撞
        player_hit = pygame.sprite.spritecollide(
            self.player, 
            self.enemy_bullets, 
            dokill=True,  # 碰撞后移除子弹
            collided=pygame.sprite.collide_mask  # 80%重叠视为碰撞
        )
        if player_hit:
            self.player.take_damage(len(player_hit) * self.enemyATK)
            #print(f"玩家血量：{self.player.health}")
        
        # 敌方与玩家子弹碰撞
        enemies_hit = pygame.sprite.groupcollide(
            self.enemies,
            self.player_bullets,
            dokilla=False,  # 不自动移除敌人
            dokillb=True,   # 自动移除子弹
            collided=pygame.sprite.collide_mask  
        )
        for enemy, bullets in enemies_hit.items():
            enemy.take_damage(len(bullets) * self.playerATK)
            if self.player.canEnhance:
                self.player.enhanceStart += len(bullets)
                #print(self.player.ATK, self.player.health)
            #print(f"敌人血量：{enemy.health}")

        enemy_penetrate_hit = pygame.sprite.groupcollide(
            self.enemies,
            self.player_penetrate_bullets_group,
            dokilla=False,  
            dokillb=False,  
            collided=pygame.sprite.collide_mask  
        )
        for enemy, bullets in enemy_penetrate_hit.items():
            enemy.take_damage(len(bullets) * self.playerATK)

            
        player_enemies_hit = pygame.sprite.spritecollide(
            self.player, 
            self.enemies, 
            dokill=False,  # 碰撞后移除子弹
            collided=pygame.sprite.collide_mask  # 80%重叠视为碰撞
        )
        if player_enemies_hit:
            self.player.take_damage(len(player_hit) * 30)