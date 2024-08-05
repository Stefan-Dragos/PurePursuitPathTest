import pygame

def LinearCurve(positions, t, screen, color, trigger=True):
    p0x = (1-t) * positions[0][0]
    p0y = (1-t) * positions[0][1]

    p1x = t * positions[1][0]
    p1y = t * positions[1][1]

    curve = (p0x + p1x, p0y + p1y)

    if trigger == True:
        pygame.draw.line(screen, (0,0,0), (positions[0][0], positions[0][1]),
                          (positions[1][0], positions[1][1]), 1)
        pygame.draw.line(screen, (color), (positions[0][0], positions[0][1]), 
                         (int(curve[0]), int(curve[1])), 2)
        pygame.draw.circle(screen, (color), (int(curve[0]), int(curve[1])), 8)
    else:
        pygame.draw.circle(screen, (color), (int(curve[0]), int(curve[1])), 8)
    
    return [int(curve[0]), int(curve[1])]
    

def CubicCurve(positions, t, screen, color, curveList, green=None, blue=None, trigger=True):
    p0x = pow((1-t), 3) * positions[0][0]
    p0y = pow((1-t), 3) * positions[0][1]

    p1x = 3 * pow((1-t), 2) * t * positions[1][0]
    p1y = 3 * pow((1-t), 2) * t * positions[1][1]

    p2x = 3 * (1-t) * pow(t,2) * positions[2][0]
    p2y = 3 * (1-t) * pow(t,2) * positions[2][1]

    p3x = pow(t,3) * positions[3][0]
    p3y = pow(t,3) * positions[3][1]

    curve = (p0x + p1x + p2x + p3x, p0y + p1y + p2y + p3y)

    
    pygame.draw.line(screen, (0,0,0), (positions[0][0], positions[0][1]),
                          (positions[1][0], positions[1][1]), 1)
    pygame.draw.line(screen, (0,0,0), (positions[1][0], positions[1][1]),
                          (positions[2][0], positions[2][1]), 1)
    pygame.draw.line(screen, (0,0,0), (positions[2][0], positions[2][1]),
                          (positions[3][0], positions[3][1]), 1)
    
    line1 = [positions[0], positions[1]]
    line2 = [positions[1], positions[2]]
    line3 = [positions[2], positions[3]]

    a = LinearCurve(line1, t, screen, green, False)
    b = LinearCurve(line2, t, screen, green, False)
    c = LinearCurve(line3, t, screen, green, False)

    pos1 = [a[0], a[1]]
    pos2 = [b[0], b[1]]
    pos3 = [c[0], c[1]]

    interline1 = [pos1, pos2]
    interline2 = [pos2, pos3]

    start = LinearCurve(interline1, t, screen, blue, False)
    end = LinearCurve(interline2, t, screen, blue, False)

    pygame.draw.line(screen, green, a, b, 2)
    pygame.draw.line(screen, green, b, c, 2)
    pygame.draw.line(screen, blue, start, end, 2)
    

    pygame.draw.circle(screen, color, (int(curve[0]), int(curve[1])), 8)
    curveList.append((int(curve[0]), int(curve[1])))


def QuinticCurve(positions, t, screen, color, curveList):

    curve = (
        pow((1-t), 5) * positions[0][0]  +  5 * t * pow((1-t), 4) * positions[1][0]  +  10 * pow(t,2) * pow((1-t),3) * positions[2][0]
        +  10 * pow(t,3) * pow((1-t), 2) * positions[3][0]  +  5 * pow(t,4) * (1-t) * positions[4][0]  +  pow(t,5) * positions[5][0]
    ,
        pow((1-t), 5) * positions[0][1]  +  5 * t * pow((1-t), 4) * positions[1][1]  +  10 * pow(t,2) * pow((1-t),3) * positions[2][1]
        +  10 * pow(t,3) * pow((1-t), 2) * positions[3][1]  +  5 * pow(t,4) * (1-t) * positions[4][1]  +  pow(t,5) * positions[5][1]
    )

    if screen != None:
        pygame.draw.circle(screen, color, (int(curve[0]), int(curve[1])), 8)
    curveList.append((int(curve[0]), int(curve[1])))


