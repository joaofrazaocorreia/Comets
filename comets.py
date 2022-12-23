import pygame, sys
import numpy as np
import random
import math
from pygame.locals import *
pygame.init()

DISPLAYSURF= pygame.display.set_mode((800,600))
pygame.display.set_caption("Comets")
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
player_image=pygame.image.load("player.png")
bullet_image=pygame.image.load("bullet.png")
hitbox= pygame.Rect(0,0,36,36)
bullet_hitbox= pygame.Rect(0,0,22,22)

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


def wrap_around(position):
    if position[0]>800:
        position=(position[0]-800,position[1])
    elif position[0]<0:
        position=(position[0]+800,position[1])
    if position[1]>600:
        position=(position[0],position[1]-600)
    elif position[1]<0:
        position=(position[0],position[1]+600)
    
    return position


cometsize={
    "large":108,
    "medium":72,
    "small":36
    }


cometmax=9
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
            direction=(np.cos(start_angle),np.sin(start_angle))
            speed=random.randrange(2,4)
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


    def split(list_pos):
        blown=cometlist.pop(list_pos)
        split_max=cometmax-len(cometlist)
        if blown.size=="large":
            start_pos=Comet.corner(blown.hitbox.center,cometsize[blown.size])
            speed=blown.speed
            
            for _ in range (min(3,split_max)):
                start_angle=random.randrange(0,201)/100*np.pi
                direction=(np.cos(start_angle),np.sin(start_angle))
                
                Comet.spawn(start_pos,direction,speed,"medium")
     
        elif blown.size=="medium":
            start_pos=Comet.corner(blown.hitbox.center,cometsize[blown.size])
            speed=blown.speed
            for _ in range (min(5,split_max)):
                start_angle=random.randrange(0,201)/100*np.pi
                direction=(np.cos(start_angle),np.sin(start_angle))
                
                Comet.spawn(start_pos,direction,speed,"small")

        elif len(cometlist)<3:
            surface_size=DISPLAYSURF.get_size()
            start_pos=(random.randrange(surface_size[0]+1),random.randrange(surface_size[1]+1))
            start_angle=random.randrange(0,201)/100*np.pi
            direction=(np.cos(start_angle),np.sin(start_angle))
            speed=random.randrange(2,4)
            Comet.spawn(start_pos,direction,speed,"large") 
             


Comet.initial()

game=True
while game:

    front_x= playerPos[0]+ math.cos((ang-90)*(np.pi)/180)*18
    front_y= playerPos[1]+ math.sin((ang-90)*(np.pi)/180)*18
    frontPoint=(front_x,front_y)

    playerPos=translation(-accel*(playerPos[0]-frontPoint[0]),-accel*(playerPos[1]-frontPoint[1]),playerPos)

    DISPLAYSURF.fill(BLACK)
    rotimage = pygame.transform.rotate(player_image,-ang)
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

        ang-=2
        
    if keys[pygame.K_RIGHT]:

        ang+=2

    if keys[pygame.K_UP]:

        accel+=0.002
        if accel>0.2:
            accel=0.2

    if keys[pygame.K_DOWN]:

        accel-=0.01 #temporary, delete when done
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

    playerPos=wrap_around(playerPos)

    if shot1:
        killBullet=False
        while not spawnAssigned1:

            bulletPos1=frontPoint

            distance1=np.subtract(bulletPos1,playerPos)
            norm1=math.sqrt(distance1[0]**2 + distance1[1]**2)
            direction1=np.divide(distance1,norm1)*5
            rotation1 = pygame.transform.rotate(bullet_image,-ang)

            spawnAssigned1=True

        bulletPos1=np.add(bulletPos1,direction1)
        bulletPos1=wrap_around(bulletPos1)

        bullet_hitbox.center=bulletPos1
        rect1 = rotimage.get_rect(center=np.add(bulletPos1,(15,10)))
        
        pygame.draw.rect(DISPLAYSURF,GREEN,bullet_hitbox,1)
        DISPLAYSURF.blit(rotation1,rect1)

        for i in cometlist:
            if bullet_hitbox.colliderect(i.hitbox):
                killBullet=True
        if bulletCooldown1+4000<=pygame.time.get_ticks():
            killBullet=True

        if killBullet:
            shot1=False
            spawnAssigned1=False

    if shot2:
        killBullet=False
        while not spawnAssigned2:

            bulletPos2=frontPoint

            distance2=np.subtract(bulletPos2,playerPos)
            norm2=math.sqrt(distance2[0]**2 + distance2[1]**2)
            direction2=np.divide(distance2,norm2)*5
            rotation2 = pygame.transform.rotate(bullet_image,-ang)
            
            spawnAssigned2=True

        bulletPos2=np.add(bulletPos2,direction2)
        bulletPos2=wrap_around(bulletPos2)

        bullet_hitbox.center=bulletPos2
        rect2 = rotimage.get_rect(center=np.add(bulletPos2,(15,10)))
        
        pygame.draw.rect(DISPLAYSURF,GREEN,bullet_hitbox,1)
        DISPLAYSURF.blit(rotation2,rect2)

        for i in cometlist:
            if bullet_hitbox.colliderect(i.hitbox):
                killBullet=True
        if bulletCooldown2+4000<=pygame.time.get_ticks():
            killBullet=True

        if killBullet:
            shot2=False
            spawnAssigned2=False

    if shot3:
        killBullet=False
        while not spawnAssigned3:

            bulletPos3=frontPoint

            distance3=np.subtract(bulletPos3,playerPos)
            norm3=math.sqrt(distance3[0]**2 + distance3[1]**2)
            direction3=np.divide(distance3,norm3)*5
            rotation3 = pygame.transform.rotate(bullet_image,-ang)
            
            spawnAssigned3=True

        bulletPos3=np.add(bulletPos3,direction3)
        bulletPos3=wrap_around(bulletPos3)

        bullet_hitbox.center=bulletPos3
        rect3 = rotimage.get_rect(center=np.add(bulletPos3,(15,10)))
        
        pygame.draw.rect(DISPLAYSURF,GREEN,bullet_hitbox,1)
        DISPLAYSURF.blit(rotation3,rect3)

        for i in cometlist:
            if bullet_hitbox.colliderect(i.hitbox):
                killBullet=True
        if bulletCooldown3+4000<=pygame.time.get_ticks():
            killBullet=True

        if killBullet:
            shot3=False
            spawnAssigned3=False

    if shot4:
        killBullet=False
        while not spawnAssigned4:

            bulletPos4=frontPoint

            distance4=np.subtract(bulletPos4,playerPos)
            norm4=math.sqrt(distance4[0]**2 + distance4[1]**2)
            direction4=np.divide(distance4,norm4)*5
            rotation4 = pygame.transform.rotate(bullet_image,-ang)
            
            spawnAssigned4=True

        bulletPos4=np.add(bulletPos4,direction4)
        bulletPos4=wrap_around(bulletPos4)

        bullet_hitbox.center=bulletPos4
        rect4 = rotimage.get_rect(center=np.add(bulletPos4,(15,10)))
        
        pygame.draw.rect(DISPLAYSURF,GREEN,bullet_hitbox,1)
        DISPLAYSURF.blit(rotation4,rect4)

        for i in cometlist:
            if bullet_hitbox.colliderect(i.hitbox):
                killBullet=True
        if bulletCooldown4+4000<=pygame.time.get_ticks():
            killBullet=True

        if killBullet:
            shot4=False
            spawnAssigned4=False





    pygame.display.update()
    fpsClock.tick(FPS)