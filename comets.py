import pygame, sys
import numpy as np
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

playerPos=(50,50)

while True:

    DISPLAYSURF.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerPos[0]-=2
    if keys[pygame.K_RIGHT]:
        playerPos[0]+=2
    if keys[pygame.K_UP]:
        playerPos[1]-=2
    if keys[pygame.K_DOWN]:
        playerPos[1]+=2
    if keys[pygame.K_ESCAPE]:
        pygame.quit()



    pygame.display.update()
    fpsClock.tick(FPS)