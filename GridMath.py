import random as rand


def getDirection(a, b): # pt,pt->int; 0=xAxis, 1=yAxis, 2=zAxis
    direction = 0
    for i,j in zip(a,b) :
        if (i-j) == 0:
            break
        else:
            direction = direction + 1
        pass
    return direction


def toArray(matrixNum, matrixWidth): #(x, y) , int -> int
    arrayNum = (matrixNum[1] * matrixWidth + matrixNum[0])
    return arrayNum


def setNeighbors(ptIndex, pointsList, gridLength, gridWidth): #((x,y),[pt...]) -> [index...]
    x = ptIndex[0]
    y = ptIndex[1]
    neighbors = [] # 0=left, 1=up, 2=right, 3=down
    ptMatrix = [(x-1, y),(x, y+1), (x+1, y), (x, y-1)]

    for pt in ptMatrix:
        if (0 <= pt[0] < gridWidth) and (0 <= pt[1] < gridLength):
            index = toArray(pt, gridWidth)
            neighbors.append(pointsList[index])
        else:
            neighbors.append(None)
    return neighbors


def getVerticalPointsArray(list, gridWidth, gridLength):
    verticalArray = []
    i = 0
    j = 0
    while i < gridWidth:
        while j < gridLength:
            index = toArray((i,j), gridWidth)
            verticalArray.append(list[index])
            j = j + 1
        i = i + 1
        j = 0
        pass
    pass
    return verticalArray

def getCrossPairs(positionPointsList, logicPointsList, gridWidth, logicGridWidth, isHorizontal=True):
    endPoints = []
    controlPoints = []
    def getIndex2Horizontal(gridIndex, logicGridWidth):
        newIndex = (gridIndex[0],(gridIndex[1]+1))
        return toArray(newIndex, logicGridWidth)
        pass
    def getIndex2vertical(gridIndex, logicGridWidth,):
        newIndex = ((gridIndex[0]+1),gridIndex[1])
        return toArray(newIndex, logicGridWidth)
        pass
    def getTwoPairs(index2Function, gridWidth):
        i = 0
        j = gridWidth
        while j <= (len(positionPointsList)):
            rowPoints = positionPointsList[i:j]
            t = 0
            while t < (len(rowPoints)-1):
                endPoints.append((rowPoints[t],rowPoints[(t+1)]))
                testIndex = rowPoints[t+1].gridIndex
                index1 = toArray(rowPoints[t+1].gridIndex, logicGridWidth)
                index2 = index2Function(rowPoints[t+1].gridIndex, logicGridWidth)
                controlPoints.append((logicPointsList[index1],logicPointsList[index2]))
                t = t + 1
                pass

            i = i + gridWidth
            j = j + gridWidth
            pass
        return (endPoints, controlPoints)
        pass

    if isHorizontal == True:
        pair = getTwoPairs(getIndex2Horizontal,gridWidth)
    else:
        pair = getTwoPairs(getIndex2vertical, gridWidth)
    return pair
    pass


def getRandomItem(list):  #always return Object not None
    if len(list) == 0:
        return None
        pass
    compareArray = []
    if len(list) != 0:
        gap = len(list)
    else:
        gap = 1
    ratio = 1.0 / gap
    seed = rand.random()
    while  ratio < 1:
        compareArray.append(ratio)
        ratio = ratio + ratio
        pass
    compareArray.append(seed)
    compareArray.sort()
    index = (compareArray.index(seed))
    item = list[index]
    if item != None:
        return item
    else:
        list.remove(item)
        return getRandomItem(list)
    pass

def checkPointsOrder(pt1, pt2):#pt = (x,y,z)
    for i,j in zip(pt1,pt2):
        if i> j:
            return False
            break
            pass
        pass
    return True
    pass
