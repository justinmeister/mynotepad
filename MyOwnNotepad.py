import pygame, sys, os, math
from pygame.locals import*

## CONSTANTS, yo ## 

DISPLAYWIDTH  = 640
DISPLAYHEIGHT = 480
FPS          = 30
TEXTHEIGHT   = 20
STARTX       = 0
STARTY       = 0
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
    global FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    
    windowWidth  = 640
    windowHeight = 480 
    lineNumber   = 0
    newChar      = ''
    typeChar     = False
    textString   = ''
    mainList     = []
    mainList.append(textString)
    deleteKey    = False
    returnKey    = False
    insertPoint  = 0
    camerax      = 0
    cameray      = 0
    mouseClicked = False
    mouseX       = 0
    mouseY       = 0
    
    displaySurf = pygame.display.set_mode((windowWidth, windowHeight), RESIZABLE)    
    displaySurf.fill(BGCOLOR)
    displaySurf.convert()
    pygame.display.update()
    
    pygame.display.set_caption('Notepad')
    mainFont = pygame.font.SysFont('Helvetica', TEXTHEIGHT)
    
    cursorRect = getCursorRect(STARTX, STARTY + (TEXTHEIGHT + (TEXTHEIGHT/4)), mainFont, camerax, cameray)
    

## The main game loop detects user input, displays the text on the screen,
## displays the cursor on the screen, and adjusts the camera view if
## necessary.
    
    while True:
        
        
        camerax, cameray = adjustCamera(mainList, lineNumber, insertPoint, cursorRect, mainFont, camerax, cameray, windowWidth, windowHeight)

        newChar, typeChar, deleteKey, returnKey, directionKey, windowWidth, windowHeight, mouseX, mouseY, mouseClicked= getInput(windowWidth, windowHeight)

        if newChar == 'escape':
            mainList = saveAndLoadScreen(mainList, windowWidth, windowHeight, displaySurf, mainFont)
            newChar = False
            insertPoint = 0
            lineNumber = 0
        
        mainList, lineNumber, insertPoint, cursorRect = displayText(mainFont, newChar, typeChar, mainList, deleteKey, returnKey, lineNumber, insertPoint, directionKey, camerax, cameray, cursorRect, windowWidth, windowHeight, displaySurf, mouseClicked, mouseX, mouseY)

        displayInfo(insertPoint, mainFont, cursorRect, camerax, windowWidth, windowHeight, displaySurf)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


## Interprets user input and changes mainList, lineNumber, insertPoint
## and cursorRect accordingly.  There is a function called blitAll()
## which blits all strings to the main surface.

def displayText(mainFont, newChar, typeChar, mainList, deleteKey, returnKey, lineNumber, insertPoint, directionKey, camerax, cameray, cursorRect, windowWidth, windowHeight, displaySurf, mouseClicked, mouseX, mouseY):
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
        
    elif mouseClicked:
        insertPoint, lineNumber, cursorRect = setCursorToClick(mainList, cursorRect, mainFont, camerax, cameray, mouseX, mouseY)

    elif directionKey:
        if directionKey == LEFT:
            if lineNumber == 0:
                if insertPoint > 0:
                    insertPoint -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = STARTY
                    
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
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top
                    
        elif directionKey == UP:
            if lineNumber > 0:
                if insertPoint == 0:
                    lineNumber -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = STARTX
                    cursorRect.y = stringRect.top
                    
                elif insertPoint > len(mainList[lineNumber - 1]):
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
                if insertPoint == 0:
                    lineNumber += 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = STARTX
                    cursorRect.y = stringRect.top
                    
                elif insertPoint > len(mainList[lineNumber + 1]):
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
            cursorRect.y = STARTY
        elif lineNumber > 0:
            cursorRect.y = stringRect.top
        else:
            cursorRect.x = stringRect.right

    if cursorRect.left >= STARTX:
        if cursorRect.right <= windowWidth:
            if cursorRect.top >= STARTY:
                if cursorRect.bottom <= (windowHeight - STARTY):
                    blitAll(mainList, mainFont, camerax, cameray, cursorRect, displaySurf)

    return mainList, lineNumber, insertPoint, cursorRect

