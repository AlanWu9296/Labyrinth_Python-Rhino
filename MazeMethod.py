import random as rand
import GridMath as gm

'''These are general methods that may be later used'''

def makeNeighbors(grid, point, pointNeighbor):
    pointIndex = gm.toArray(point.gridIndex, (grid.gridWidth+1))
    basePoint = grid.logicPoints[pointIndex]
    basePoint.isChosen = True
    pointNeighborIndex = gm.toArray(pointNeighbor.gridIndex, (grid.gridWidth+1))
    grid.logicPoints[pointNeighborIndex].isChosen = True
    basePoint.mazeNeighbors.append(grid.logicPoints[pointNeighborIndex])
    grid.logicPoints[pointNeighborIndex].mazeNeighbors.append(basePoint)
    check = gm.checkPointsOrder(basePoint.gridIndex, pointNeighbor.gridIndex)
    if check == True:
        return (basePoint, grid.logicPoints[pointNeighborIndex])
    else:
        return (grid.logicPoints[pointNeighborIndex], basePoint)
    pass

def setInteriorNeighbors(interiorPoints):
    for interiorPoint in interiorPoints:
        neighbors = [pt for pt in interiorPoint.neighbors if pt != None]
        interiorNeighbors = list(set(neighbors).intersection(set(interiorPoints)))
        interiorPoint.interiorNeighbors = interiorNeighbors
    pass

def getRandomUnvisitedInteriorNeighbor(point,pointList):# !!! attention, it's now only for interiorNeighbors
    potentialNeighborList = []
    for neighbor in  point.interiorNeighbors:
        if neighbor.isVisited == True:
            pass
        else:
            potentialNeighborList.append(neighbor)
        pass
    if len(potentialNeighborList) == 0:
        return None
    else:
        neighbor = gm.getRandomItem(potentialNeighborList)
        index = pointList.index(neighbor)
        pointList[index].isVisited = True
        return neighbor
        pass
    pass

def getPointWithUnvisitedNeibors(pointList, isInOrder=False): # !!! attention, it's now only for interiorNeighbors
    newPointList = []
    for pt in pointList:
        potentialNeighborList =  pt.interiorNeighbors
        visitedCount = 0
        for neighbor in potentialNeighborList:
            if neighbor.isVisited == True:
                visitedCount =visitedCount + 1
                pass
            pass
        if visitedCount == len(potentialNeighborList):
            pass
        else: newPointList.append(pt)
    if isInOrder ==  False:
        return gm.getRandomItem(newPointList)
    else:
        if len(newPointList) != 0:
            return newPointList[-1]
        else:
            return None
        pass
    pass


def getRandomUnchosenInteriorNeighbor(point,pointList):# !!! attention, it's now only for interiorNeighbors
    potentialNeighborList = []
    for neighbor in  point.interiorNeighbors:
        if neighbor.isChosen == True:
            pass
        else:
            potentialNeighborList.append(neighbor)
        pass
    if len(potentialNeighborList) == 0:
        return None
    else:
        neighbor = gm.getRandomItem(potentialNeighborList)
        index = pointList.index(neighbor)
        pointList[index].isChosen = True
        return neighbor
        pass
    pass

def getPointWithUnchosenNeibors(pointList, isInOrder=False): # !!! attention, it's now only for interiorNeighbors
    newPointList = []
    for pt in pointList:
        potentialNeighborList =  pt.interiorNeighbors
        visitedCount = 0
        for neighbor in potentialNeighborList:
            if neighbor.isChosen == True:
                visitedCount += 1
                pass
            pass
        if visitedCount == len(potentialNeighborList):
            pass
        else: newPointList.append(pt)
    if isInOrder ==  False:
        return gm.getRandomItem(newPointList)
    else:
        if len(newPointList) != 0:
            return newPointList[-1]
        else:
            return None
        pass
    pass

''' These are methods to generate maze'''

def binaryTree(grid, logicPointsList):
    controlPointsList = []
    for logicPoint in logicPointsList:
        neighbors = logicPoint.neighbors[1:3]
        PotentialNeighbors = list(set(neighbors).intersection(set(logicPointsList)))
        binaryTreeNeighbor = gm.getRandomItem(PotentialNeighbors)
        if binaryTreeNeighbor != None:
            controlPointsList.append((makeNeighbors(grid, logicPoint, binaryTreeNeighbor)))
            pass
        pass
    return controlPointsList

