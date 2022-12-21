import pygame, sys
import numpy as np
import random
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

ang=90

playerPos=(50,500)
accel=0

def spawnComet(size):
    cometType=random.randrange(1,4)

    if cometType==1:
        size=(50,50)

    elif cometType==2: #size: 1="small", 2="medium", 3="large"
        size=(125,125)

    else:
        size=(200,200)


def drawTriangle(p1,p2,p3,colour,radius):
    pygame.draw.line(DISPLAYSURF,colour,p1,p2,radius)
    pygame.draw.line(DISPLAYSURF,colour,p2,p3,radius)
    pygame.draw.line(DISPLAYSURF,colour,p3,p1,radius)

def translation(x,y,point):
    nTrans=[x,y]
    res=np.add(nTrans,point)
    return (res[0], res[1])

point1=(playerPos[0],playerPos[1]-25)
point2=(playerPos[0]-18,playerPos[1]+10)
point3=(playerPos[0]+18,playerPos[1]+10)

while True:

    midpoint=np.divide(np.add(point2,point3),2)

    DISPLAYSURF.fill(BLACK)
    drawTriangle(point1,point2,point3,GREEN,2)

    playerPos=translation(-accel*(playerPos[0]-point1[0]),-accel*(playerPos[1]-point1[1]),playerPos)
    pygame.draw.line(DISPLAYSURF,RED,midpoint,point1,2)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:

        pass
        
    if keys[pygame.K_RIGHT]:

        pass

    if keys[pygame.K_UP]:

        accel+=0.001

    if keys[pygame.K_DOWN]:

        accel-=0.001 #temporary, delete when done

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()


    point1=(playerPos[0],playerPos[1]-25)
    point2=(playerPos[0]-18,playerPos[1]+10)
    point3=(playerPos[0]+18,playerPos[1]+10)



    pygame.display.update()
    fpsClock.tick(FPS)