##################################################################
## Blits all the strings in mainList to the main surface object 
##################################################################
##################################################################


def blitAll(mainList, mainFont, camerax, cameray, cursorRect, displaySurf):
    displaySurf.fill(BGCOLOR)
    i = 0
    
    for string in mainList:  ##blitting all the strings in the mainList by iterating through them
        stringRender = mainFont.render(string, True, TEXTCOLOR, BGCOLOR)
        stringRect = stringRender.get_rect()
        stringRect.x = STARTX - camerax
        stringRect.y = STARTY + (i * (TEXTHEIGHT + (TEXTHEIGHT/4))) - cameray
        displaySurf.blit(stringRender, stringRect)
        i += 1

    drawCursor(mainFont, cursorRect, displaySurf)


def adjustCamera(mainList, lineNumber, insertPoint, cursorRect, mainFont, camerax, cameray, windowWidth, windowHeight):

    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
    
    if (stringRect.right + cursorRect.width) > windowWidth:
        camerax += (stringRect.right + cursorRect.width) - windowWidth  
    elif cursorRect.left < STARTX:
        camerax -= (-1)*(cursorRect.left)

    if stringRect.bottom > windowHeight:
        cameray += stringRect.bottom - windowHeight
    elif stringRect.top < 0:
        cameray -= (-1)*(stringRect.top)
               
    if insertPoint == 0:
        camerax = 0
    if lineNumber == 0:
        cameray = 0

    return camerax, cameray
    

def drawCursor(mainFont, cursorRect, displaySurf):
    cursor = mainFont.render('l', True, RED, RED)
    displaySurf.blit(cursor, cursorRect)
    

def getInput(windowWidth, windowHeight):
    newChar = False
    typeChar = False
    deleteKey = False
    returnKey = False
    directionKey = False
    mouseX = 0
    mouseY = 0
    mouseClicked = False
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                deleteKey = True
            elif event.key == K_ESCAPE:
                newChar = 'escape'
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

        elif event.type == VIDEORESIZE:
            displaySurf = pygame.display.set_mode(event.dict['size'], RESIZABLE)
            windowWidth = event.dict['w']
            windowHeight = event.dict['h']
            displaySurf.fill(WHITE)
            displaySurf.convert()
            pygame.display.update()
            
           
            
        elif event.type == MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            mouseClicked = True
                
    return newChar, typeChar, deleteKey, returnKey, directionKey, windowWidth, windowHeight, mouseX, mouseY, mouseClicked


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

def displayInfo(insertPoint, mainFont, cursorRect, camerax, windowWidth, windowHeight, displaySurf):
    number = mainFont.render(str(insertPoint), True, TEXTCOLOR, BGCOLOR)
    numbRect = number.get_rect()
    numbRect.bottom = windowHeight
    numbRect.right = windowWidth
    displaySurf.blit(number, numbRect)

    cursor = mainFont.render(str(cursorRect.x) + '  ', True, TEXTCOLOR, BGCOLOR)
    cursorNewRect = cursor.get_rect()
    cursorNewRect.bottom = windowHeight
    cursorNewRect.right = numbRect.left
    displaySurf.blit(cursor, cursorNewRect)

    cameraxRender = mainFont.render(str(camerax) + '    ', True, TEXTCOLOR, BGCOLOR)
    cameraRect = cameraxRender.get_rect()
    cameraRect.bottom = windowHeight
    cameraRect.right = cursorNewRect.left
    displaySurf.blit(cameraxRender, cameraRect)

    windowWidthRender = mainFont.render(str(windowWidth) + '    ', True, TEXTCOLOR, BGCOLOR)
    windowRect = windowWidthRender.get_rect()
    windowRect.bottom = windowHeight
    windowRect.right = cameraRect.left
    displaySurf.blit(windowWidthRender, windowRect)

