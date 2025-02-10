import pygame 
from settings import *
from player import Player
from enemy import Drone, Robot

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        self.player = Player((640,800), self.all_sprites)
        self.enemy = []
        self.enemy.append(Drone((320,200), 1, self.all_sprites))
        self.enemy.append(Drone((480,200), 2, self.all_sprites))
        self.enemy.append(Drone((640,200), 3, self.all_sprites))
        self.enemy.append(Drone((960,200), 4, self.all_sprites))
        self.enemy.append(Drone((800,200), 5, self.all_sprites))
        self.enemy.append(Robot((640,300), (400,240), 1, self.all_sprites))

        
    def run(self,dt):
        self.display_surface.blit(pygame.image.load(BACKGROUND_FIGHT_PATH),(0,0))
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)