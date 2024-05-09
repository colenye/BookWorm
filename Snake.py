import pygame
import random
import sys
from classes import moveBox, playerUnit, gridTile,red, blue, green, pink, darkBrown, brown, black, white
from functions import drawMenu,drawText,spawnBook,initGrid
from typing import List

##Initialization
pygame.init()
clock = pygame.time.Clock()

##Screen
sWidth , sHeight = 1280 , 720
screen = pygame.display.set_mode((sWidth,sHeight))

##Title and display
title = "Book Worm"
pygame.display.set_caption(title)

##Buttons
playRect = pygame.Rect(1280/2-150,500,300,100)

##Fonts
font = pygame.font.Font(None,50)
arial = pygame.font.SysFont("Arial",50)

##States
gameRunning = True
gameState = "Menu"

##Grid properties    
gridWidth = 600
gridHeight = 600
gridSquares = 17

##Player properties
playerList = []
playerDiameter = (gridHeight/gridSquares)
playerSpeed = 5

##Images
glasses = pygame.image.load('Glasses.png')
scaledGlasses = pygame.transform.scale(glasses, (playerDiameter, playerDiameter))
buckTeeth = pygame.image.load('BuckTeeth.png')
scaledBuckTeeth = pygame.transform.scale(buckTeeth, (playerDiameter, playerDiameter))
bookPNG = pygame.image.load('Book.png')
scaledBook = pygame.transform.scale(bookPNG, (playerDiameter, playerDiameter))

##Head of the players starting point
initPlayerX = 300 - 10 + 4 * playerDiameter
initPlayerY = 50 + 8 * playerDiameter

##Bounds of box
maxR = 900 + 5
maxL = 300 - 5
maxD = 650 + 5
maxU = 50 - 5

##List of movement change boxes
boxList = []
books = []
gridList = []
bookOn = False
canMakeBox = True

##Function to start game
def startGame():
    ##Reset the lsits
    global gridList,playerList,books,bookOn,boxList
    gridList = []
    boxList = []
    playerList = []
    books = []
    bookOn = False
    initGrid(gridSquares,gridSquares,gridList,gridWidth,gridHeight)

    ##Make first three boxes, and add them to the player list
    player1 = playerUnit(initPlayerX,initPlayerY,playerDiameter,"")
    player2 = playerUnit(initPlayerX - playerDiameter,initPlayerY,playerDiameter,"")
    player3 = playerUnit(initPlayerX - playerDiameter * 2,initPlayerY,playerDiameter,"")
    playerList.append(player1)
    playerList.append(player2)
    playerList.append(player3)
    screen.fill(black)
    pygame.display.update()

##Function to draw grid
def drawGame(width: int, height: int, gridList: List[gridTile]):
    for i in range (width):
        for j in range(height):
            pygame.draw.rect(screen,gridList[i][j].color,gridList[i][j].rect)
    for playerBox in playerList:
        playerBox.rect = pygame.Rect(playerBox.X,playerBox.Y,playerDiameter,playerDiameter)
        pygame.draw.rect(screen,pink,playerBox.rect)
    #for book in books:
        #pygame.draw.rect(screen,green,book)
    screen.blit(scaledBuckTeeth,(playerList[0].X,playerList[0].Y + 7))
    screen.blit(scaledGlasses,(playerList[0].X,playerList[0].Y - 7))
    if books != []:
        screen.blit(scaledBook,(books[0].left,books[0].top))



##Self hit
def checkSelfHit():
    global playerList
    playerHead = playerList[0]
    for player in playerList[3:]:
        if playerHead.rect.colliderect(player.rect):
            return True
    return False

##Change direction function
def changeDirection (currentDir: str, nextDir: str, playerHead: playerUnit) -> pygame.rect:
    ##Globals
    global playerDiameter, playerSpeed, maxL, maxD, maxR, maxU, canMakeBox

    ##Check if input is valid
    if (currentDir == "l" or currentDir == "r") and (nextDir == "l" or nextDir == "r"):
        return
    if (currentDir == "u" or currentDir == "d") and (nextDir == "d" or nextDir == "u"):
        return
    if (currentDir == "" and nextDir == "l"):
        return
    
    else:
        ##Pressed up or down while moving right
        if currentDir == "r":
            test = maxL + 5
            while playerHead.X > test:
                test += playerDiameter
            hello = moveBox(test,playerHead.Y,playerDiameter,nextDir,(len(playerList)))
            return hello
        
        ##Pressed up or down while moving left
        elif currentDir == "l" or currentDir == "":
            test = maxR - 5
            while playerHead.X < test:
                test -= playerDiameter
            hello = moveBox(test,playerHead.Y,playerDiameter,nextDir, (len(playerList)))
            return hello

        ##Pressed right or left while moving up
        elif currentDir == "u" or currentDir == "":
            test = maxD - 5 
            while playerHead.Y < test:
                test -= playerDiameter
            hello = moveBox(playerHead.X,test,playerDiameter,nextDir,(len(playerList)))
            return hello

        ##Pressed right or left while moving upww
        else:
            test = maxU + 5
            while playerHead.Y > test:
                test += playerDiameter
            hello = moveBox(playerHead.X,test,playerDiameter,nextDir,(len(playerList)))
            return hello

