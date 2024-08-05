import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame
from scipy.interpolate import interp1d
from Curves import QuinticCurve
from BezierCircleIntersection import bezierCircleIntersections

import math
import numpy as np
import time

def add_line(path):
    for i in range(0, len(path)):
        plt.plot(path[i][0], path[i][1], '.', color='red', markersize=10)

    for j in range(0, (len(path)-1)):
        plt.plot([path[j][0], path[j+1][0]], [path[j][1], path[j+1][1]], color='b')
    

def add_complicated_line(path, lineStyle, lineColor, lineLabel):
    for i in range(0, len(path)):
        plt.plot(path[i][0], path[i][1], '.', color='red', markersize=10)
    
    for j in range(0, len(path)-1):
        if j == 0:
            print("label")
            plt.plot([path[j][0], path[j+1][0]], [path[j][1], path[j+1][1]], lineStyle, color=lineColor, label=lineLabel)
        else:
            plt.plot([path[j][0], path[j+1][0]], [path[j][1], path[j+1][1]], lineStyle, color=lineColor)

    plt.axis('scaled')


def highlight_points(points,pointColor):
    for point in points:
        plt.plot(point[0], point[1], '.', color=pointColor, markersize=10)


def draw_circle(x, y, r, circleColor, circleType):
    xs = []
    ys = []
    angles = np.arange(0, 2.2 * math.pi, 0.2)

    for angle in angles:
        xs.append(x + r * math.cos(angle))
        ys.append(y + r * math.sin(angle))

    plt.plot(xs, ys, circleType, color=circleColor)


def signum(num):
    if num >= 0:
        return 1
    else:
        return -1


def p2pDistance(p1, p2):
    return math.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


#path = [[30,30], [100, 100], [180, 350], [460, 555], [575, 375], [140, 430], [230, 200], [300, 395]]
path = [(93, 259), 
(116, 286),
(140, 304),
(165, 315),
(190, 323),
(216, 329),
(242, 334),
(268, 338),
(294, 341),
(319, 343),
(342, 343),
(364, 339),
(383, 332),
(399, 319),
(411, 301),
(418, 276),
(419, 245),
(413, 207),
(399, 164),
(376, 116),
(342, 65)]



def lineCircleIntersection(currentPos, pt1, pt2, lookAheadDist):
    currentX = currentPos[0]
    currentY = currentPos[1]
    x1 = pt1[0]
    y1 = pt1[1]
    x2 = pt2[0]
    y2 = pt2[1]

    x1Offset = pt1[0] - currentX
    y1Offset = pt1[1] - currentY
    x2Offset= pt2[0] - currentX
    y2Offset = pt2[1] - currentY

    intersectionFound = False

    dx = x2Offset - x1Offset
    dy = y2Offset - y1Offset
    dr = math.sqrt((dx**2) + (dy**2))

    det = x1Offset * y2Offset - x2Offset * y1Offset
    discriminant = (lookAheadDist**2) * (dr**2) - (det**2)

    if discriminant >= 0:

        solx1 = ((det * dy) + signum(dy) * dx * math.sqrt(discriminant)) / (dr**2)
        soly1 = ((-det * dx) + abs(dy) * math.sqrt(discriminant)) / (dr**2)
        solx2 = ((det * dy) - signum(dy) * dx * math.sqrt(discriminant)) / (dr**2)
        soly2 = ((-det * dx) - abs(dy) * math.sqrt(discriminant)) / (dr**2)

        sol1 = [solx1 + currentX, soly1 + currentY]
        sol2 = [solx2 + currentX, soly2 + currentY]

        minX = min(x1,x2)
        maxX = max(x1,x2)

        #---------------Visual------------------------
        draw_circle(currentX, currentY, lookAheadDist, 'pink', '-')

        if minX <= sol1[0] <= maxX:
            intersectionFound = True
            plt.plot(sol1[0], sol1[1], '.', color='orange', markersize=10)
            print("1 Valid")

        if minX <= sol2[0] <= maxX:
            intersectionFound = True
            plt.plot(sol2[0], sol2[1], '.', color='orange', markersize=10)
            print("2 Valid")


