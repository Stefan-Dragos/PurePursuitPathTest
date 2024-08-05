import tkinter as tk
from tkinter import ttk

import math
import numpy as np

from Curves import *


HermiteCurves = [QuinticBezier([[100,300], [200,150], [250, 250], [300, 450], [445, 325], [375, 460]], 0.05),
                 QuinticBezier([[150,300], [250,150], [300, 250], [350, 450], [495, 325], [415, 460]], 0.05)]

isMovingPoint = False
movePoint = [None, None]  #keep track of curve index and point index in that curve 

addingCurve = False
pointsToAdd = -1
controlPointsAdded = []
curveType = ""
speed = 0.1


def p2pDistance(p1, p2):
    return math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))


def handlePointClick(mouseX, mouseY, r):

    global isMovingPoint
    global movePoint

    if not isMovingPoint:
        for i, curve in enumerate(HermiteCurves):
            for j, p in enumerate(curve.controlPoints):
                if p2pDistance([mouseX, mouseY], p) <= r:
                    movePoint = [i,j]
                    isMovingPoint = True
    else:
        HermiteCurves[movePoint[0]].controlPoints[movePoint[1]] = [mouseX, mouseY]
        isMovingPoint = False


def handleCurveCreation(x,y):
    global controlPointsAdded
    global pointsToAdd
    global curveType
    global speed
    global addingCurve
    global HermiteCurves

    #handle curve creation if a curve is being added
    if addingCurve:
        controlPointsAdded.append([x,y])
        pointsToAdd -= 1
        if pointsToAdd == 0:
            if curveType == "quintic":
                ctrlPts = controlPointsAdded.copy()    #have to copy it to remove alias (when control points are cleared, also cleared inside curve obj)
                HermiteCurves.append(QuinticBezier(ctrlPts, speed))

                addingCurve = False
                controlPointsAdded.clear()
            elif curveType == "cmr":
                ctrlPts = controlPointsAdded.copy()
                HermiteCurves.append(CMR(ctrlPts, speed, 0.5))
                print("----------------added cmr-----------------------")
                print(HermiteCurves[-1].controlPoints)
                addingCurve = False
                controlPointsAdded.clear()


def drawLines(bezierPoints, canv, color, width):
    canv.create_line(np.ndarray.flatten(np.array(bezierPoints)).tolist(), fill=color, width=width)


def drawPoints(controlPoints, canv, color, r):
    for p in controlPoints:
        canv.create_oval(p[0] - r, p[1] - r, p[0] + r, p[1] + r, fill=color)


window = tk.Tk()
window.title("Pathing Generator")
window.geometry("800x600")

#canvas for drawing field and curves
canvas = tk.Canvas(master=window, height=500, width=500, bg="grey")
canvas.place(x=15, y=15, anchor="nw")

#frame for editing specific curves
editorFrame = ttk.Frame(master=window, height=500, width=200)
EditorTitle = ttk.Label(master=editorFrame, text="Editor", font = "Arial 24 bold")
#gives info about highlighted point
pointSelectedVar = tk.StringVar(value="(xxx,xxx) | Curve x")
pointSelectedInfo = ttk.Label(master=editorFrame, text="PointInfo", textvariable=pointSelectedVar, font="Arial 12")
pointSelectedLabel = ttk.Label(master=editorFrame, text="Highlighted Point:", font="Arial 14")


entryFrame = ttk.Frame(master=editorFrame, width=200, height=130)
newXInt = tk.IntVar()
newYInt = tk.IntVar()
xEntry = ttk.Entry(master=entryFrame, textvariable=newXInt)
yEntry = ttk.Entry(master=entryFrame, textvariable=newYInt)
xLabel = ttk.Label(master=entryFrame, text="X:", font="Arial 14")
yLabel = ttk.Label(master=entryFrame, text="Y:", font="Arial 14")

def updateXY():
    global isMovingPoint
    global HermiteCurves
    global movePoint
    global newXInt
    global newYInt

    if isMovingPoint:
        HermiteCurves[movePoint[0]].controlPoints[movePoint[1]] = [newXInt.get(), newYInt.get()]

