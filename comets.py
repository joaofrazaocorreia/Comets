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
bulletCooldownMain=0
bulletCooldown1=0
bulletCooldown2=0
bulletCooldown3=0
bulletCooldown4=0

font = pygame.font.SysFont('Arial', 25)
image=pygame.image.load("player.png")
hitbox= pygame.Rect(0,0,36,36)
bullet= pygame.Rect(0,0,5,20)
shot1=False
shot2=False
shot3=False
shot4=False
spawnAssigned1=False
spawnAssigned2=False
spawnAssigned3=False
spawnAssigned4=False


def shootBullet(cooldown):
    currentTime=pygame.time.get_ticks()

    if cooldown+1000>currentTime:
        return False

    else:
        return True

def translation(x,y,point):
    nTrans=[x,y]
    res=np.add(nTrans,point)
    return (res[0], res[1])

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
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:

        ang-=2
        
    if keys[pygame.K_RIGHT]:

        ang+=2

    if keys[pygame.K_UP]:

        accel+=0.005
        if accel>2:
            accel=2

    if keys[pygame.K_DOWN]:

        accel-=0.005 #temporary, delete when done
        if accel<0:
            accel=0

    if keys[pygame.K_SPACE]:

        if not shot1: 
            shot1=shootBullet(bulletCooldownMain)
            bulletCooldown1=pygame.time.get_ticks()
            if shot1:
                bulletCooldownMain=pygame.time.get_ticks()

        elif not shot2:
            shot2=shootBullet(bulletCooldownMain)
            bulletCooldown2=pygame.time.get_ticks()
            if shot2:
                bulletCooldownMain=pygame.time.get_ticks()

        elif not shot3:
            shot3=shootBullet(bulletCooldownMain)
            bulletCooldown3=pygame.time.get_ticks()
            if shot3:
                bulletCooldownMain=pygame.time.get_ticks()

        elif not shot4:
            shot4=shootBullet(bulletCooldownMain)
            bulletCooldown4=pygame.time.get_ticks()
            if shot4:
                bulletCooldownMain=pygame.time.get_ticks()



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

    if shot1:
        while not spawnAssigned1:
            bulletPos1=frontPoint
            spawnAssigned1=True

        bulletPos1=np.add(bulletPos1,(2,-2))

        bullet.center=bulletPos1
        pygame.draw.rect(DISPLAYSURF,WHITE,bullet,10)
        
        if bulletCooldown1+4000<=pygame.time.get_ticks():
            shot1=False
            spawnAssigned1=False

    if shot2:
        while not spawnAssigned2:
            bulletPos2=frontPoint
            spawnAssigned2=True

        bulletPos2=np.add(bulletPos2,(2,-2))

        bullet.center=bulletPos2
        pygame.draw.rect(DISPLAYSURF,WHITE,bullet,10)
        
        if bulletCooldown2+4000<=pygame.time.get_ticks():
            shot2=False
            spawnAssigned2=False

    if shot3:
        while not spawnAssigned3:
            bulletPos3=frontPoint
            spawnAssigned3=True

        bulletPos3=np.add(bulletPos3,(2,-2))

        bullet.center=bulletPos3
        pygame.draw.rect(DISPLAYSURF,WHITE,bullet,10)
        
        if bulletCooldown3+4000<=pygame.time.get_ticks():
            shot3=False
            spawnAssigned3=False

    if shot4:
        while not spawnAssigned4:
            bulletPos4=frontPoint
            spawnAssigned4=True

        bulletPos4=np.add(bulletPos4,(2,-2))

        bullet.center=bulletPos4
        pygame.draw.rect(DISPLAYSURF,WHITE,bullet,10)
        
        if bulletCooldown4+4000<=pygame.time.get_ticks():
            shot4=False
            spawnAssigned4=False





    pygame.display.update()
    fpsClock.tick(FPS)