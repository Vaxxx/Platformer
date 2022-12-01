import pygame
from settings import *


#step7b
vector = pygame.math.Vector2

#step2
class Spritesheet:
    #class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()
        
    def getImage(self, xPos, yPos, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (xPos, yPos, width, height))
        
        #step 10->reduce the size of the sprites
        #the double slash division is used to produce an absolute int value
        image = pygame.transform.scale(image, (width//2, height//2))        
        return image


#step 7a -> create an actor class
class Actor(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game  = game #this gives the actor access to all game attributes
        pygame.sprite.Sprite.__init__(self)
        #.........................................this can be seen in line 9 of the spritesheet.xml
        self.image = self.game.spritesheet.getImage(614, 1063, 120, 191)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.position = vector(WIDTH/2, HEIGHT/2)
        
    #step 8
    def update(self):
        self.rect.midbottom = self.position