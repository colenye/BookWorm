import pygame
import random
import sys
from classes import moveBox, playerUnit, gridTile,red, blue, green, pink, darkBrown, brown, black, white
from typing import List

##text funciton
def drawText(text: str, font: pygame.font, color: tuple, pos: tuple, screen: pygame.display):
    words = font.render(text, True, color)
    screen.blit(words, pos)

##Screen functions
def drawMenu(title: str, font: pygame.font, screen: pygame.display, playRect: pygame.rect, sWidth: int):
    drawText(title,font,white, (sWidth // 2 - len(title * 10), 50), screen)
    pygame.draw.rect(screen,white,playRect)

##Spawn book
def spawnBook(playerDiameter,playerList):
    spawnedBook = False
    while (not spawnedBook):
        xShift = random.randint(0,16) * playerDiameter
        yShift = random.randint(0,16) * playerDiameter
        bookRect = pygame.Rect(300 + xShift, 50 + yShift, playerDiameter, playerDiameter)
        spawnedBook = True
        for player in playerList:
            if player.rect.colliderect(bookRect):
                spawnedBook = False
    return bookRect

##Init Grid
def initGrid(width: int, height: int,gridList: List[gridTile], gridWidth: int,gridHeight: int):
    boxWidth = gridWidth / width
    boxHeight = gridHeight / height
    ##Draws grid with alternating light/dark brown squares
    for i in range (width):
        gridList.append([])
        for j in range (height):
            if i % 2 == 0:
                if j % 2 == 0:
                    col = darkBrown
                else:
                    col = brown
            else:
                if j % 2 == 0:
                    col = brown
                else:
                    col = darkBrown
            box = gridTile(300 + boxWidth * i, 50 + boxHeight * j, boxWidth,col)
            gridList[i].append(box)