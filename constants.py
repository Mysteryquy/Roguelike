import pygame

pygame.init()

GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

#Mapvars
MAP_WIDTH = 30
MAP_HEIGHT = 30




#Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)


#game colors
COLOR_DEFAULT_BG = COLOR_GREY


#SPRITES
S_PLAYER = pygame.image.load("data/python.png")
S_WALL = pygame.image.load("data/wall1.png")
S_FLOOR = pygame.image.load("data/floor.jpg")
S_ENEMY = pygame.image.load("data/enemy1.png")