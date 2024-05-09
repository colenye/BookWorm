import pygame
import random
import sys

class moveBox:
    def __init__(self, left, top, width, direction,playerToMove):
        self.left = left
        self.top = top
        self.width = width
        self.direction = direction
        self.playerToMove = 0
        self.rect = pygame.Rect(left,top,width,width)

class playerUnit:
    def __init__(self, left,top,width,direction):
        self.X = left
        self.Y = top
        self.width = width
        self.direction = direction
        self.rect = pygame.Rect(left,top,width,width)

class gridTile:
    def __init__(self,left,top,width,color):
        self.X = left
        self.Y = top
        self.width = width
        self.color = color
        self.rect = pygame.Rect(left,top,width,width)
        #self.containsHead = containsHead
        

##RGBS
red = (100,0,0)
green = (0,100,0)
blue = (0,0,100)
white = (255,255,255)
black = (0,0,0)
darkBrown = (123, 63, 0)
brown = (210, 125, 45)
pink = (255,105,180)