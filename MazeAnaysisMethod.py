import ClassSet as cs
import GridMath as gm
import MazeMethod as mm
import RhinoMethod as rm
import rhinoscriptsyntax as rs

def getInteriorPoint(grid, message):
    ptPosition = rs.GetPoint(message)
    if ptPosition :
        ptGridIndex = ((ptPosition[0]-grid.referencePoint[0]+grid.width*0.5)/grid.width, (ptPosition[1]-grid.referencePoint[1]+grid.length*0.5)/grid.length)
        ptIndex = int(gm.toArray(ptGridIndex, grid.gridWidth+1))
        return grid.logicPoints[ptIndex]
    else:
        return None
    pass

def Dijkstra(grid, startPt=None):
    calculatingGroup = []
    nextGroup = []
    visitedGroup = []
    if startPt == None:
        startPt = getInteriorPoint(grid, 'Please select the interior start point for analysis')
    #initialize
    calculatingGroup.append(startPt)
    index = 0
    # recursive process
    while len(calculatingGroup) != 0:
        nextGroup = []
        for pt in calculatingGroup:
            pt.DijkstraIndex = index
            visitedGroup.append(pt)
            nextNeighbors = pt.mazeNeighbors
            nextGroup += (list(set(nextNeighbors) - set(visitedGroup)))
        index += 1
        calculatingGroup = nextGroup
    pass
    return index


def pathFindingBasedOnDijkstra(grid):
    startPt =  getInteriorPoint(grid, 'Please select the interior start point')
    endPt = getInteriorPoint(grid, 'Please select the interior end point')
    pathList = []
    Dijkstra(grid, startPt)
    start = endPt
    while start.DijkstraIndex != 0:
        for neighbor in start.mazeNeighbors:
            if (start.DijkstraIndex - neighbor.DijkstraIndex) == 1:
                pathList += [(start, neighbor)]
                start = neighbor
    for ptPair in pathList:
        rm.drawAtLayer2(rs.AddLine, ptPair[0].position, ptPair[1].position, 'Solution', color=(255,0,0))
    return pathList
