import pygame 
from settings import *
from player import Player
from CollisionManager import CollisionManager
from enemy import Drone, Robot

class Level:
    def __init__(self, roleNum):

        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.role = roleNum
        self.setup()

    def setup(self):
        self.player = Player((640,800), self.all_sprites, self.player_bullets, self.role)
        self.enemies.add(Drone((320,200), 1, self.all_sprites, self.enemy_bullets))
        self.enemies.add(Drone((480,200), 2, self.all_sprites, self.enemy_bullets))
        self.enemies.add(Drone((640,200), 3, self.all_sprites, self.enemy_bullets))
        self.enemies.add(Drone((960,200), 4, self.all_sprites, self.enemy_bullets))
        self.enemies.add(Drone((800,200), 5, self.all_sprites, self.enemy_bullets))
        self.enemies.add(Robot((640,300), (400,240), 1, self.all_sprites))
        # 初始化碰撞管理器
        self.collision_manager = CollisionManager(
            player=self.player,
            enemies_group=self.enemies,
            player_bullets_group=self.player_bullets,
            enemy_bullets_group=self.enemy_bullets,
            playerATK=self.player.ATK
        )
        
    def run(self,dt):
        self.display_surface.blit(pygame.image.load(BACKGROUND_FIGHT_PATH),(0,0))
        self.collision_manager.check_collisions()
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
        