import pygame, sys
from pygame.locals import *
pygame.init()
DISPLAYSURF = pygame.display.set_mode((600,600))
pygame.display.set_caption('Hello World')
pygame.draw.circle(DISPLAYSURF, (255, 255, 255), (15,15), 15)

grid = 20
gridWidth = DISPLAYSURF.get_width() / grid
gridHeight = DISPLAYSURF.get_height() / grid

for i in range(grid):
    pygame.draw.line(DISPLAYSURF, (255,255,255), (i*gridWidth, 0), (i*gridWidth, DISPLAYSURF.get_height()))

for j in range(grid):
    pygame.draw.line(DISPLAYSURF, (255,255,255), (0, j*gridHeight), (DISPLAYSURF.get_width(), j*gridHeight))

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()