import pygame
from Curves import QuinticCurve
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import sys

pygame.init()

pygame.display.set_caption("Bezier Spline Tester")
SCREEN = pygame.display.set_mode((600,600))

clock = pygame.time.Clock()
fps = 10

t = 0
speed = 0.05

#--------------------------------------

QuinticPositions = []
for i in range(6):
    QuinticPositions.append([np.random.randint(i * 100, (i+1) * 100), np.random.randint(50, 550)])

QuinticPositions = [[75, 300], [155, 100], [230, 500], [375, 350], [450, 130], [200, 250]]

quinticList = []
LUT = {}  #associates t value with a point in quinticList

def displayPoints(screen, points):
    for i, p in enumerate(points):
        pygame.draw.circle(screen, (i * 35,50,50), p, 6)


#creates the quintic curve
for i in range(101):
    QuinticCurve(QuinticPositions, t, SCREEN, (255,0,0), quinticList)
    t += 0.01


def p2pDistance(p1, p2):
    return math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))


def singleBezierCircleIntersection(bezierList, circleCenter, r):
    lowestDist = 100000   #save the lowest distance found
    index = -1            #save the index of the bezier point

    for i, p in enumerate(bezierList):
        #subtract radius from distance of point to circle center
        dist = abs(p2pDistance(p, circleCenter) - r)   #the lower this is to 0, the closer the point is to the cicle
        print(f"Index {i}  |  {dist}")
        #if the point is closer to the radius, save its index
        if dist < lowestDist:
            lowestDist = dist
            index = i

    return index, lowestDist


def closestMinIntersection(bezierList, start, circleCenter, r):
    #finds the closest local min to start

    minDistance = 100000
    index = -1
    pd2 = minDistance
    if start > 2:
        pd2 = abs(p2pDistance(bezierList[start-2], circleCenter) - r)
    pd1 = minDistance
    if start > 2:
        pd1 = abs(p2pDistance(bezierList[start-1], circleCenter) - r)

    slice = bezierList[start:]
    epsilon = 10000

    #checks if pd1 is a min
    for i, p in enumerate(slice):
        dist = abs(p2pDistance(circleCenter, p) - r)
        print(f"{pd2}  {pd1}  {dist}")
        if pd1 < pd2 and pd1 < dist and pd1 < epsilon:
            index = i - 1
            break

        minDistance = min(dist, minDistance)
        pd2 = pd1
        pd1 = dist

    return start + index, minDistance


def bezierCircleIntersections(bezierList, circleCenter, r):
    start = 0  #keeps track of point to find closest minima to
    intersections = []
    index = 1

    while True:
        print(f"Start:{start}")
        #get the closest minimum to start
        index = closestMinIntersection(bezierList, start, circleCenter, r)[0]   #a tuple (index, dist) is retured, so get only index
        #minimum not found if index is less than the start 
        #OR if index is positive yet equal to the start
        print(f"Index: {index}")
        if (index < start or (index > 0 and index == start - 1)):
            break
        intersections.append(index)  #add the found intersection
        start = index + 2        #start is increased by two to prevent using minimum in checking future minima

    print(intersections)

    distances = []

    minDist = 10000
    for i in intersections:
        dist = abs(p2pDistance(bezierList[i], circleCenter) - r)
        minDist = min(dist, minDist)
        distances.append(dist)

    tolerance = 3
    
    removed = 0  #decrease index whenever removing an element
    for j in range(len(intersections)):
        print(f"{j} | {distances[j]}")
        if distances[j] > (minDist + tolerance):
            intersections.pop(j - removed)
            removed +=1

    return intersections



center = (262.15,235.19)
radius = 35

intersection, dist = singleBezierCircleIntersection(quinticList, center, radius)
intersections= bezierCircleIntersections(quinticList, center, radius)
print(intersections)

plt.plot([quinticList[i][0] for i in range(len(quinticList))],
         [quinticList[i][1] for i in range(len(quinticList))], color="green")
plt.plot([radius * math.cos(0.1 * i * math.pi) + center[0] for i in range(21)], 
         [radius * math.sin(0.1 * i * math.pi) + center[1] for i in range(21)], color="red")

for i in intersections:
    print("Point plot")
    plt.plot([quinticList[i][0], quinticList[i][0]+1], [quinticList[i][1], quinticList[i][1]+1], color="blue", markersize=50)

plt.axis('scaled')
plt.show()

run = False
startCurve = False
while run:
    clock.tick(2)

    SCREEN.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if len(quinticList) > 2:
        pygame.draw.lines(SCREEN, (255,0,0), False, quinticList, 5)

    pygame.draw.circle(SCREEN, (0,0,255), center, radius, 3)

    for i in intersections:
        pygame.draw.circle(SCREEN, (0,255,0), quinticList[i], 3)


    #print("---------LUT----------")
    #print(LUT)
    #print(LUT[1])

    #for p in quinticList:
        #print(f"({p[0]}, {600 - p[1]}), ")

    displayPoints(SCREEN, QuinticPositions)

    pygame.display.flip()
    #print("--------RESET------------")


pygame.quit()