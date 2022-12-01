import pygame
from settings import * 
import random
 
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
        pygame.sprite.Sprite.__init__(self)
        self.game  = game #this gives the actor access to all game attributes
      
        self.walking = False
        self.jumping = False
        self.currentFrame = 0
        self.lastUpdate = 0 
        self.loadImages() 
        self.image = self.standingFrames[0]
        
        #.........................................this can be seen in line 9 of the spritesheet.xml
        self.image = self.game.spritesheet.getImage(614, 1063, 120, 191)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        
        # >change position
        self.position = vector(40, HEIGHT - 100)
        
        # remove former position
        #self.position = vector(WIDTH/2, HEIGHT/2) 
        self.velocity = vector(0,0)
        self.acceleration = vector(0,0) 
    def loadImages(self):
        
        self.standingFrames = [
            self.game.spritesheet.getImage(614, 1063, 120, 191),
            self.game.spritesheet.getImage(690, 406, 120, 201)
        ]
        for frame in self.standingFrames:
            frame.set_colorkey(BLACK)
        
        self.walkingFrameRight = [
           self.game.spritesheet.getImage(678, 860, 120, 201),
            self.game.spritesheet.getImage(692, 1458, 120, 207)
        ]
        self.walkingFrameLeft = []
        for frame in self.walkingFrameRight:
            frame.set_colorkey(BLACK)
            #............................frame, horizontalFlip=true, verticalFlip = false
            self.walkingFrameLeft.append(pygame.transform.flip(frame, True, False))
        self.jumpFrame = self.game.spritesheet.getImage(382, 763, 150, 181)
        self.jumpFrame.set_colorkey(BLACK)
 
    #define a jump method    
    def jump(self):
        self.rect.y += 2
        platformCollision = pygame.sprite.spritecollide(self, self.game.platformGroup, False)
        self.rect.y -= 2
        if platformCollision:
            #  replace with variable
            self.velocity.y = -ACTOR_JUMP 
            
    def animate(self):
        now = pygame.time.get_ticks()
        
        #step1
        #walking animation
        if self.velocity.x != 0:
            self.walking = True
        else:
            self.walking = False
            
        #step 2
        #show walk animation
        if self.walking:
            if now - self.lastUpdate > 180:
                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.walkingFrameLeft)
                bottom = self.rect.bottom
                if self.velocity.x > 0:
                    self.image = self.walkingFrameRight[self.currentFrame]
                else:
                    self.image = self.walkingFrameLeft[self.currentFrame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
        
        if not self.jumping and not self.walking:
            if now - self.lastUpdate > 350: #350 in milliseconds
                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.standingFrames)
                
                #set the bottom or feet of the animation
                bottom = self.rect.bottom
                self.image = self.standingFrames[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.bottom  = bottom
 
    def update(self):  
        self.animate() 
        #  add gravity to acc
        self.acceleration = vector(0, ACTOR_GRAVITY) 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -ACTOR_ACCELERATION
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = ACTOR_ACCELERATION 
        self.acceleration += self.velocity * ACTOR_FRICTION 
        self.velocity += self.acceleration
        
        #step 3
        #to make the actor stop moving when the right/left key is not pressed
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0
            
        self.position += self.velocity + 0.5 * self.acceleration
        #step 4-> adjust this position
        #to wrap around the sides of the screen 
        if self.position.x > WIDTH + self.rect.width / 2:
            self.position.x = 0 - self.rect.width / 2
        if self.position.x < 0 - self.rect.width / 2:
            self.position.x = WIDTH + self.rect.width / 2    
        self.rect.midbottom = self.position
        
#create a platform for object to stand on
class Platform(pygame.sprite.Sprite):
    def __init__(self, game, xPos, yPos):
        pygame.sprite.Sprite.__init__(self) 
        self.game = game  
        images = [self.game.spritesheet.getImage(0,288,380,94),
                   self.game.spritesheet.getImage(213, 1662, 201, 100)] 
        # since there are two types of image use the random choice method to choose
        self.image = random.choice(images) 
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos