import ClassSet as cs
import MazeMethod as mm
grid = cs.Grid((0,0,0),50 ,25 , 4, 4)
chosedPoints =mm.Wilson(grid, grid.interiorLogicPoints)
grid.update(chosedPoints)
grid.drawAll(isPositionPointOn = False, isLogicPointOn = False, isWallOn = True, isPathOn = True)
