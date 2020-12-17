import pyRender as pr
import objectReader as obr

import math as math

import sys

import pygame
from pygame.locals import *
from pygame import gfxdraw
from pygame import Surface
from pygame import key

pygame.init()

keys = []

blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

pr.init((640, 480), screen)



# Game loop.
while True:
    screen.fill((255, 255, 255))

    keys = pygame.key.get_pressed()  #checking pressed keys
    if keys[pygame.K_RIGHT]:
        pr.rotate(0, .04, 0)
    if keys[pygame.K_LEFT]:
        pr.rotate(0, -.04, 0)
    if keys[pygame.K_DOWN]:
        pr.rotate(-.04, 0, 0)
    if keys[pygame.K_UP]:
       pr.rotate(.04, 0, 0)
    if keys[pygame.K_w]:
        pr.moveCamera(0, .5, 0)
    if keys[pygame.K_s]:
        pr.moveCamera(0, -.5, 0)
    if keys[pygame.K_a]:
        pr.moveCamera(-.5, 0, 0)
    if keys[pygame.K_d]:
        pr.moveCamera(.5, 0, 0)
    if keys[pygame.K_e]:
        pr.moveCamera(0, 0, .5)
    if keys[pygame.K_q]:
        pr.moveCamera(0, 0, -.5)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        

    # Update.
    # Draw.
    
    pr.drawObject((0, 0, 10), 1, "room", (0, 0, 255))
    pr.drawObject((0, 0, 25), 1, "wall_x_door", red)
    pr.drawObject((-4, 0, 21), 1, "wall_z_door", red)

    pygame.display.flip()
    fpsClock.tick(fps)