def removeHighlight():
    global isMovingPoint
    isMovingPoint = False

setXYButton = ttk.Button(master=entryFrame, text="Update Position",command=updateXY)
clearHighlightButton = ttk.Button(master=entryFrame, text="Clear Highlighted Point", command=removeHighlight)

#Add scrollbar to display currently placed lines in HermiteLines()

#editor information
EditorTitle.place(x=70, y=0, anchor="nw")
pointSelectedLabel.place(x=45, y=50, anchor="nw")
pointSelectedInfo.place(x=60, y=80, anchor="nw")

#changing points via entries
clearHighlightButton.place(x=50, y=0, anchor="nw")
xLabel.place(x=45,y=40, anchor="nw")
xEntry.place(x=75, y=40, anchor="nw")
yLabel.place(x=45, y=70, anchor="nw")
yEntry.place(x=75, y=70, anchor="nw")
setXYButton.place(x=65, y=100, anchor="nw")
entryFrame.place(x=0, y=135, anchor="nw")

#place main editor frame
editorFrame.place(x=545, y=15, anchor="nw")

#functions for adding new curves
def add_quintic():
    global addingCurve
    global pointsToAdd
    global curveType

    if not addingCurve:
        addingCurve = True
        pointsToAdd = 6
        curveType = "quintic"

def add_cmr():
    global addingCurve
    global pointsToAdd
    global cmrNumPoints
    global curveType

    if not addingCurve and cmrNumPoints.get() >= 4:
        addingCurve = True
        pointsToAdd = cmrNumPoints.get()
        curveType = "cmr"

#widgets for adding new curves
curveAddFrame = ttk.Frame(master=window, width=400, height=100)
addCurveLabelText = tk.StringVar(value="Adding Curve")
curveAddedLabel = ttk.Label(master=curveAddFrame, textvariable=addCurveLabelText, font="Arial 14 bold")
addQuinticButton = ttk.Button(master=curveAddFrame, text="Quintic Bezier", command=add_quintic)
cmrNumPoints = tk.IntVar()
addCMRButton = ttk.Button(master=curveAddFrame, text="Catmull Rom", command=add_cmr)
cmrPointInput = ttk.Entry(master=curveAddFrame, textvariable=cmrNumPoints, width=1)

curveAddedLabel.place(x=100, y=0, anchor="nw")
addQuinticButton.place(x=30, y=30, anchor="nw")
addCMRButton.place(x=130, y=30, anchor="nw")
cmrPointInput.place(x=210, y=33, anchor="nw")

curveAddFrame.place(x=15, y=520, anchor="nw")


def canvasClick(event):

    x = window.winfo_pointerx() - window.winfo_rootx() - 15  #subtract padding
    y = window.winfo_pointery() - window.winfo_rooty() - 15  #subtract padding
    
    handlePointClick(x, y, 10)
    handleCurveCreation(x, y)


canvas.bind('<Button-1>', canvasClick)

def displayHighlightInfo():
    global isMovingPoint
    global movePoint
    global HermiteCurves

    if isMovingPoint:
        pointSelectedVar.set(f"     { HermiteCurves[movePoint[0]].controlPoints[movePoint[1]] }\nCurve {movePoint[0]} Index {movePoint[1]}")
    else:
        pointSelectedVar.set("")


def displayAddCurveInfo():
    global addCurveLabelText
    global addingCurve
    global pointsToAdd

    print(addingCurve)

    if addingCurve:
        addCurveLabelText.set(f"Adding Curve | {pointsToAdd} Points Left")
    else:
        addCurveLabelText.set("")


def drawAllCurves():
    global HermiteCurves

    for curve in HermiteCurves:
        curve.updatePoints()
        drawLines(curve.bezierPoints, canvas, "red", 5)
        drawPoints(curve.controlPoints, canvas, "blue", 5)


def update():

    displayHighlightInfo()
    displayAddCurveInfo()
    canvas.delete("all")

    drawAllCurves()
    window.after(100, update)

update()
window.mainloop()
