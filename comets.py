import pygame, sys
import numpy as np
import random
import math
from pygame.locals import *
pygame.init()

DISPLAYSURF= pygame.display.set_mode((800,600))
pygame.display.set_caption("Pygaming")
fpsClock=pygame.time.Clock()
FPS=60

WHITE = (255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK = (0,0,0)

ang=0

playerPos=(50,500)
accel=0

font = pygame.font.SysFont('Arial', 25)
image=pygame.image.load("player.png")
hitbox= pygame.Rect(0,0,36,36)


def translation(x,y,point):
    nTrans=[x,y]
    res=np.add(nTrans,point)
    return (res[0], res[1])

cometsize={
    "large":108,
    "medium":72,
    "small":36
    }

cometcount=0
cometlist=[]

class Comet():
    direction=[1,1]
    speed=0
    size="large"
    hitbox=0
    def __init__(self,center,direction,speed,size):
        self.direction=direction
        self.speed=speed
        self.size=size
        self.hitbox=pygame.Rect(center[0]-(cometsize[size]/2),center[1]-(cometsize[size]/2),cometsize[size],cometsize[size])
        
    def corner(center,size):
        return [center[0]-(size/2),center[1]-(size/2)]

    def spawn(center,direction,speed,size):
        cometlist.append(Comet(center,direction,speed,size))

    def initial():
        surface_size=DISPLAYSURF.get_size()
        for _ in range(3):
            start_pos=(random.randrange(surface_size[0]+1),random.randrange(surface_size[1]+1))
            start_angle=random.randrange(0,201)/100*np.pi
            print(start_angle)
            direction=(np.cos(start_angle),np.sin(start_angle))
            print(direction)
            speed=random.randrange(2,4)
            print(speed)
            Comet.spawn(start_pos,direction,speed,"large")
            
    def move():
        surface_size=DISPLAYSURF.get_size()
        for c in cometlist:
            size=cometsize[c.size]
            center=c.hitbox.center
            corner=Comet.corner(center,size)
            
            new_center=(center[0]+(c.direction[0]*c.speed),center[1]+(c.direction[1]*c.speed))
             
            if new_center[0]<0:
                c.hitbox.move_ip(surface_size[0],0)
                
            elif new_center[0]>surface_size[0]:
                c.hitbox.move_ip(-1*surface_size[0],0)
                
            if new_center[1]<0:
                c.hitbox.move_ip(0,surface_size[1])
                
            elif new_center[1]>surface_size[1]:
                c.hitbox.move_ip(0,-1*surface_size[1])
                
            
            c.hitbox.move_ip((c.direction[0]*c.speed),(c.direction[1]*c.speed))


            
            
    def draw():
        for c in cometlist:
            
            pygame.draw.circle(DISPLAYSURF,WHITE,c.hitbox.center,cometsize[c.size]/2)
            pygame.draw.rect(DISPLAYSURF,GREEN,c.hitbox,1)



Comet.initial()


game=True
while game:

    front_x= playerPos[0]+ math.cos((ang-90)*(np.pi)/180)*18
    front_y= playerPos[1]+ math.sin((ang-90)*(np.pi)/180)*18
    frontPoint=(front_x,front_y)

    playerPos=translation(-accel*(playerPos[0]-frontPoint[0]),-accel*(playerPos[1]-frontPoint[1]),playerPos)

    DISPLAYSURF.fill(BLACK)
    rotimage = pygame.transform.rotate(image,-ang)
    rect = rotimage.get_rect(center=playerPos)
    DISPLAYSURF.blit(rotimage,rect)


    hitbox.center=playerPos
    pygame.draw.rect(DISPLAYSURF,GREEN,hitbox,1)
    pygame.draw.line(DISPLAYSURF,RED,frontPoint,playerPos,2)
    
    Comet.move()
    Comet.draw()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:

        ang-=1
        
    if keys[pygame.K_RIGHT]:

        ang+=1

    if keys[pygame.K_UP]:

        accel+=0.005
        if accel>2:
            accel=2

    if keys[pygame.K_DOWN]:

        accel-=0.005 #temporary, delete when done
        if accel<0:
            accel=0

    if keys[pygame.K_SPACE]:

        #shootBullet()
        pass

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    if playerPos[0]>800:
        playerPos=(playerPos[0]-800,playerPos[1])
    elif playerPos[0]<0:
        playerPos=(playerPos[0]+800,playerPos[1])
    if playerPos[1]>600:
        playerPos=(playerPos[0],playerPos[1]-600)
    elif playerPos[1]<0:
        playerPos=(playerPos[0],playerPos[1]+600)

    pygame.display.update()
    fpsClock.tick(FPS)