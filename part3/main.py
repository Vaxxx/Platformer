#Special thanks to KidsCanCode Video series
#Extracted from Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
#Part 3
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
        self.actor = Actor(self)
        self.allSprites.add(self.actor)     
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
        
    def update(self):
        self.allSprites.update()
                
    def draw(self):
        self.screen.fill(BLACK)
        self.allSprites.draw(self.screen)
        pygame.display.flip()
        
    
gamePlay = GamePlay()
while gamePlay.running:
    gamePlay.new()
    
pygame.quit()