def goal_pt_search(path, currentPos, lookAheadDist, lastFoundIndex):

    goalPt = [None, None]

    currentX = currentPos[0]
    currentY = currentPos[1]

    intersectionFound = False

    start = lastFoundIndex
    for i in range(start, len(path) - 1):

        print(f"-----------{i}--------------")

        x1 = path[i][0]
        y1 = path[i][1]
        x2 = path[i+1][0]
        y2 = path[i+1][1]

        x1Offset = x1 - currentX
        y1Offset = y1 - currentY
        x2Offset= x2 - currentX
        y2Offset = y2 - currentY

        dx = x2Offset - x1Offset
        dy = y2Offset - y1Offset
        dr = math.sqrt((dx**2) + (dy**2))

        det = x1Offset * y2Offset - x2Offset * y1Offset
        discriminant = (lookAheadDist**2) * (dr**2) - (det**2)

        if discriminant >= 0:

            print("Found solutions")

            solx1 = ((det * dy) + signum(dy) * dx * math.sqrt(discriminant)) / (dr**2)
            soly1 = ((-det * dx) + abs(dy) * math.sqrt(discriminant)) / (dr**2)
            solx2 = ((det * dy) - signum(dy) * dx * math.sqrt(discriminant)) / (dr**2)
            soly2 = ((-det * dx) - abs(dy) * math.sqrt(discriminant)) / (dr**2)

            sol1 = [solx1 + currentX, soly1 + currentY]
            sol2 = [solx2 + currentX, soly2 + currentY]

            minX = min(x1,x2)
            maxX = max(x1,x2)

            #---------------Visual------------------------
            #draw_circle(currentX, currentY, lookAheadDist, 'pink', '-')
            #---------------------------------------------

            int1Found = False
            int2Found = False

            if minX <= sol1[0] <= maxX:
                int1Found = True
                #plt.plot(sol1[0], sol1[1], '.', color='orange', markersize=10)
                pygame.draw.circle(SCREEN, (215,90,0), (sol1[0], 600-sol1[1]), 5)
                print(f"sol1 {sol1}")

            if minX <= sol2[0] <= maxX:
                int2Found = True
                #plt.plot(sol2[0], sol2[1], '.', color='orange', markersize=10)
                pygame.draw.circle(SCREEN, (215,90,0), (sol2[0], 600-sol2[1]), 5)
                print(f"sol2 {sol2}")

            #if two intersections are found on the line, choose the point closest to the end of the line
            if int1Found and int2Found:
                if p2pDistance(sol1, path[i+1]) < p2pDistance(sol2, path[i+1]):
                    goalPt = sol1
                else:
                    goalPt = sol2
            elif int1Found:
                goalPt = sol1           #If only one intersection, choose
            elif int2Found:             #the one that was found
                goalPt = sol2
            else:
                goalPt = path[lastFoundIndex]   #go to last known path point if no intersections are found

            print(f"index {lastFoundIndex}")

            #if the second to last path point has been passed, and the robot distance to the endpoint is shorter than
            #the chosen goal point, then set the goalpoint to the last point in the path
            if (lastFoundIndex == len(path)-2) and (p2pDistance(goalPt, path[i+1]) > p2pDistance(currentPos, path[i+1])):
                goalPt = path[i+1]

            #if we are farther from the line end than the goal point, then we know the goalPoint is between us and the end
            #and therefore is the best choice
            if p2pDistance(goalPt, path[i+1]) < p2pDistance(currentPos, path[i+1]):
                lastFoundIndex = i
                print(f"Found goal at {i}  |  goalPtDist:{p2pDistance(goalPt, path[i+1])}  currentPos:{p2pDistance(currentPos, path[i+1])}")
                break
            #if we are closer the end of the line than the goal point, we know we are between the point and the end
            #so the goal point is behind us, and we continue searching in the next line for a better point
            else:
                print(f"CONTINUE SEARCH   |  goalPtDist:{p2pDistance(goalPt, path[i+1])}  currentPos:{p2pDistance(currentPos, path[i+1])}")
                lastFoundIndex = i+1
                
        #if no solutions are found on the line, we know it was passed
        #lastFoundIndex += 1

    if goalPt == [None, None]:
        print("OFF TRACK")
        return path[lastFoundIndex], lastFoundIndex

    print(f"goalPoint: {goalPt}")
    print("------GOAL_EXIT-------")
    return goalPt, lastFoundIndex