##Game loop
while gameRunning:
    ##FPS and mouse
    clock.tick(60)
    mouseX,mouseY = pygame.mouse.get_pos()
    ##print(mouseX,mouseY)

    ##Pygame eventsa
    for event in pygame.event.get():
        ##Exit button
        if event.type == pygame.QUIT:
            gameRunning = False

        ##Play button
        elif event.type == pygame.MOUSEBUTTONDOWN and gameState == "Menu":
            if playRect.collidepoint((mouseX,mouseY)):
                startGame()
                gameState = "Game"
    
    ##Menu
    if gameState == "Menu":
        screen.fill(black)
        drawMenu(title,font,screen,playRect,sWidth)
        pygame.display.update()

    ##Gameplay
    if gameState == "Game":
        
        ##Draw grid and update
        screen.fill(black)
        drawGame(gridSquares,gridSquares,gridList)
        pygame.display.update()

        ##Head of worm
        playerHead = playerList[0]

        ##Check to see if we should place a book
        if bookOn == False:
            books.append(spawnBook(playerDiameter,playerList))
            bookOn = True
        

        ##Move
        for playerBox in playerList:
            if playerBox.direction == "u":
                playerBox.Y -= playerSpeed
            elif playerBox.direction == "d":
                playerBox.Y  += playerSpeed
            elif playerBox.direction == "l":
                playerBox.X -= playerSpeed
            elif playerBox.direction == "r":
                playerBox.X += playerSpeed

        ##End game
        if playerHead.X + playerDiameter > maxR:
            gameState = "Menu"
        if playerHead.X < maxL:
            gameState = "Menu"
        if playerHead.Y < maxU:
            gameState = "Menu"
        if playerHead.Y + playerDiameter > maxD:
            gameState = "Menu"

        if checkSelfHit():
            gameState = "Menu"

        ##keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            newBox = (changeDirection(playerHead.direction,"u", playerHead))
            if type(newBox) == moveBox and (boxList == [] or newBox.direction != boxList[-1].direction):
                boxList.append(newBox)
        elif keys[pygame.K_a]:
            newBox = (changeDirection(playerHead.direction,"l", playerHead))
            if type(newBox) == moveBox and (boxList == [] or newBox.direction != boxList[-1].direction):
                boxList.append(newBox)
        elif keys[pygame.K_s]:
            newBox = (changeDirection(playerHead.direction,"d", playerHead))
            if type(newBox) == moveBox and (boxList == [] or newBox.direction != boxList[-1].direction):
                boxList.append(newBox)
        elif keys[pygame.K_d]:
            newBox = (changeDirection(playerHead.direction,"r", playerHead))
            if type(newBox) == moveBox and (boxList == [] or newBox.direction != boxList[-1].direction):
                boxList.append(newBox)

        ##Book and knoweldge gain
        if playerHead.rect.colliderect(books[0]):
            books.remove(books[0])
            bookOn = False
            lastPlayer = playerList[-1]
            if lastPlayer.direction == "r":
                newPlayerY = lastPlayer.Y
                newPlayerX = lastPlayer.X - playerDiameter
                playerList.append(playerUnit(newPlayerX,newPlayerY,playerDiameter,lastPlayer.direction))
            elif lastPlayer.direction == "l":
                newPlayerY = lastPlayer.Y
                newPlayerX = lastPlayer.X + playerDiameter
                playerList.append(playerUnit(newPlayerX,newPlayerY,playerDiameter,lastPlayer.direction))
            elif lastPlayer.direction == "u":
                newPlayerX = lastPlayer.X
                newPlayerY = lastPlayer.Y + playerDiameter
                playerList.append(playerUnit(newPlayerX,newPlayerY,playerDiameter,lastPlayer.direction))
            elif lastPlayer.direction == "d":
                newPlayerX = lastPlayer.X
                newPlayerY = lastPlayer.Y - playerDiameter
                playerList.append(playerUnit(newPlayerX,newPlayerY,playerDiameter,lastPlayer.direction))

        ##Changing direction of worm
        for box in boxList:
            p2m = playerList[box.playerToMove]
            ##pygame.draw.rect(screen,blue,box.rect)
            if p2m.direction == "r":
                if p2m.Y == box.top and p2m.X >= box.left and p2m.direction != box.direction:
                    p2m.X = box.left
                    p2m.direction = box.direction
                    box.playerToMove += 1
                    if p2m == playerList[-1]:
                        boxList.remove(box)
            elif p2m.direction == "l":
                if p2m.Y == box.top and p2m.X <= box.left and p2m.direction != box.direction:
                    p2m.X = box.left
                    p2m.direction = box.direction
                    box.playerToMove += 1
                    if p2m == playerList[-1]:
                        boxList.remove(box)
            elif p2m.direction == "d":
                if p2m.Y >= box.top and p2m.X == box.left and p2m.direction != box.direction:
                    p2m.Y = box.top
                    p2m.direction = box.direction
                    box.playerToMove += 1
                    if p2m == playerList[-1]:
                        boxList.remove(box)
            elif p2m.direction == "u":
                if p2m.Y <= box.top and p2m.X == box.left and p2m.direction != box.direction:
                    p2m.Y = box.top
                    p2m.direction = box.direction
                    box.playerToMove += 1
                    if p2m == playerList[-1]:
                        boxList.remove(box)
            elif playerHead.direction == "" :
                for player in playerList:
                    player.direction = "r"
                    boxList = []
        pygame.display.update()

pygame.quit()
sys.exit()