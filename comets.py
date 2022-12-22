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

game=True
while game:

    front_x= playerPos[0]+ math.cos((ang-90)*(np.pi)/180)*18
    front_y= playerPos[1]+ math.sin((ang-90)*(np.pi)/180)*18
    frontPoint=(front_x,front_y)

    DISPLAYSURF.fill(BLACK)
    rotimage = pygame.transform.rotate(image,-ang)
    rect = rotimage.get_rect(center=playerPos)
    DISPLAYSURF.blit(rotimage,rect)


    playerPos=translation(-accel*(playerPos[0]-frontPoint[0]),-accel*(playerPos[1]-frontPoint[1]),playerPos)

    hitbox.center=playerPos
    pygame.draw.rect(DISPLAYSURF,GREEN,hitbox,1)
    pygame.draw.line(DISPLAYSURF,RED,frontPoint,playerPos,2)
    
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

        accel+=0.001

    if keys[pygame.K_DOWN]:

        accel-=0.001 #temporary, delete when done

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()



    pygame.display.update()
    fpsClock.tick(FPS)