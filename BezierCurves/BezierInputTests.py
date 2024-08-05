import pygame
from Curves import CubicCurve
import time
import numpy as np

pygame.init()

pygame.display.set_caption("Bezier Spline Tester")
SCREEN = pygame.display.set_mode((600,600))

clock = pygame.time.Clock()
fps = 10

t = 0
speed = 0.05

LinearPositions = [[100, 500], [400, 200]]
#CubicPositions = [[100, 100], [400, 500], [500, 500], [500, 100]]
CubicPositions = []
CubicPositions2 = []

cubicCurveList = []
cubicCurveList2 = []

def displayPoints(screen, points):
    for i, p in enumerate(points):
        pygame.draw.circle(screen, (i * 75,50,50), p, 6)

run = True
startCurve = False
while run:
    clock.tick(4)

    SCREEN.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(CubicPositions) < 4:
                CubicPositions.append(pygame.mouse.get_pos())
            elif len(CubicPositions2) < 3:
                CubicPositions2.append(pygame.mouse.get_pos())
            print(f"1:  {CubicPositions}  | 2: {CubicPositions2}")
        if event.type == pygame.KEYDOWN:
            if startCurve:
                startCurve = False
                CubicPositions.clear()
                cubicCurveList.clear()
                CubicPositions2.clear()
                cubicCurveList2.clear()
                print("RESET")
            else:
                print("START")

                tension = 0.5

                cubicCurveList.append(CubicPositions[0])
                cubicCurveList2.append(CubicPositions2[0])
                CubicPositions2.insert(0, CubicPositions[-1])
                startCurve = True

    if startCurve:
        #LinearCurve(LinearPositions, t, SCREEN, (255, 0, 0))
        CubicCurve(CubicPositions, t, SCREEN, (255,0,0), cubicCurveList, (0,255,0), (0,0,255))
        CubicCurve(CubicPositions2, t, SCREEN, (255,0,0), cubicCurveList2, (0,255,0), (0,0,255))

        #for point in LinearPositions:
            #pygame.draw.circle(SCREEN, (0,0,0), point, 2)

        if len(cubicCurveList) > 2:
            pygame.draw.lines(SCREEN, (255,0,0), False, cubicCurveList, 5)
        if len(cubicCurveList2) > 2:
            pygame.draw.lines(SCREEN, (255,0,0), False, cubicCurveList2, 5)

        print(t)

        if t >= 1:
            pygame.display.flip()
            time.sleep(2)

            t = 0
            for p in cubicCurveList:
                print(f"({p[0]}, {600 - p[1]}), ")
            cubicCurveList.clear()
            #cubicCurveList.append(CubicPositions[0])

            print()

            for p in cubicCurveList2:
                print(f"({p[0]}, {600 - p[1]}), ")
            cubicCurveList2.clear()
            #cubicCurveList2.append(CubicPositions2[0])
            print("--------RESET------------")
        else: 
            t += speed
    
    displayPoints(SCREEN, CubicPositions)
    displayPoints(SCREEN, CubicPositions2)
    pygame.display.flip()

pygame.quit()