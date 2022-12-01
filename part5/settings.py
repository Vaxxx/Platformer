TITLE = "PLATFORMER"
WIDTH = 500
HEIGHT = 700
FPS = 60 
ACTOR_ACCELERATION = 0.5
ACTOR_FRICTION = -0.14

 
ACTOR_GRAVITY = 0.5
 
SPRITESHEET = 'spritesheet.png'


#colors
GREY    = (190, 190, 190)
WHITE   = (255, 255, 255)
BLACK   = (0  , 0,   0)
RED     = (255, 0,   0)
GREEN   = (0,   255, 0)
BLUE    = (0,    0,  255)
YELLOW  = (255, 255,  0)
PURPLE  = (0,  255, 255)

#step 7
#add platform array
PLATFORM_LIST = [
     (0, HEIGHT-60),
     (WIDTH / 2 - 50, HEIGHT * 0.75 - 50),
     (125, HEIGHT - 350),
     (350, 200),
     (175, 100)
]