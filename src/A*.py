import pygame
import math


wdith = 1280
height = 720
pygame.init()
screen = pygame.display.set_mode((wdith,height))
clock = pygame.time.Clock()
running = True




font = pygame.font.Font(None, 34)
text = font.render("A* pathfinding", 2,"black")
textpos = text.get_rect()
textpos.center = (1140,20)

textStX = 1260
textStY = 700
textForStart = "Start"
textStartPos = text.get_rect()


textResetPos = text.get_rect()
textResetPos.center = (1110,700)
textReset = font.render("RESET", 2,"black")




messegeText = ""
messegeRect = text.get_rect()
messegeRect.center = (1100 -10,100)

class node:
    def __init__(self,color,x,y):
        self.color       = color
        self.posX = x
        self.posY = y
        self.hovered = False
        self.chosen = False
        self.hCost = 0
        self.gCost = 0
        self.fCost = 0
        self.Parent = None
        self.WalkAble = True




Nodes = []
selectingStart = False
selectingEND   = False
inPrgoress     = False
hoveredNode    = None

selectingWalk = False

nodeIndex = 0
startNode = None
endNode   = None


maxWidth = 1000
maxHeight = 720
squareSize = 40
def reset():
    print("ran")
    index = 0
    startNode = None
    endNode   = None
    selectingStart = False
    selectingEND = False
    selectingWalk = False
    messegeText = ""
    textForStart = "Start"

    for x in range(0,maxWidth,squareSize):
        for y in range(0,maxHeight,squareSize):
             Nodes[index].chosen = False
             Nodes[index].WalkAble = True
             index +=1



    

def nodeINIT():
    for x in range(0,1000,40):
        for y in range(0,height,40):
            color      = "gray"
            newNode    = node(color,x,y)
            Nodes.append(newNode)

nodeINIT()

def chebyshev_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


    
def startPathfinding():
    openNodes = [startNode]
    closedNodes = []
    foundPath = False

    startNode.gCost = 0
    startNode.hCost = chebyshev_distance(startNode.posX,startNode.posY,endNode.posX,endNode.posY)
    startNode.fCost = startNode.gCost + startNode.hCost
    currentNode = startNode
    index = 0
    
    while len(openNodes) >= 1 and foundPath == False:

        lastF = 99999999
        for openNode in openNodes:
            if openNode.fCost < lastF:
                currentNode = openNode
                lastF = openNode.fCost
 


        closedNodes.append(currentNode)
        openNodes.remove(currentNode)

        if currentNode == endNode:
            traceNode = endNode
            while traceNode.Parent:
                if traceNode.Parent == startNode:
                    break
                traceNode.Parent.color = "blue"
                traceNode.Parent.chosen = True
                traceNode = traceNode.Parent

            foundPath = True
            break

        for node in Nodes:
            if node in closedNodes:
                continue
            if node!= startNode and abs(currentNode.posX/40 - node.posX/40) <= 1 and abs(currentNode.posY/40 - node.posY/40) <=1 and node.WalkAble:
                if  not (node in openNodes) and not (node in closedNodes):
                    openNodes.append(node)
                    node.Parent = currentNode
                    node.gcost = chebyshev_distance(startNode.posX,startNode.posY,node.posX,node.posY)
                    node.hCost = chebyshev_distance(endNode.posX,endNode.posY,node.posX,node.posY)
                    node.fCost = node.gCost + node.hCost
                elif node in closedNodes and node.gCost < currentNode.gCost:
                    node.color = "orange"
                    node.chosen = True
                    openNodes.remove(node)  
                    closedNodes.remove(node)
                elif node in openNodes and node.gcost < currentNode.gCost:
                    node.color = "red"
                    node.chosen = True
                    openNodes.remove(node)
           


  



def drawGrid():
    index = 0
    for x in range(0,1000,40):
        for y in range(0,height,40):

            nodeColor = Nodes[index].color
            if Nodes[index].hovered == False and Nodes[index].chosen == False and Nodes[index].WalkAble == True:
                nodeColor = "gray"

            pygame.draw.rect(screen, nodeColor, pygame.Rect(x, y, 39, 39))
            index+= 1
    
def drawMenu():
    pygame.draw.rect(screen,"white",pygame.Rect(995,0,285,720))
    pygame.draw.rect(screen,"black",pygame.Rect(995,0,285,720),5)
    pygame.draw.rect(screen,"green",pygame.Rect(1140,675,135,40))
    pygame.draw.rect(screen,"gray",pygame.Rect(1000,675,140,40))
    pygame.draw.line(screen,"black",(1000,675),(1280,675),5)
    pygame.draw.line(screen,"black",(1140,675),(1140,720),5)
    screen.blit(text, textpos)
    textStart = font.render(textForStart, 2,"black")
    textStartPos.center = (textStX,textStY)
    screen.blit(textStart, textStartPos)
    screen.blit(textReset,textResetPos)
    messegeBox = font.render(messegeText, 2,"black")
    screen.blit(messegeBox,messegeRect)


while running:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            mousePosition = pygame.mouse.get_pos()
            X = mousePosition[0]
            Y = mousePosition[1]
            if X > 1140 and X < 1280 and Y > 675 and Y < 720 and inPrgoress == False:
                if selectingWalk == False and selectingStart == False and selectingEND == False:
                    print("ran")
                    selectingWalk = True
                    textForStart = "Continue"
                    textStX = 1240
                    messegeText = "Select unwalkable area"
                elif selectingWalk == True :
                    selectingWalk = False
                    selectingStart = True
                    messegeText = "Select start point"        
                elif selectingStart == True:
                    selectingEND == True
                    selectingStart = False
                    messegeText = "Select end point"
                elif selectingEND:
                     messegeText = "reset to try again"
                     selectingEND = False
                     startPathfinding()
                     inPrgoress = True       
            if X > 1000 and X < 1140 and Y > 675 and Y < 720:
                    inPrgoress = False
                    print("reset")
                    reset()
        if selectingWalk or selectingStart or selectingEND:
            mousePostion = pygame.mouse.get_pos()
            X = mousePostion[0]
            Y = mousePostion[1]
            for node in Nodes:
                if X > node.posX and X < (node.posX + 40) and Y > node.posY and Y < (node.posY + 40) and node.chosen == False:
                    if selectingWalk:
                       node.color = "black"
                       node.hovered = True
                       if pygame.mouse.get_pressed()[0]:
                          node.chosen = True
                          node.WalkAble = False   
                    elif selectingStart:
                        print("selecting start")
                        node.color ="green"
                        node.hovered = True
                        if pygame.mouse.get_pressed()[0]:
                          if startNode:
                            startNode.chosen = False

                          node.chosen = True
                          startNode = node
                          selectingEND = True
                    elif selectingEND:
                        print("selecting end")
                        node.color = "red"
                        node.hovered = True
                        if pygame.mouse.get_pressed()[0]:
                            if endNode:
                                endNode.chosen = False

                            node.chosen = True
                            endNode = node      
                else:node.hovered = False 
    screen.fill("black")
    drawGrid()
    drawMenu()
    
    pygame.display.flip()
    clock.tick(60)        