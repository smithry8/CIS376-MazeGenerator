#Created by Ian O'Strander
import Updateable
# A class that holds information about the player
class Player(Updateable.Updateable):
    def __init__(self, x, y, color = (255,255,255)):
        self.position = (x,y)
        self.color = color
        self.x = x
        self.y = y

    def Update(self):
        pass

    # if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
    #     if collisionDetector(player.x + tileSize, player.y)[
    #         1] == False and player.x + tileSize < DISPLAYSURF.get_width():
    #         player.x += tileSize
    #         player.position = (player.x, player.y)
    # elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
    #     if collisionDetector(player.x - tileSize, player.y)[1] == False and player.x - tileSize >= 0:
    #         player.x -= tileSize
    #         player.position = (player.x, player.y)
    # elif event.key == pygame.K_UP or event.key == pygame.K_w:
    #     if collisionDetector(player.x, player.y - tileSize)[1] == False and player.y - tileSize >= 0:
    #         player.y -= tileSize
    #         player.position = (player.x, player.y)
    # elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
    #     if collisionDetector(player.x, player.y + tileSize)[
    #         1] == False and player.y + tileSize < DISPLAYSURF.get_height():
    #         player.y += tileSize
    #         player.position = (player.x, player.y)