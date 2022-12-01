#Special thanks to KidsCanCode Video series
#Extracted from Video link: https://www.youtube.com/watch?v=uWvb3QzA48c
#Part 8
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
        self.fontName = pygame.font.match_font(FONT_NAME)      
    
        self.loadFiles()
  
    # -> adjust the loadFiles method
    def loadFiles(self):
        self.gameFolder = os.path.dirname(__file__)
        self.imgFolder = os.path.join(self.gameFolder, "images")
        
        with open(os.path.join(self.gameFolder, HIGHSCORE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
                return "error in finding highscore.txt file"
         
        self.spritesheet = Spritesheet(os.path.join(self.imgFolder, SPRITESHEET))
        
        
    def new(self):
        #start a new game 
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
        
        
        #check if actor reaches top quarter of the screen
        if self.actor.rect.top <= HEIGHT * 0.25:
            self.actor.position.y +=  max(abs(self.actor.velocity.y),2)
            for platform in self.platformGroup:
                platform.rect.y += max(abs(self.actor.velocity.y),2)
                if platform.rect.top >= HEIGHT:
                    platform.kill() 
                    self.score += random.randrange(1,5)
        #  create death act
        if self.actor.rect.bottom > HEIGHT:
            for sprite in self.allSprites:
                sprite.rect.y -= max(self.actor.velocity.y, 10)
                #check if actor goes off the screen
                if sprite.rect.bottom < 0:            
                    sprite.kill()
        if len(self.platformGroup) == 0:
            self.playing = False 
            
       
        #spawn new platform to keep same average number
        while len(self.platformGroup) < 6: #where 6 is the amount of platform already existing
            width = random.randrange(50,100)
            platform = Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30))
            self.platformGroup.add(platform)
            self.allSprites.add(platform)
                
    def draw(self): 
        self.screen.fill(BACKGROUND_COLOR)
        self.allSprites.draw(self.screen)
        
    
        self.screen.blit(self.actor.image, self.actor.rect)
         
        self.addText(str(self.score), 25, WHITE, WIDTH/2, 15)
        
        pygame.display.flip()
     
 
    def startScreen(self):
        #start scren
        self.screen.fill(BACKGROUND_COLOR)
        self.addText(TITLE, 50, GREY, WIDTH / 2, HEIGHT / 4)
        self.addText('Use Arrow keys for motion & Space key to jump', 25, GREY, WIDTH / 2, HEIGHT / 2)
        self.addText("Press any key to play", 20, GREY, WIDTH / 2, HEIGHT * 0.75)
        
      
        self.addText("HIGH SCORE: " + str(self.highscore), 25, GREY, WIDTH / 2, 16 )
        
        pygame.display.flip()
        self.timedKeyPress()
        
     
    def timedKeyPress(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False
  
    def hudScreen(self):
        if not self.running:
            return
        #game over/continue screen
        self.screen.fill(BACKGROUND_COLOR)
        self.addText("GAME OVER", 50, GREY, WIDTH / 2, HEIGHT / 4)
        self.addText("SCORE: " + str(self.score), 25, GREY, WIDTH / 2, HEIGHT / 2)
        self.addText("Press any key to play", 20, GREY, WIDTH / 2, HEIGHT * 0.75)
        
     
        if self.score > self.highscore:
            self.highscore = self.score
            self.addText("NEW HIGH SCORE!", 25,  GREY, WIDTH / 2, HEIGHT / 2 + 40)
            with open(os.path.join(self.gameFolde, HIGHSCORE), 'w') as f:
                f.write(str(self.score))
        else:
            self.addText("HIGH SCORE: " + str(self.highscore), 25, GREY, WIDTH / 2, HEIGHT / 2 + 40)
        
        pygame.display.flip()
        self.timedKeyPress()
   
    def addText(self, text, size, color, xPos, yPos):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midtop = (xPos, yPos)
        self.screen.blit(textSurface, textRect)
        
    
gamePlay = GamePlay()
 
gamePlay.startScreen()
while gamePlay.running:
    gamePlay.new() 
    gamePlay.hudScreen()
    
pygame.quit()