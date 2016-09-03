import rhinoscriptsyntax as rs

def drawAtLayer(drawMethod, rhinoObject, layer, color = None):
    if rs.IsLayer(layer):
        rs.LayerColor(layer, color)
        pass
    else:
        rs.AddLayer(layer, color)
    rs.CurrentLayer(layer)

    drawMethod(rhinoObject)

def drawAtLayer2(drawMethod, rhinoObject1, rhinoObject2, layer, color = None):
    if rs.IsLayer(layer):
        rs.LayerColor(layer, color)
        pass
    else:
        rs.AddLayer(layer, color)
    rs.CurrentLayer(layer)

    drawMethod(rhinoObject1, rhinoObject2)

def drawOpenLine(EndPoints, ratio, layer, color = None):

    if rs.IsLayer(layer):
        pass
    else:
        rs.AddLayer(layer, color)
    rs.CurrentLayer(layer)

    pt1 = EndPoints[0]
    pt2 = EndPoints[1]
    vector12 = rs.VectorCreate(pt2, pt1)
    vectorRatio = (1 - ratio) * 0.5
    pt1End = rs.VectorAdd(pt1, (vector12*vectorRatio))
    pt2End = rs.VectorAdd(pt2,((-vector12)*vectorRatio))
    rs.AddLine(pt1, pt1End)
    rs.AddLine(pt2, pt2End)
    pass


def setChoromeColor(index, max, colorHBL, isChromed = False):
    if isChromed == True:
        colorNew = (colorHBL[0], colorHBL[1], colorHBL[2]/max*(max-index))
    else: colorNew = (colorHBL[0]/max*index, colorHBL[1], colorHBL[2])
    color = rs.ColorHLSToRGB (colorNew)
    return color
