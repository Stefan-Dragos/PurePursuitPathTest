import pygame
from Curves import *
import time
import numpy as np

pygame.init()

pygame.display.set_caption("Bezier Spline Tester")
SCREEN = pygame.display.set_mode((600,600))

clock = pygame.time.Clock()
fps = 10

t = 0
speed = 0.05

QuinticPositions = []

quinticList = []

def displayPoints(screen, points):
    for i, p in enumerate(points):
        pygame.draw.circle(screen, (i * 35,50,50), p, 6)

run = True
startCurve = False
while run:
    clock.tick(fps)

    SCREEN.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(QuinticPositions) < 6:
                QuinticPositions.append(pygame.mouse.get_pos())
            print(f"1:  {QuinticPositions} ")
        if event.type == pygame.KEYDOWN:
            if startCurve:
                startCurve = False
                QuinticPositions.clear()
                quinticList.clear()
                print("RESET")
            else:
                print("START")
                startCurve = True

    if startCurve:
        QuinticCurve(QuinticPositions, t, SCREEN, (255,0,0), quinticList)

        if len(quinticList) > 2:
            pygame.draw.lines(SCREEN, (255,0,0), False, quinticList, 5)

        print(t)

        if t >= 1:

            print(round(1/speed) + 1)
            print(len(quinticList))

            pygame.display.flip()
            time.sleep(2)

            t = 0
            for p in quinticList:
                print(f"({p[0]}, {600 - p[1]}), ")
            quinticList.clear()
            
            print("--------RESET------------")
        else: 
            t += speed
    
    displayPoints(SCREEN, QuinticPositions)

    pygame.display.flip()

#-------------------------------------------------------

QuinticPositions = [[75,300], [150, 150], [200, 340], [300, 100], [440, 70], [480, 270]]

run = True
startCurve = False
while run:
    clock.tick(2)

    SCREEN.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            QuinticPositions[2] = pygame.mouse.get_pos()
            print(f"1:  {QuinticPositions} ")

    while t <= 1.0:
        QuinticCurve(QuinticPositions, t, SCREEN, (255,0,0), quinticList)
        SCREEN.fill((255,255,255))
        t += speed
        print(t)

    if len(quinticList) > 2:
        pygame.draw.lines(SCREEN, (255,0,0), False, quinticList, 5)


    if t >= 1:
        pygame.display.flip()

        t = 0
        for p in quinticList:
            print(f"({p[0]}, {600 - p[1]}), ")
        quinticList.clear()
        
        print("--------RESET------------")
    
    displayPoints(SCREEN, QuinticPositions)

    pygame.display.flip()

pygame.quit()