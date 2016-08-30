import ClassSet as cs
import MazeMethod as mm
grid = cs.Grid((0,0,0), 30, 40 , 5, 8)
chosedPoints =mm.recursiveBacktracker(grid, grid.interiorLogicPoints)
grid.update(chosedPoints)
grid.drawAll(isPositionPointOn = False, isLogicPointOn = False, isWallOn = True, isPathOn = True)