def sideWinder(grid, logicPointsList):
    controlPointsList = []
    visitedPts = []
    for logicPoint in logicPointsList:
        visitedPts.append(logicPoint)
        coin = rand.random()
        if coin < 0.5:
            basePt = gm.getRandomItem(visitedPts)
            potentialNeighbor = basePt.neighbors[1]
            test = list(set([potentialNeighbor]).intersection(set(logicPointsList)))
            if len(test) != 0:
                sideWinderNeighbor = potentialNeighbor
                controlPointsList.append(makeNeighbors(grid, basePt, sideWinderNeighbor))
                visitedPts = []
                pass
            else:
                test = list(set([logicPoint.neighbors[2]]).intersection(set(logicPointsList)))
                if len(test) != 0:
                    sideWinderNeighbor = logicPoint.neighbors[2]
                    controlPointsList.append(makeNeighbors(grid, logicPoint, sideWinderNeighbor))
                    visitedPts = []
                pass
            pass
        else:
            potentialNeighbor = logicPoint.neighbors[2]
            test = list(set([potentialNeighbor]).intersection(set(logicPointsList)))
            if len(test) !=  0:
                sideWinderNeighbor = potentialNeighbor
                visitedPts.append(sideWinderNeighbor)
                controlPointsList.append(makeNeighbors(grid, logicPoint, sideWinderNeighbor))
                pass
            else:
                test = list(set([logicPoint.neighbors[1]]).intersection(set(logicPointsList)))
                if len(test) != 0:
                    sideWinderNeighbor = logicPoint.neighbors[1]
                    controlPointsList.append(makeNeighbors(grid, logicPoint, sideWinderNeighbor))
                    visitedPts = []
                    pass
                pass
            pass
        pass
    return controlPointsList
    pass

def Aldous_Broder(grid, logicPointsList): # This is a refined method for the original Aldous_Broder
    controlPointsList = []
    visitedPointList = []
    setInteriorNeighbors(logicPointsList)
    unvisitedCount = len(logicPointsList)
    #initialize
    start = gm.getRandomItem(logicPointsList)
    visitedPointList.append(start)
    unvisitedCount -= 1
    # creating process
    while unvisitedCount != 0:
        neighbor = gm.getRandomItem(start.interiorNeighbors)
        if neighbor.isVisited == False:
            controlPointsList.append(makeNeighbors(grid, start, neighbor))
            start.isVisited = True
            neighbor.isVisited = True
            unvisitedCount -= 1
            visitedPointList.append(neighbor)
            start = neighbor
        else:
            # below are the refined methods to help to better find unvisited neighbors
            nextNeighbor = getRandomUnvisitedInteriorNeighbor(neighbor, logicPointsList)
            if nextNeighbor != None:
                controlPointsList.append(makeNeighbors(grid, neighbor, nextNeighbor))
                nextNeighbor.isVisited = True
                unvisitedCount -= 1
                start = nextNeighbor
                visitedPointList.append(start)
            else:
                newStart = getPointWithUnvisitedNeibors(visitedPointList)
                if newStart != None:
                  newNeibor = getRandomUnvisitedInteriorNeighbor(newStart, logicPointsList)
                  if newNeibor != None:
                      controlPointsList.append(makeNeighbors(grid, newStart, newNeibor))
                      newStart.isVisited = True
                      newNeibor.isVisited = True
                      unvisitedCount -= 1
                      start = newNeibor
                      visitedPointList.append(start)
                  else:
                      start = neighbor
                else:
                   start = neighbor
    return controlPointsList
    pass


