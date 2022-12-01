import pygame
from settings import *

 
vector = pygame.math.Vector2
 
class Spritesheet:
    #class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()
        
    def getImage(self, xPos, yPos, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (xPos, yPos, width, height))
         
        image = pygame.transform.scale(image, (width//2, height//2))        
        return image
 
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
 
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
    
 
    def update(self): 
        #step 2-> add gravity to acc
        self.acceleration = vector(0, ACTOR_GRAVITY)
        
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -ACTOR_ACCELERATION
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = ACTOR_ACCELERATION 
        self.acceleration += self.velocity * ACTOR_FRICTION 
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
         
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = WIDTH     
        #step6    
        self.rect.midbottom = self.position
        
#step 3
#create a platform for object to stand on
class Platform(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos