import GridMath as gm
import rhinoscriptsyntax as rs
import RhinoMethod as rm

class Point(object):
    """docstring for Point.It is the conceptual class to shape the grid"""
    def __init__(self, referencePoint, gridIndex, unitWidth, unitLength,layer, color):
        super(Point, self).__init__()
        self.referencePoint = referencePoint
        self.gridIndex = gridIndex
        self.unitWidth = unitWidth
        self.unitLength = unitLength
        self.layer = layer
        self.color = color
        rp = referencePoint

        i = gridIndex[0]
        j = gridIndex[1]
        xOffset = (i) * unitWidth
        yOffset = (j) * unitLength

        self.position = ((xOffset+rp[0]), (yOffset+rp[1]),rp[2]) #2D now

    def draw(self):
        rm.drawAtLayer(rs.AddPoint, self.position, self.layer, self.color)
        pass


class PositionPoint(Point):
    """docstring for PositionPoint. It's the point which phisically define the shape of the grid"""
    def __init__(self, referencePoint, gridIndex, unitWidth, unitLength,layer='PositionPoint', color=(120,120,120)):
        super(PositionPoint, self).__init__(referencePoint, gridIndex, unitWidth, unitLength,layer, color)
        self.neighbors = []# wait to be initialized by Grid class, 0=left, 1=up, 2=right, 3=down


class LogicPoint(Point):
    """
       It's the invisible points which will later define the path finding
       and will define how the grid lines will be open or closed.
    """
    def __init__(self,referencePoint, gridIndex, unitWidth, unitLength,layer='LogicPoint', color=(150,0,0)):
        rp = referencePoint
        referencePoint = ((rp[0]-0.5*unitWidth),(rp[1]-0.5*unitLength),rp[2])
        super(LogicPoint, self).__init__(referencePoint, gridIndex, unitWidth, unitLength,layer,color)
        self.neighbors = []# wait to be initialized by Grid class, 0=left, 1=up, 2=right, 3=down
        self.mazeNeighbors = [] # wait to be initialized by the MazeMethods and for later analysis
        self.interiorNeighbors = [] #wait to be initialized by the MazeMethods
        self.isInterior = False # wait to be changed by Grid class
        self.isEnd = False # wait to be changed on the users' demands
        self.isVisited = False # wait to be changed by PathMaker class
        self.isChosen = False # wait to be changed by PathMaker class
        self.DijkstraIndex = int # wait to be given by Dijkstra analysis

    def drawDijkstraIndex(self,fontHeight, layer='DijkstraIndex', color=(120,120,120)):
        if rs.IsLayer(layer):
            rs.LayerColor(layer, color)
            pass
        else:
            rs.AddLayer(layer, color)
        rs.CurrentLayer(layer)
        rs.AddText(str(self.DijkstraIndex),self.position, height=fontHeight, justification=2)
        pass

    def drawDijkstraColor(self, width, height, color, maxIndex, layer='DijkstraColor' ):
        if rs.IsLayer(layer):
            rs.LayerColor(layer)
            pass
        else:
            rs.AddLayer(layer)
        rs.CurrentLayer(layer)
        pass
        drawColor = rm.setChoromeColor(self.DijkstraIndex, maxIndex, color)
        drawPosition = (self.position[0]-width*0.5, self.position[1]-height*0.5, self.position[2])
        rectGuid = rs.AddRectangle(drawPosition, width, height)
        guid = rs.AddPlanarSrf(rectGuid)
        rs.DeleteObject(rectGuid)
        rs.ObjectColor(guid, drawColor)
        pass


class Line(object):
    """It's the conceptual skeleton for all line-like class"""
    def __init__(self, endPoints, layer, color, isDrawedOpen=False, openRatio=0.5):
        super(Line, self).__init__()
        self.endPoints = endPoints
        self.isDrawedOpen = isDrawedOpen
        self.openRatio = openRatio
        self.layer = layer
        self.color = color
        self.direction = gm.getDirection(endPoints[0], endPoints[1])

    def draw(self):
        if self.isDrawedOpen == False: #normal
            rm.drawAtLayer2(rs.AddLine, self.endPoints[0], self.endPoints[1], self.layer, self.color)
        #else:
            #rm.drawOpenLine(self.endPoints, self.openRatio, self.layer, self.color)
        pass


class Wall(Line):
    """the graph presentation and has nothing to do with logic"""
    def __init__(self, endPoints, layer='Wall', isDrawedOpen=False, openRatio=0.5, color=0):
        super(Wall, self).__init__(endPoints, layer, color)
        self.controlLogicPoints = [] # wait to be initialized by Grid class


class Path(Line):
    """shows all the routes of the maze and which types of the routes"""
    def __init__(self, endPoints, layer='Path', isDrawedOpen=False, openRatio=0.5, color=(0,255,0)):
        super(Path, self).__init__(endPoints, layer, color)
        self.type = 4 # 0=undefined, 1=main, 2=subsidiary, 3=circuit, 4=unchosen



