#Special thanks to KidsCanCode Video series
#Extracted from Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
#Part 6
#created by Vakpo Okagbare

import pygame
import random
from settings import * 
from sprite import *
import os

class GamePlay:
    def __init__(self):
        pygame.init()#initialize all pygame function
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True 
        #step5
        self.fontName = pygame.font.match_font(FONT_NAME)      
        self.loadFiles()
  
    def loadFiles(self):
        self.gameFolder = os.path.dirname(__file__)
        self.imgFolder = os.path.join(self.gameFolder, "images")
         
        self.spritesheet = Spritesheet(os.path.join(self.imgFolder, SPRITESHEET))
        
        
    def new(self):
        #start a new game
        
        #step6
        self.score = 0
        
        
        self.allSprites = pygame.sprite.Group() 
        
      
        self.platformGroup = pygame.sprite.Group()
        
        self.actor = Actor(self)
        self.allSprites.add(self.actor)   
        #  add platform list
        for p in PLATFORM_LIST:
            pform = Platform(self, *p)
            self.allSprites.add(pform)
            self.platformGroup.add(pform) 
        self.run()
        
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.actor.jump()
        
    def update(self):
        self.allSprites.update()  
        #check if player touches a platform when there is velocity
        if self.actor.velocity.y > 0:
            #check collision between the actor and the platform
            platformCollision = pygame.sprite.spritecollide(self.actor, self.platformGroup, False)
            if platformCollision:
                self.actor.position.y = platformCollision[0].rect.top
                self.actor.velocity.y = 0 #set to 0 so the actor doesn't fall through the platform
        
        #step 8a
        #check if actor reaches top quarter of the screen
        if self.actor.rect.top <= HEIGHT * 0.25:
            self.actor.position.y +=  max(abs(self.actor.velocity.y),2)
            for platform in self.platformGroup:
                platform.rect.y += max(abs(self.actor.velocity.y),2)
                if platform.rect.top >= HEIGHT:
                    platform.kill()
                    #step 8b
                    self.score += random.randrange(1,5)
        #step9-> create death act
        if self.actor.rect.bottom > HEIGHT:
            for sprite in self.allSprites:
                sprite.rect.y -= max(self.actor.velocity.y, 10)
                #check if actor goes off the screen
                if sprite.rect.bottom < 0:            
                    sprite.kill()
        if len(self.platformGroup) == 0:
            self.playing = False 
            
        #step10
        #spawn new platform to keep same average number
        while len(self.platformGroup) < 6: #where 6 is the amount of platform already existing
            width = random.randrange(50,100)
            platform = Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30))
            self.platformGroup.add(platform)
            self.allSprites.add(platform)
                
    def draw(self):
        self.screen.fill(BLACK)
        self.allSprites.draw(self.screen)
        
        #step13
        self.screen.blit(self.actor.image, self.actor.rect)
        #step11
        self.addText(str(self.score), 25, WHITE, WIDTH/2, 15)
        
        pygame.display.flip()
    
    #step7
    def addText(self, text, size, color, xPos, yPos):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midtop = (xPos, yPos)
        self.screen.blit(textSurface, textRect)
        
    
gamePlay = GamePlay()
while gamePlay.running:
    gamePlay.new()
    
pygame.quit()