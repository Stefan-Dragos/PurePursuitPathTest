#visuals
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame

#specifics
from scipy.interpolate import interp1d
from BezierCurves.Curves import QuinticCurve

#generics
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
                print("Reverting to last known point...")
                goalPt = path[lastFoundIndex]   #go to last known path point if no intersections are found

            print(f"index {lastFoundIndex}")

            #if the second to last path point has been passed, and the robot distance to the endpoint is shorter than
            #the chosen goal point => we are between goalPt and end, then set the goalpoint to the last point in the path
            if (lastFoundIndex == len(path)-2) and (p2pDistance(goalPt, path[i+1]) > p2pDistance(currentPos, path[i+1])):
                goalPt = path[-1]

            #if we are farther from the line end than the goal point is, then we know the goalPoint is between us and the end
            #and therefore is the best choice.
            #If the goalPt is pt i (most likely the first point searched), continue searching as to not get
            #softlocked at i : goalpt is i and i will be returned, causing the next iteration to produce the same result
            if (p2pDistance(goalPt, path[i+1]) < p2pDistance(currentPos, path[i+1])) and not goalPt == path[i]:
                lastFoundIndex = i
                print(f"Found goal at {i}  |  goalPtDist:{p2pDistance(goalPt, path[i+1])}  currentPos:{p2pDistance(currentPos, path[i+1])}")
                break
            #if we are closer to end of the line than the goal point, we know we are between the point and the end
            #so the goal point is behind us, and we continue searching in the next line for a better point
            #also continue searching if we were about to be softlocked to get a new goalpt
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

#-----------------------------------VISUAL----------------------------
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((600,600))

def displayPoints(screen, points):
    for i, p in enumerate(points):
        pygame.draw.circle(screen, (i * 35,50,50), p, 6)
#--------------------------------------PATHING------------------------------

ControlPoints = []

creating = True
while creating:

    CLOCK.tick(2)
    SCREEN.fill((255,255,255))
    for event in pygame.event.get():

        if (event.type == pygame.QUIT or event.type == 768) and len(ControlPoints) == 6:
            creating = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(ControlPoints) < 6:
                ControlPoints.append(pygame.mouse.get_pos())

    displayPoints(SCREEN, ControlPoints)
    print(ControlPoints)

    pygame.display.flip()


ControlPoints = [[ControlPoints[i][0], 600 - ControlPoints[i][1]] for i in range(len(ControlPoints))]

QuinticList = []

t = 0
speed = 0.05

#creates the quintic curve
for i in range(round(1/speed) + 1):
    QuinticCurve(ControlPoints, t, SCREEN, (255,0,0), QuinticList)
    t += speed

path = [(84, 295),
(93, 305),
(101, 313),
(108, 319),
(115, 323),
(121, 326),
(127, 328),
(133, 329),
(139, 330),
(145, 329),
(152, 329),
(158, 328),
(165, 328),
(172, 328),
(180, 329),
(189, 330),
(198, 332),
(208, 336),
(220, 341),
(232, 347),
(246, 356),
(246, 356),
(259, 366),
(271, 375),
(281, 385),
(290, 394),
(298, 404),
(304, 413),
(310, 422),
(314, 430),
(318, 438),
(322, 446),
(326, 453),
(329, 460),
(332, 466),
(336, 471),
(340, 476),
(345, 480),
(350, 483),
(356, 485),
(364, 486),
(372, 486),
(372, 486),
(381, 485),
(389, 485),
(397, 483),
(405, 482),
(411, 480),
(417, 477),
(423, 474),
(428, 471),
(432, 466),
(436, 461),
(439, 454),
(441, 447),
(442, 439),
(443, 430),
(443, 419),
(442, 407),
(440, 394),
(437, 380),
(433, 364),
(429, 346),
(429, 346),
(423, 328),
(416, 311),
(407, 295),
(397, 280),
(386, 265),
(375, 251),
(363, 238),
(350, 226),
(338, 214),
(326, 203),
(315, 192),
(304, 183),
(294, 173),
(286, 164),
(279, 156),
(273, 148),
(270, 140),
(268, 133),
(269, 126),
(273, 119),
(273, 119),
(279, 113),
(286, 109),
(295, 107),
(304, 106),
(315, 107),
(327, 109),
(340, 112),
(354, 116),
(368, 121),
(382, 127),
(398, 134),
(413, 141),
(428, 150),
(443, 158),
(459, 167),
(474, 177),
(488, 186),
(502, 196),
(515, 205),
(528, 215)]
#path = QuinticList
print(path)

#-------------------------------VARIABLES--------------------------
currentPos = [path[0][0], path[0][1]]
currentHeading = 0
lookAheadDis = 35

angVel = 0
linVel = 0

indexPass = 0
pi = np.pi

time.sleep(3)

run = True
while run:

    CLOCK.tick(3)

    SCREEN.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for i in range(0, len(path) - 1):
        pygame.draw.circle(SCREEN, (255,0,0), (path[i][0], 600 - path[i][1]), 5)
        pygame.draw.line(SCREEN, (0,255,0), (path[i][0], 600 - path[i][1]), (path[i+1][0], 600 - path[i+1][1]), width=3)

    pygame.draw.circle(SCREEN, (255,0,0), (path[-1][0], 600 - path[-1][1]), 5)
    #add_complicated_line(path, '-', 'green', "LineTest")

    #draw_circle(currentPos[0], currentPos[1], 1, 'yellow', '-')
    goal, indexPass = goal_pt_search(path, currentPos, lookAheadDis, indexPass)

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
    currentPos[0] += math.cos(currentHeading * (pi/180)) * linearVel
    currentPos[1] += math.sin(currentHeading * (pi/180)) * linearVel

    pygame.display.flip()

    print("----------------------------------------------------------------")
    #plt.show()

pygame.quit()