def move_to_point(goal, pos, heading):
    KpAng = 0.5
    KpLin = 0.5

    #angular stuff
    absAngleTarget = math.atan2(goal[1] - pos[1], goal[0] - pos[0]) * (180/pi)

    if absAngleTarget < 0:
        absAngleTarget += 360

    turnError = (absAngleTarget - heading) % 360

    if turnError > 180 or turnError < -180:
        turnError = -1 * signum(turnError) * (360 - abs(turnError))

    #linear stuff
    linearError = p2pDistance(goal, pos)

    linearVel = linearError * KpLin
    turnVel = turnError * KpAng

    linearVel = np.clip(linearVel, 0, 15)
    turnVel = np.clip(turnVel, -30, 30)

    if linearError < 0.1:
        turnVel = 0

    return turnVel, linearVel

#-------------------------------

pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((600,600))

QuinticPositions = [[75, 300], [155, 100], [230, 500], [375, 350], [450, 130], [200, 250]]
quinticList = []

t = 0

for i in range(501):
    QuinticCurve(QuinticPositions, t, SCREEN, (255,0,0), quinticList)
    t += 0.002

currentPos = [quinticList[0][0], quinticList[0][1]]
currentHeading = 0
lookAheadDis = 35

angVel = 0
linVel = 0

indexPass = 0
pi = np.pi


while True:

    CLOCK.tick(2)

    SCREEN.fill((0,0,0))

    pygame.event.get()

    for i in range(0, len(quinticList) - 1):
        #pygame.draw.circle(SCREEN, (255,0,0), (path[i][0], 600 - path[i][1]), 5)
        pygame.draw.line(SCREEN, (0,255,0), (quinticList[i][0], 600 - quinticList[i][1]),
                          (quinticList[i+1][0], 600 - quinticList[i+1][1]), width=3)

    pygame.draw.circle(SCREEN, (255,0,0), (quinticList[-1][0], 600 - quinticList[-1][1]), 5)
    #add_complicated_line(path, '-', 'green', "LineTest")

    #draw_circle(currentPos[0], currentPos[1], 1, 'yellow', '-')
    intersections = bezierCircleIntersections(quinticList, currentPos, lookAheadDis)

    for i in intersections:
        pygame.draw.circle(SCREEN, (0,0,255), [quinticList[i][0], 600 - quinticList[i][1]], 6)

    if len(intersections) > 0:
        goal = quinticList[intersections[-1]]

    print(f"GOAL: {goal}")

    pygame.draw.circle(SCREEN, (190,25,100), [currentPos[0], 600 - currentPos[1]], 10)
    pygame.draw.line(SCREEN, (255, 0, 255), [currentPos[0], 600 - currentPos[1]], 
                     [currentPos[0] + 15 * math.cos(currentHeading * (pi/180)), 600 - (currentPos[1] + 15 * math.sin(currentHeading * (pi/180)))], 4)

    print(f"HEADING: {currentHeading}")
    pygame.draw.circle(SCREEN, (100,25,100), [currentPos[0], 600 - currentPos[1]], lookAheadDis, width=2)
    pygame.draw.circle(SCREEN, (0,0,255), [goal[0], 600 - goal[1]], 6)

    turnVel, linearVel = move_to_point(goal, currentPos, currentHeading)

    print(f"turn {turnVel}  forward{linearVel}")

    currentHeading += turnVel
    currentHeading = currentHeading % 360
    currentPos[0] += math.cos(currentHeading * (pi/180)) * linearVel
    currentPos[1] += math.sin(currentHeading * (pi/180)) * linearVel

    print(f"POS: {currentPos}")

    pygame.display.flip()

    
    #plt.show()


#plt.axis('scaled')
plt.legend()
plt.show()