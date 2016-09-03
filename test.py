import ClassSet as cs
import MazeMethod as mm
import MazeAnaysisMethod as mam

''' These are for generating the whole maze grid. For later analysis purpose, please keep the isLogicPoiintOn=True'''
grid = cs.Grid((0,0,0), 20, 20, 5, 5)
chosedPoints =mm.huntAndKill(grid, grid.interiorLogicPoints)
grid.update(chosedPoints)
grid.drawAll(isPositionPointOn = False, isLogicPointOn = True, isWallOn = True, isPathOn = True)

''' These are for the Dijkstra analysis for the whole maze, please select the logicPoints in the maze or there will come an error'''
maxIndex = mam.Dijkstra(grid)
grid.drawAnalysis(maxIndex)

'''This is for the path finding. Please make sure that the start point and end point are both from the logicPoints and in the maze, or there will come an error'''
mam.pathFindingBasedOnDijkstra(grid)
