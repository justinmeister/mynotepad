import pygame, sys, os
from pygame.locals import*

## CONSTANTS, yo ##

DISPLAYWIDTH  = 640
DISPLAYHEIGHT = 480
FPS          = 30
XMARGIN      = 10
YMARGIN      = 10
TEXTHEIGHT   = 20
STARTX       = XMARGIN
STARTY       = YMARGIN

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

## COLORS ##

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
COMBLUE  = (233, 232, 255)


BGCOLOR = WHITE
TEXTCOLOR = BLACK




def main():
    global DISPLAYSURF, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))    
    DISPLAYSURF.fill(BGCOLOR)
    pygame.display.set_caption('Notepad')
    mainFont = pygame.font.SysFont('Helvetica', TEXTHEIGHT)

    lineNumber = 0
    newChar = ''
    typeChar = True
    textString = ''
    mainList = []
    mainList.append(textString)
    deleteKey = False
    returnKey = False
    insertPoint = 0
    camerax = 0
    cameray = 0
    cursorRect = getCursorRect(STARTX, setCursorY(lineNumber), mainFont, camerax, cameray)
    pygame.display.update()


## The main game loop detects user input, displays the text on the screen,
## displays the cursor on the screen, and adjusts the camera view if
## necessary.
    
    while True:

        newChar, typeChar, deleteKey, returnKey, directionKey = getInput()

        
        mainList, lineNumber, insertPoint, cursorRect, camerax, cameray = displayText(mainFont, newChar, typeChar, mainList, deleteKey, returnKey, lineNumber, insertPoint, directionKey, camerax, cameray, cursorRect)

        displayInsertPoint(insertPoint, mainFont, cursorRect, camerax)

        
        pygame.display.update()
        FPSCLOCK.tick(FPS)



## Interprets user input and changes mainList, lineNumber, insertPoint
## and cursorRect accordingly.  There is a function called blitAll()
## which blits all strings to the main surface.

