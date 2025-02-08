import pygame 
from settings import *
from player import Player

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        self.player = Player((640,500), self.all_sprites)
        
    def run(self,dt):
        self.display_surface.blit(pygame.image.load(BACKGROUND_FIGHT_PATH),(0,0))
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)