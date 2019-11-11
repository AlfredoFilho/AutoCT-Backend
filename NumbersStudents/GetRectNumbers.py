import cv2
import numpy as np

modelo = cv2.imread('ModeloPNGTeste.png')

def findContours():
    
    img_gray = cv2.cvtColor(modelo, cv2.COLOR_RGB2GRAY)
    contours, hierarchy = cv2.findContours(~img_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def cutImage (polygonExternalPoints):
    # Define the corners of the target rectangle
    width, height = 680, 966
    cutOutPoints = np.zeros(polygonExternalPoints.shape, dtype=np.float32)
    cutOutPoints[0] = (0, 0)
    cutOutPoints[1] = (0, height)
    cutOutPoints[2] = (width, height)
    cutOutPoints[3] = (width, 0)

    transformationMatrix = cv2.getPerspectiveTransform(polygonExternalPoints.astype(np.float32), cutOutPoints)

    # Apply perspective transformation
    bigRect = cv2.warpPerspective(modelo, transformationMatrix, (width, height))
    return bigRect
    

def extractTemplateRectangle():
    # Find contour of the biggest rectangle
    contours = findContours()
    templateRectangle = max(contours, key = cv2.contourArea)

    ## Stract the polygon points
    epsilonCurve = 0.01 * cv2.arcLength(templateRectangle, True)
    polygonExternalPoints = cv2.approxPolyDP(templateRectangle, epsilonCurve, True)

    bigRect = cutImage(polygonExternalPoints)
    return bigRect


def cutRect(bigRect, xCoord, yCoord, height, width):
    
    rect = bigRect[yCoord:yCoord + height, xCoord:xCoord + width]
    return rect


def getRects(bigRect):
    
    
    widthRect = 27
    heightRect = 27
    List_Vertex_X = [61, 98, 135, 172, 211, 249, 285, 323, 361, 399, 438, 474, 512, 551, 590]
    List_Coord_Y = [40, 88, 133, 178, 223]
    
    listRects = []
    
    contLinha = 1
    
    for Y in List_Coord_Y:
        
        print('Linha: ' + str(contLinha))
        contLinha = contLinha + 1
        
        for X in List_Vertex_X:
            rect = cutRect(bigRect, X, Y, heightRect, widthRect)
            listRects.append(rect)
            
            
            
            rectResize = cv2.resize(rect, (300, 300))
            cv2.imshow('Rect', rectResize)
            cv2.waitKey(0)
            

    
    return listRects
    
    
bigRect = extractTemplateRectangle()

listRects = []
listRects = getRects(bigRect)

#
#for rect in listRects:
#    cv2.imshow('Rect', rect)
#    cv2.waitKey(0)