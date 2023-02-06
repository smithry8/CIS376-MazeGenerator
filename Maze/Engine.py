import pygame, sys
import copy
import Scene
# The game Engine
FRAME_RATE = 60
clock = pygame.time.Clock()
class Engine:
    def __init__(self, scene):
        self.scene = scene
        pygame.init()
        pygame.display.set_caption('Ryan and Ian Maze Generator / Solver')
        self._running = False
        self._screen = scene.DISPLAYSURF
    def loop(self):
        self._running = True
        while self._running:
            events = pygame.event.get()
            # used to check if the player has reached the bottom right tile for win
            # if (player.x >= (gridSize - 2) * tileSize) and (player.y >= (gridSize - 2) * tileSize):
            #     winGame()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
            #     #Handle the Movement of the player
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            #             if collisionDetector(player.x + tileSize, player.y)[1] == False and player.x + tileSize < DISPLAYSURF.get_width():
            #                 player.x += tileSize
            #                 player.position = (player.x,player.y)
            #         elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            #             if collisionDetector(player.x - tileSize, player.y)[1] == False and player.x - tileSize >= 0:
            #                 player.x -= tileSize
            #                 player.position = (player.x,player.y)
            #         elif event.key == pygame.K_UP or event.key == pygame.K_w:
            #             if collisionDetector(player.x, player.y - tileSize)[1] == False and player.y - tileSize >= 0:
            #                 player.y -= tileSize
            #                 player.position = (player.x,player.y)
            #         elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            #             if collisionDetector(player.x, player.y + tileSize)[1] == False and player.y + tileSize < DISPLAYSURF.get_height():
            #                 player.y += tileSize
            #                 player.position = (player.x,player.y)
            #         if event.key == pygame.K_q:
            #             quitGame()
            #     if event.type == pygame.MOUSEBUTTONUP:
            #         print("THIS WORKED")
            #         pos = pygame.mouse.get_pos()
            #         result = collisionDetector(pos[0],pos[1])
            #         grid[result[0].row][result[0].col].alive = not grid[result[0].row][result[0].col].alive
            # #calls one cycle every frame
            # if(not stable):
            self.gridBuffer = copy.deepcopy(self.scene.grid)
            for updateables in self.scene.updateable:
                updateables.Update()
            self.grid = self.gridBuffer
            self.scene.render()
            #limits frame rate to the FRAME_RATE constant
            clock.tick(FRAME_RATE)