## These three functions, setCursorToClick(), getLineNumberOfClick(), and
## get insertPointAtMouseX() allow the user to set the cursor location
## by clicking the mouse at the spot they want to go.


def setCursorToClick(mainList, cursorRect, mainFont, camerax, cameray, mouseX, mouseY):
    lineNumber = getLineNumberOfClick(mouseY, cameray, mainList)
    insertPoint = getInsertPointAtMouseX(mouseX, mouseY, lineNumber, mainList, mainFont, camerax, cameray)
    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)

    if insertPoint == 0:
        cursorRect.x = STARTX
    elif insertPoint > 0:
        cursorRect.x = stringRect.right
        
    cursorRect.y = stringRect.top

    return insertPoint, lineNumber, cursorRect


def getLineNumberOfClick(mouseY, cameray, mainList):
    clickLineNumber = (mouseY + cameray) / float(TEXTHEIGHT+ (TEXTHEIGHT/4))
    if clickLineNumber > len(mainList):
        lineNumber = (len(mainList)) - 1
    elif clickLineNumber <= len(mainList):
        floorLineNumber = math.floor(clickLineNumber)
        lineNumber = int(floorLineNumber)

    return lineNumber


def getInsertPointAtMouseX(mouseX, mouseY, lineNumber, mainList, mainFont, camerax, cameray):
    string = mainList[lineNumber]
    newInsertPoint = 0

    if (mouseY + cameray) > ((lineNumber + 1) * (TEXTHEIGHT + TEXTHEIGHT/4)):
        insertPoint = len(mainList[lineNumber])
        return insertPoint
    
    for insertPoint in string:
        stringRect = getStringRectAtInsertPoint(mainList, lineNumber, newInsertPoint, mainFont, camerax, cameray)
        if mouseX >= stringRect.left:
            if mouseX < stringRect.right:
                if newInsertPoint > 0:
                    return newInsertPoint - 1

        newInsertPoint += 1

    else:
        return newInsertPoint


def saveAndLoadScreen(mainList, windowWidth, windowHeight, displaySurf, mainFont):
    messageRender, messageRect = getStringRenderAndRect('Press \'s\' to save, \'o\' to open, \'q\' to quit and \'r\' to continue typing' , mainFont)
    saveFile = False
    openFile = False
    menuWidth  = windowWidth * .94
    menuHeight = windowHeight * .4
    displaySurfRect = displaySurf.get_rect()

    menuRect = pygame.Rect(0, 0, menuWidth, menuHeight)
    menuRect.centerx = displaySurfRect.centerx
    menuRect.centery = displaySurfRect.centery
    pygame.draw.rect(displaySurf, WHITE, menuRect)

    menuBorderRect = menuRect
    pygame.draw.rect(displaySurf, BLUE, menuBorderRect, 5)

    messageRect.centerx = menuRect.centerx
    messageRect.centery = menuRect.centery
    displaySurf.blit(messageRender, messageRect)
    
    pygame.display.update()

    while True:
        saveFile, openFile, continueTyping = saveAndLoadInput()

        if saveFile == True:
            saveString = 'Please enter the directory you wish to save to.'
            saveMessage, saveMessageRect, entryBoxRect = createMenuBox(saveString, mainFont, displaySurf, menuRect, menuBorderRect, menuWidth)
            saveDirectory = False
            directoryString = ''
            
            while saveDirectory == False:
                saveDirectory, directoryString = directoryInput(displaySurf, directoryString, mainFont, menuRect, menuBorderRect, saveMessage, saveMessageRect, entryBoxRect, saveDirectory)
                
            saveToDisk(mainList, saveDirectory)
            break
        
        elif openFile == True:
            loadString = 'Please enter the directory you wish to load from.'
            loadMessage, loadMessageRect, entryBoxRect = createMenuBox(loadString, mainFont, displaySurf, menuRect, menuBorderRect, menuWidth)
            loadDirectory = False
            directoryString = ''

            while loadDirectory == False:
                loadDirectory, directoryString = directoryInput(displaySurf, directoryString, mainFont, menuRect, menuBorderRect, loadMessage, loadMessageRect, entryBoxRect, loadDirectory)

                
            newMainList = loadFromDisk(loadDirectory)
            return newMainList

        elif continueTyping == True:
            break
            

    return mainList