def CatmullRom(positions, t, screen, color, curveList, tension=0.5):
    for p in range(1, len(positions) - 2):
        
        #print("Generating CMR...")

        #getting the x value

        xp0 = positions[p-1][0]  #control/tangent point
        xv1 = positions[p][0]    #curve vertex
        xv2 = positions[p+1][0]  #curve vertex
        xp3 = positions[p+2][0]  #control/tangent point

        s = 2 * tension
        xdv1 = (xv2 - xp0) / s
        xdv2 = (xp3 - xv1) / s

        xc0 = 2 * pow(t,3) - 3 * pow(t,2) + 1
        xc1 = pow(t,3) - 2 * pow(t,2) + t
        xc2 = -2 * pow(t,3) + 3 * pow(t,2)
        xc3 = pow(t,3) - pow(t,2)

        x = round(xc0 * xv1 + xc1 * xdv1 + xc2 * xv2 + xc3 * xdv2)

        #getting the y value

        yp0 = positions[p-1][1]  #control/tangent point
        yv1 = positions[p][1]    #curve vertex
        yv2 = positions[p+1][1]  #curve vertex
        yp3 = positions[p+2][1]  #control/tangent point

        #s = 2 * tension
        ydv1 = (yv2 - yp0) / s
        ydv2 = (yp3 - yv1) / s

        yc0 = 2 * pow(t,3) - 3 * pow(t,2) + 1
        yc1 = pow(t,3) - 2 * pow(t,2) + t
        yc2 = -2 * pow(t,3) + 3 * pow(t,2)
        yc3 = pow(t,3) - pow(t,2)

        y = round(yc0 * yv1 + yc1 * ydv1 + yc2 * yv2 + yc3 * ydv2)

        if screen != None:
            pygame.draw.circle(screen, color, (x, y), 8)

        curveList.append([x,y])


def CMRPointsToCoordinates(controls, curveList):

    updatedPoints = []

    polyNum = len(controls) - 3  #gives the us the number of polynomials in the spline, know how many indices to skip

    #iterate through number of points in each polynomial
    for i in range(polyNum):
        for j in range(round(len(curveList) / polyNum)):
            updatedPoints.append(curveList[(j * polyNum) + i])

    return updatedPoints
        

class QuinticBezier:

    def __init__(self, controlPoints, speed):
        self.controlPoints = controlPoints
        self.t = 0
        self.bezierPoints = []
        self.speed = speed

        for i in range(round(1/self.speed) + 1):
            QuinticCurve(self.controlPoints, self.t, None, None, self.bezierPoints)
            self.t += self.speed


    def getStart(self):
        return self.controlPoints[0]
    
    def updatePoints(self):
        self.t = 0
        self.bezierPoints.clear()

        for i in range(round(1/self.speed) + 1):
            QuinticCurve(self.controlPoints, self.t, None, None, self.bezierPoints)
            self.t += self.speed


class CMR:

    def __init__(self, controlPoints, speed=0.1, tension=0.5):
        self.controlPoints = controlPoints
        self.t = 0
        self.bezierPoints = []
        self.speed = speed
        self.tension = tension

        for i in range(round(1/self.speed) + 1):
            CatmullRom(self.controlPoints, self.t, None, None, self.bezierPoints, self.tension)
            self.t += self.speed

        self.bezierPoints = CMRPointsToCoordinates(self.controlPoints, self.bezierPoints)

    def getStart(self):
        return self.controlPoints[0]
    
    def updatePoints(self):
        self.t = 0
        self.bezierPoints.clear()

        for i in range(round(1/self.speed) + 1):
            CatmullRom(self.controlPoints, self.t, None, None, self.bezierPoints, self.tension)
            self.t += self.speed

        self.bezierPoints = CMRPointsToCoordinates(self.controlPoints, self.bezierPoints)