def displayText(mainFont, newChar, typeChar, mainList, deleteKey, returnKey, lineNumber, insertPoint, directionKey, camerax, cameray, cursorRect):

    camerax, cameray = adjustCamera(mainList, lineNumber, insertPoint, cursorRect, mainFont, camerax, cameray)
    
    if returnKey:
        firstString = getStringAtInsertPoint(mainList, lineNumber, insertPoint)
        secondString = getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
        mainList[lineNumber] = firstString
        mainList.insert(lineNumber+1, secondString)
        lineNumber +=1
        returnKey = False
        insertPoint = 0
        cursorRect.x = STARTX
        stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
        cursorRect.y = stringRect.top


    elif directionKey:
        if directionKey == LEFT:
            if lineNumber == 0:
                if insertPoint > 0:
                    insertPoint -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = YMARGIN
                    
            elif lineNumber > 0:
                if insertPoint == 0:
                    lineNumber -= 1
                    insertPoint = len(mainList[lineNumber])
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top
                    
                elif insertPoint > 0:
                    insertPoint -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)

                    if insertPoint == 0:
                        cursorRect.x = STARTX
                        cursorRect.y = stringRect.top
                    else:
                        cursorRect.x = stringRect.right
                        cursorRect.y = stringRect.top
                    
                    

        elif directionKey == RIGHT:
            if insertPoint < len(mainList[lineNumber]):
                insertPoint += 1
                stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                cursorRect.x = stringRect.right
                cursorRect.y = stringRect.top

            elif insertPoint >= len(mainList[lineNumber]):
                if len(mainList) > (lineNumber + 1):
                    lineNumber += 1
                    insertPoint = 0
                    cursorRect.x = STARTX
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.y = stringRect.top
                    
                

        elif directionKey == UP:
            if lineNumber > 0:
                if insertPoint > len(mainList[lineNumber - 1]):
                    lineNumber -= 1
                    insertPoint = len(mainList[lineNumber])
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top
                    
                    
                elif insertPoint <= len(mainList[lineNumber -1]):
                    lineNumber -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top
                    
                    

        elif directionKey == DOWN:
            if lineNumber + 1 < len(mainList):
                if insertPoint > len(mainList[lineNumber + 1]):
                    lineNumber +=1
                    insertPoint = len(mainList[lineNumber])
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top
                elif insertPoint <= len(mainList[lineNumber +1]):
                    lineNumber += 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top
                    
                    

    elif typeChar:
        string = mainList[lineNumber]
        stringList = list(string)
        stringList.insert(insertPoint, newChar)
        newString = ''.join(stringList)
        mainList[lineNumber] = newString
        
        typeChar = False

        if len(newString) > len(string) and newChar != '    ':   ## Prevents alteration keys like shifts from affecting the insertPoint ##
            insertPoint += 1
            stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
            cursorRect.x = stringRect.right
            cursorRect.y = stringRect.top
            
        elif newChar == '    ':
            insertPoint += 4
            stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
            cursorRect.x = stringRect.right
            cursorRect.y = stringRect.top



    elif deleteKey:
        
        if insertPoint > 0:
            firstString = getStringAtInsertPoint(mainList, lineNumber, insertPoint)
            secondString = getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
            stringList = list(firstString)
            del stringList[insertPoint-1]
            string = ''.join(stringList)
            string += secondString
            mainList[lineNumber] = string

            deleteKey = False
            insertPoint -= 1
            stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
            cursorRect.x = stringRect.right
            cursorRect.y = stringRect.top
                    
                    
        elif insertPoint <= 0:
            if lineNumber > 0:
                string = getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
                del mainList[lineNumber]
                lineNumber -= 1
                mainList[lineNumber] += string
                
                deleteKey = False
                insertPoint = len(mainList[lineNumber]) - len(string)
                stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)                
                cursorRect.x = stringRect.right
                cursorRect.y = stringRect.top

    else:
        stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
        if insertPoint == 0:
            cursorRect.x = STARTX
        elif insertPoint > 0:
            cursorRect.x = stringRect.right
        if lineNumber == 0:
            cursorRect.y = YMARGIN
        elif lineNumber > 0:
            cursorRect.y = stringRect.top
        else:
            cursorRect.x = stringRect.right


    
    
    if cursorRect.left >= XMARGIN:
        if cursorRect.right <= (DISPLAYWIDTH - XMARGIN):
            if cursorRect.top >= YMARGIN:
                if cursorRect.bottom <= (DISPLAYHEIGHT - YMARGIN):
                    blitAll(mainList, mainFont, camerax, cameray, cursorRect)

    

    return mainList, lineNumber, insertPoint, cursorRect, camerax, cameray


##################################################################
## Blits all the strings in mainList to the main surface object 
##################################################################
##################################################################


def blitAll(mainList, mainFont, camerax, cameray, cursorRect):
    DISPLAYSURF.fill(BGCOLOR)


    i = 0
    for string in mainList:  ##blitting all the strings in the mainList by iterating through them
        stringRender = mainFont.render(string, True, TEXTCOLOR, BGCOLOR)
        stringRect = stringRender.get_rect()
        stringRect.x = STARTX - camerax
        stringRect.y = STARTY + (i * (TEXTHEIGHT + (TEXTHEIGHT/4))) - cameray
        DISPLAYSURF.blit(stringRender, stringRect)
        i += 1

    drawCursor(mainFont, cursorRect)


    


def adjustCamera(mainList, lineNumber, insertPoint, cursorRect, mainFont, camerax, cameray):

    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
    
    
    if (stringRect.right + cursorRect.width) > (DISPLAYWIDTH - XMARGIN):
        camerax += ((stringRect.right + cursorRect.width) - (DISPLAYWIDTH - XMARGIN))
        

    elif cursorRect.left < XMARGIN:
        if camerax > 0:
            if cursorRect.left < 0:
                adjustAmount = ((-1)*(cursorRect.left)) + XMARGIN
                camerax -= adjustAmount
            elif cursorRect.left > 0:
                adjustAmount = XMARGIN - cursorRect.left
                camerax -= adjustAmount
        elif camerax < 0:
            camerax = 0

    if ((stringRect.bottom > (DISPLAYHEIGHT - YMARGIN))):
        cameray += (stringRect.bottom) - (DISPLAYHEIGHT - YMARGIN)

    elif (stringRect.top < YMARGIN):
        if stringRect.top < 0:
            cameray -= (-1)*(stringRect.top) + YMARGIN
        else:
            cameray -= YMARGIN - stringRect.top
          

    if insertPoint == 0:
        camerax = 0

    if lineNumber == 0:
        cameray = 0

    return camerax, cameray
    