class Grid(object):
    """The mother class which holds all other classes together and give the comprehensive idea of the maze. 2D version"""
    def __init__(self, referecePoint, gridWidth, gridLength, width, length):
        self.referencePoint = referecePoint
        self.gridWidth = gridWidth
        self.gridLength = gridLength
        self.width = width
        self.length = length
        self.positionPoints = []
        self.logicPoints = []
        self.interiorLogicPoints = []
        self.exteriorLogicPoints = []
        self.walls = []
        self.wallsDict = {}
        self.paths = []
#initialize all positionPoints
        i = 0
        j = 0
        while  (j < gridLength):
            while (i < gridWidth):
                pp = PositionPoint(self.referencePoint, (i,j), width, length, layer='PositionPoint')
                self.positionPoints.append(pp)
                i = i + 1
                pass
            j = j + 1
            i = 0
            pass
        for pt in self.positionPoints: #initialize each point's neighbors
            pt.neighbors = gm.setNeighbors(pt.gridIndex, self.positionPoints, self.gridLength, self.gridWidth)
            pass

#initialize all logicPoints
        i = 0
        j = 0
        while  (j <= gridLength ):
            while (i <= gridWidth):
                lp = LogicPoint(self.referencePoint, (i,j), width, length, layer='LogicPoint', color=(150,0,0))
                self.logicPoints.append(lp)
                i = i + 1
            j = j + 1
            i = 0
        for pt in self.logicPoints:
            pt.neighbors = gm.setNeighbors(pt.gridIndex, self.logicPoints, (self.gridLength+1), (self.gridWidth+1))
            count = 0
            for neighborPt in pt.neighbors:
                if neighborPt != None:
                    count = count + 1
                    pass
            if count == 4:
                self.interiorLogicPoints.append(pt)
                pt.isInterior = True
                pass
            else:
                self.exteriorLogicPoints.append(pt)
            pass
#initialize all walls to be closed
        wallPositionList = []
        controlPointsList = []
        wallPositionList = wallPositionList + gm.getCrossPairs(self.positionPoints, self.logicPoints, self.gridWidth, (self.gridWidth+1), isHorizontal=True)[0]
        controlPointsList = controlPointsList + gm.getCrossPairs(self.positionPoints, self.logicPoints, self.gridWidth, (self.gridWidth+1), isHorizontal=True)[1]

        verticalArray = gm.getVerticalPointsArray(self.positionPoints, self.gridWidth, self.gridLength)
        wallPositionList = wallPositionList + gm.getCrossPairs(verticalArray, self.logicPoints, self.gridLength, (self.gridWidth+1), isHorizontal=False)[0]
        controlPointsList = controlPointsList + gm.getCrossPairs(verticalArray, self.logicPoints, self.gridLength, (self.gridWidth+1), isHorizontal=False)[1]

        i = 0
        while (i < len(wallPositionList)):
            endPoints = []
            for positionPoint in wallPositionList:
                endPoints.append((positionPoint[0].position, positionPoint[1].position))
            wall = Wall(endPoints[i], layer='Wall', isDrawedOpen=False, openRatio=0.5, color=0)
            wall.controlLogicPoints = controlPointsList[i]
            self.walls.append(wall)
            key1 = wall.controlLogicPoints[0].gridIndex
            key2 = wall.controlLogicPoints[1].gridIndex
            self.wallsDict[(key1,key2)] = i
            i = i + 1
            pass

    def drawAll(self, isPositionPointOn = False, isLogicPointOn = False, isWallOn = True, isPathOn = False):
        def checkDraw(trigger, list):
            if trigger == True:
                for item in list:
                    item.draw()
                pass
            pass
        checkDraw(isPositionPointOn, self.positionPoints)
        checkDraw(isLogicPointOn, self.logicPoints)
        checkDraw(isWallOn, self.walls)
        checkDraw(isPathOn, self.paths)

    def update(self,controlPointsList):
        for pts in controlPointsList:
            #change the walls state to make the maze
            key = (pts[0].gridIndex, pts[1].gridIndex)
            index = self.wallsDict[key]
            wall = self.walls[index]
            wall.isDrawedOpen = True
#initaiize the Path class to represent the route in the maze
            position1 = pts[0].position
            position2 = pts[1].position
            path = Path((position1, position2), layer='Path', isDrawedOpen=False, openRatio=0.5, color=(0,255,0))
            self.paths.append(path)
    def drawAnalysis(self, max, color = (200,150,255)):
        for pt in self.interiorLogicPoints:
            pt.drawDijkstraIndex(self.width/5)
            pt.drawDijkstraColor(self.width, self.length, color, max, layer='DijkstraColor')
        pass
