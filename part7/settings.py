TITLE = "PLATFORMER"
WIDTH = 500
HEIGHT = 700
FPS = 60 
ACTOR_ACCELERATION = 0.5
ACTOR_FRICTION = -0.12 
ACTOR_GRAVITY = 0.8
#SET A JUMP VARIABLE
ACTOR_JUMP = 30  
#set a font
FONT_NAME= 'Times New Roman' 
 
SPRITESHEET = 'spritesheet.png'


#colors
GREY    = (190, 190, 190)
WHITE   = (255, 255, 255)
BLACK   = (0  , 0,   0)
RED     = (255, 0,   0)
GREEN   = (0,   255, 0)
BLUE    = (50,    50,  200)
YELLOW  = (255, 255,  0)
PURPLE  = (255, 0, 255)
#step 1
BACKGROUND_COLOR = BLUE

 
#add platform array
PLATFORM_LIST = [
     (0, HEIGHT-60),
     (WIDTH / 2 - 50, HEIGHT * 0.75 - 50),
     (125, HEIGHT - 350),
     (350, 200),
     (175, 100)
]