def drawCursor(mainFont, cursorRect):

    cursor = mainFont.render('l', True, RED, RED)

    DISPLAYSURF.blit(cursor, cursorRect)
    




def getInput():
    
    newChar = False
    typeChar = False
    deleteKey = False
    returnKey = False
    directionKey = False
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                deleteKey = True

            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                
            elif event.key == K_RETURN:
                returnKey = True
                
            elif event.key == K_TAB:
                newChar = '    '
                typeChar = True

            elif event.key == K_LEFT:
                directionKey = LEFT

            elif event.key == K_RIGHT:
                directionKey = RIGHT

            elif event.key == K_UP:
                directionKey = UP

            elif event.key == K_DOWN:
                directionKey = DOWN
            
            else:
                newChar = event.unicode
                typeChar = True
                
                

    return newChar, typeChar, deleteKey, returnKey, directionKey


## These functions involve the string the cursor happens to be on.
## By using the lineNumber, the program knows which string to
## manipulate.  lineNumber = 0 is the first line, and so on.
## The cursor's left position is always locked to the right of whatever
## stringRect it is next to.



def getStringRect(string, lineNumber, camerax, cameray):
    stringRect = string.get_rect()
    stringRect.x = STARTX - camerax
    stringRect.y = STARTY + (lineNumber * (TEXTHEIGHT + (TEXTHEIGHT/4))) - cameray

    return stringRect



def getStringAtInsertPoint(mainList, lineNumber, insertPoint):
    string = mainList[lineNumber]
    stringList = list(string)
    newStringList = stringList[0:insertPoint]
    newString = ''.join(newStringList)

    return newString

def getStringAfterInsertPoint(mainList, lineNumber, insertPoint):
    string = mainList[lineNumber]
    stringList = list(string)
    newStringList = stringList[insertPoint:]
    newString = ''.join(newStringList)

    return newString


def getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray):
    string = getStringAtInsertPoint(mainList, lineNumber, insertPoint)
    stringRender = mainFont.render(string, True, TEXTCOLOR, BGCOLOR)
    stringRect = getStringRect(stringRender, lineNumber, camerax, cameray)

    return stringRect



## Miscelaneous Functions.  getCursorRect is used to produce the
## cursors's rect object.


def getCursorRect(cursorX, cursorY, mainFont, camerax, cameray):
    cursor = mainFont.render('L', True, RED)
    cursorRect = cursor.get_rect()
    cursorRect.x = cursorX - camerax
    cursorRect.y = cursorY - cameray

    return cursorRect


def displayInsertPoint(insertPoint, mainFont, cursorRect, camerax):
    number = mainFont.render(str(insertPoint), True, TEXTCOLOR, BGCOLOR)
    numbRect = number.get_rect()
    numbRect.bottom = DISPLAYHEIGHT
    numbRect.right = DISPLAYWIDTH

    DISPLAYSURF.blit(number, numbRect)

    cursor = mainFont.render(str(cursorRect.x) + '  ', True, TEXTCOLOR, BGCOLOR)
    cursorNewRect = cursor.get_rect()
    cursorNewRect.bottom = DISPLAYHEIGHT
    cursorNewRect.right = numbRect.left

    DISPLAYSURF.blit(cursor, cursorNewRect)

    camerax = mainFont.render(str(camerax) + '    ', True, TEXTCOLOR, BGCOLOR)
    cameraRect = camerax.get_rect()
    cameraRect.bottom = DISPLAYHEIGHT
    cameraRect.right = cursorNewRect.left

    DISPLAYSURF.blit(camerax, cameraRect)


def setCursorY(lineNumber):
    y = STARTY + (lineNumber * (TEXTHEIGHT + (TEXTHEIGHT/4)))
    return y



if __name__ == '__main__':
    main()


