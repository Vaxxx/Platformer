#Special thanks to KidsCanCode Video series
#Extracted from Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
#Part 5
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
        self.loadFiles()
  
    def loadFiles(self):
        self.gameFolder = os.path.dirname(__file__)
        self.imgFolder = os.path.join(self.gameFolder, "images")
         
        self.spritesheet = Spritesheet(os.path.join(self.imgFolder, SPRITESHEET))
        
        
    def new(self):
        #start a new game
        self.allSprites = pygame.sprite.Group() 
        
      
        self.platformGroup = pygame.sprite.Group()
        
        self.actor = Actor(self)
        self.allSprites.add(self.actor)   
        #step 13-> add platform list
        for p in PLATFORM_LIST:
            pform = Platform(self, *p)
            self.allSprites.add(pform)
            self.platformGroup.add(pform)
        
        #step 12-> remove former created former platform      
        #define platform object
        # platformA = Platform(0, HEIGHT-20, WIDTH, 20)
        # self.allSprites.add(platformA)
        # self.platformGroup.add(platformA)
        
        # platformB = Platform(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20)
        # self.allSprites.add(platformB)
        # self.platformGroup.add(platformB)
        
          
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
            #step 1: add key for jumping
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.actor.jump()
        
    def update(self):
        self.allSprites.update() 
        #step8
        #check if player touches a platform when there is velocity
        if self.actor.velocity.y > 0:
            #check collision between the actor and the platform
            platformCollision = pygame.sprite.spritecollide(self.actor, self.platformGroup, False)
            if platformCollision:
                self.actor.position.y = platformCollision[0].rect.top
                self.actor.velocity.y = 0 #set to 0 so the actor doesn't fall through the platform
        
        #step9
        #check if player reaches top quarter of the screen
        if self.actor.rect.top <= HEIGHT / 4:
            self.actor.position.y += max(abs(self.actor.velocity.y), 2)
            for platform in self.platformGroup:
                platform.rect.y += max(abs(self.actor.velocity.y),2)
                if platform.rect.top >= HEIGHT:
                    platform.kill()
                    
                
    def draw(self):
        self.screen.fill(BLACK)
        self.allSprites.draw(self.screen)
        pygame.display.flip()
        
    
gamePlay = GamePlay()
while gamePlay.running:
    gamePlay.new()
    
pygame.quit()