def Wilson(grid, logicPointsList):
    controlPointsList = []
    visitedPointList = []
    setInteriorNeighbors(logicPointsList)
    unChosenPointList = [pt for pt in logicPointsList]
    #initialize
    origin = gm.getRandomItem(unChosenPointList)
    origin.isVisited = True
    origin.isChosen = True
    unChosenPointList.remove(origin)
    start = gm.getRandomItem(unChosenPointList)
    start.isVisited = True
    visitedPointList.append(start)
    # Recursing process
    while len(unChosenPointList) != 0:
        neighbor = gm.getRandomItem(start.interiorNeighbors)
        if neighbor.isVisited == False:
            neighbor.isVisited = True
            visitedPointList.append(neighbor)
            start = neighbor
        else:
            if neighbor.isChosen == True:
                for pt in visitedPointList: unChosenPointList.remove(pt)
                visitedPointList.append(neighbor)
                i = 0
                while i < (len(visitedPointList)-1):
                    visitedPointList[i].isChosen = True
                    visitedPointList[(i+1)].isChosen = True
                    controlPointsList.append(makeNeighbors(grid, visitedPointList[i], visitedPointList[(i+1)]))
                    i += 1
                    pass
                if len(unChosenPointList) != 0:
                    start = gm.getRandomItem(unChosenPointList)
                    start.isVisited = True
                    visitedPointList = [start]
                else:
                    break
                pass
            else: #neighbor.isVisited == True
                index = visitedPointList.index(neighbor)
                savedPoints = visitedPointList[0:(index+1)]
                resetPointsList = visitedPointList[(index+1):]
                for pt in resetPointsList: pt.isVisited = False
                visitedPointList = savedPoints
                start = neighbor
        pass
    return controlPointsList
    pass


def huntAndKill(grid, logicPointsList):
    controlPointsList = []
    chosenPoints = []
    setInteriorNeighbors(logicPointsList)
    unChosenPointList = [pt for pt in logicPointsList]
    #initialize
    start = gm.getRandomItem(unChosenPointList)
    start.isChosen = True
    chosenPoints.append(start)
    unChosenPointList.remove(start)
    #Recursing process
    while len(unChosenPointList) != 0:
        neighbor = gm.getRandomItem(start.interiorNeighbors)
        if neighbor.isChosen == False:
            neighbor.isChosen = True
            controlPointsList.append(makeNeighbors(grid, start, neighbor))
            unChosenPointList.remove(neighbor)
            chosenPoints.append(neighbor)
            start = neighbor
        else:
            if len(chosenPoints) != 0:
                newNeighbor = getPointWithUnchosenNeibors(chosenPoints)
                start = getRandomUnchosenInteriorNeighbor(newNeighbor, logicPointsList)
                controlPointsList.append(makeNeighbors(grid, start, newNeighbor))
                start.isChosen =  True
                chosenPoints.append(start)
                unChosenPointList.remove(start)
            else:
                break
            pass
        pass
    return controlPointsList
    pass


def recursiveBacktracker(grid, logicPointsList):
    controlPointsList = []
    visitedPointList = []
    setInteriorNeighbors(logicPointsList)
    unChosenPointList = [pt for pt in logicPointsList]
    #initialize
    start = gm.getRandomItem(unChosenPointList)
    start.isVisited = True
    visitedPointList.append(start)
    unChosenPointList.remove(start)
    # creating process
    while len(unChosenPointList) != 0:
        neighbor = gm.getRandomItem(start.interiorNeighbors)
        if neighbor.isVisited == False:
            neighbor.isVisited = True
            controlPointsList.append(makeNeighbors(grid, start, neighbor))
            unChosenPointList.remove(neighbor)
            visitedPointList.append(neighbor)
            start = neighbor
        else:
            neighbor = getRandomUnvisitedInteriorNeighbor(start, logicPointsList)
            if neighbor != None:
                neighbor.isVisited = True
                controlPointsList.append(makeNeighbors(grid, start, neighbor))
                unChosenPointList.remove(neighbor)
                visitedPointList.append(neighbor)
                start = neighbor
            else:
                newStart = getPointWithUnvisitedNeibors(visitedPointList, isInOrder=True)
                if newStart != None:
                    newNeighbor = getRandomUnvisitedInteriorNeighbor(newStart, logicPointsList)
                    if newNeighbor != None:
                        controlPointsList.append(makeNeighbors(grid, newStart, newNeighbor))
                        unChosenPointList.remove(newNeighbor)
                        newNeighbor.isVisited = True
                        visitedPointList.append(newNeighbor)
                        start = newNeighbor
                pass
    return controlPointsList
    pass