def createMenuBox(messageString, mainFont, displaySurf, menuRect, menuBorderRect, menuWidth):
    message, messageRect = getStringRenderAndRect(messageString, mainFont)
    pygame.draw.rect(displaySurf, WHITE, menuRect)
    pygame.draw.rect(displaySurf, BLUE, menuBorderRect, 5)
    messageRect.centerx = menuRect.centerx
    messageRect.y = menuRect.y + 20

    displaySurf.blit(message, messageRect)

    entryBoxRect = pygame.Rect(0, 0, menuWidth - 10, TEXTHEIGHT+10)

    displayRect = displaySurf.get_rect()
    entryBoxRect.centerx = displayRect.centerx
    entryBoxRect.centery = displayRect.centery
    pygame.draw.rect(displaySurf, BLACK, entryBoxRect, 1)
    pygame.display.update()

    return message, messageRect, entryBoxRect
    

def directoryInput(displaySurf, directoryString, mainFont, menuRect, menuBorderRect, message, messageRect, entryBoxRect, saveOrLoadDirectory):
    directoryList = ''.join(directoryString)

    for event in pygame.event.get():

        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                saveOrLoadDirectory = directoryString
            elif event.key == K_BACKSPACE:
                if directoryList:
                    if len(directoryList) > 0:
                        directoryList = list(directoryString)
                        directoryList.pop()
                        directoryString = ''.join(directoryList)
                    
            else:
                newChar = event.unicode
                directoryList = list(directoryString)
                directoryList.append(newChar)
                directoryString = ''.join(directoryList)
                newChar = False
                saveOrLoadDirectory = False

    directRender, directRect = getStringRenderAndRect(directoryString, mainFont)
    directRect.x = entryBoxRect.x + 4
    directRect.y = entryBoxRect.y + 2
    
    pygame.draw.rect(displaySurf, WHITE, menuRect)
    pygame.draw.rect(displaySurf, BLUE, menuBorderRect, 5)
    pygame.draw.rect(displaySurf, BLACK, entryBoxRect, 1)
    displaySurf.blit(message, messageRect)
    displaySurf.blit(directRender, directRect)
    pygame.display.update()

    return saveOrLoadDirectory, directoryString


def saveToDisk(mainList, saveDirectory):
    saveFile = open(saveDirectory, 'w')

    for string in mainList:
        saveFile.write(string + '\n')

    saveFile.close()


def loadFromDisk(loadDirectory):
    mainList = []
    saveFile = open(loadDirectory, 'r')

    for line in saveFile:
        mainList.append(line)

    saveFile.close()

    i = 0
    while i < len(mainList):
        stringList = list(mainList[i])
        stringList.pop()
        mainList[i] = ''.join(stringList)
        i += 1

    return mainList


def saveAndLoadInput():
    saveFile = False
    openFile = False
    continueTyping = False
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                sys.exit()
            elif event.key == K_s:
                saveFile = True
            elif event.key == K_o:
                openFile = True
            elif event.key == K_r:
                continueTyping = True
                
    return saveFile, openFile, continueTyping

    
def getStringRenderAndRect(string, mainFont):
    stringRender = mainFont.render(string, True, TEXTCOLOR, WHITE)
    stringRect = stringRender.get_rect()

    return stringRender, stringRect


if __name__ == '__main__':
    main()


