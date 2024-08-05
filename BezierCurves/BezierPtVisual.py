import pygame
from Curves import *
import time
import numpy as np
import math

def p2pDistance(p1, p2):
    return math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))


pygame.init()

pygame.display.set_caption("Bezier Spline Tester")
SCREEN = pygame.display.set_mode((600,600))

clock = pygame.time.Clock()
fps = 10

t = 0
speed = 0.05


BezierControls = [[100,300], [175, 475], [235, 220], [375, 100], [280, 300], [500, 285], [425,425], [300,300]]
BezierPoints = []

tension = 0.5

#BezierControls = [BezierControls[1],
                      #np.add(BezierControls[1], np.divide(np.subtract(BezierControls[2], BezierControls[0]), 6 * tension)),
                      #np.subtract(BezierControls[2], np.divide(np.subtract(BezierControls[3], BezierControls[1]), 6 * tension)),
                      #BezierControls[2]]


def displayPoints(points, screen, color):
    for i, p in enumerate(points):
        pygame.draw.circle(screen, color, p, 6)


def handlePointHighlight(mousePos):
    for i, p in enumerate(BezierControls):
        if p2pDistance(p, mousePos) < 10:
            return True, i
    return False, -1

highlightedPoint = False
movingPointIndex = -1

printTimer = 0
run = True
startCurve = False

while run:
    clock.tick(5)

    SCREEN.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not highlightedPoint:
                highlightedPoint, movingPointIndex = handlePointHighlight(pygame.mouse.get_pos())
            else:
                BezierControls[movingPointIndex] = pygame.mouse.get_pos()
                highlightedPoint = False

    tension = 0.5

    for i in range(round(1/speed) + 1):
        CatmullRom(BezierControls, t, SCREEN, (255,0,0), BezierPoints, tension)
        t += speed
    
    BezierPoints = CMRPointsToCoordinates(BezierControls, BezierPoints)
        
    #CubicCurve(BezierControls, t, SCREEN, (255,0,0), BezierPoints)


    if len(BezierPoints) > 2:
        pygame.draw.lines(SCREEN, (255,0,0), False, BezierPoints, 5)
        #displayPoints(BezierPoints, SCREEN, (0,255,0))
        pygame.draw.line(SCREEN, (0,0,0), BezierControls[0], BezierPoints[0], 5)
        pygame.draw.line(SCREEN, (0,0,0), BezierControls[-1], BezierPoints[-1], 5)

    displayPoints(BezierControls, SCREEN, (0,0,255))
    if highlightedPoint:
        pygame.draw.circle(SCREEN, (0,255,0), BezierControls[movingPointIndex], 7)


    t = 0
    if printTimer > 25:
        print("PRINT")
        for p in BezierPoints:
            print(f"({p[0]}, {600 - p[1]}), ")
        printTimer = 0
    else:
        printTimer += 1
    BezierPoints.clear()

    print(printTimer)

    pygame.display.flip()   #flip before clearing point list to render all points


pygame.quit()