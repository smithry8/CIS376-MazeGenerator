import json
import sys

sys.path.append("../")

from GameEngine.Engine import engine
import GameEngine.GameObject as go
import GameEngine.Scene as scn
import pygame as pg
from Box2D import *
import random

w2b = 1 / 100
b2w = 100
gravity = b2Vec2(0, -10.0)
world = b2World(gravity, doSleep=False)

timeStep = 1.0 / 60
vel_iters, pos_iters = 6, 2


class Ground(go.DGameObject):
    def __init__(self, x, y, w, h, tag = "", collidable = False):
        super().__init__(x, y, w, h, tag, collidable)
        self.body = world.CreateStaticBody(position=(x, y), shapes=b2PolygonShape(box=(w, h)))
        self.image = pg.Surface((w * b2w, h * b2w))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2w, 768 - self.body.position.y * b2w
        groundGroup.add(self)

    def Draw(self):
        pass


class Bullet(go.DUGameObject):
    def __init__(self, x = 0, y = 0, w = 0.2, h = 0.2, tag = "", collidable = False):
        super().__init__(x, y, w, h, tag, collidable)
        self.body = world.CreateDynamicBody(position=(player.body.position.x, player.body.position.y), gravityScale = 0.0)
        shape = b2PolygonShape(box=(w/2, h/2))
        self.fixDef = b2FixtureDef(shape=shape, density=.5)
        self.fixDef.filter.categoryBits = 0x0003
        self.fixDef.filter.maskBits &= ~0x0002
        self.fixDef.filter.maskBits &= ~0x0003
        self.box = self.body.CreateFixture(self.fixDef)
        self.dirty = 2
        d = .5 * b2w
        self.image = pg.Surface((d, d), pg.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        pg.draw.circle(self.image, (0, 101, 164), self.rect.center, w/2 * b2w)
        self.velocity = b2Vec2(player.direction * 0.05, 0)
    def Update(self):
        self.rect.center = self.body.position[0] * b2w, 770 - self.body.position[1] * b2w
        enemyCollisions = pg.sprite.spritecollide(self, enemyGroup, False)
        groundCollisions = pg.sprite.spritecollide(self, groundGroup, False)
        collided = len(enemyCollisions) + len(groundCollisions)
        if collided > 0:
            updater.remove(self)
        self.body.ApplyLinearImpulse(self.velocity, self.body.position, True)

    def Draw(self):
        pass

class Camera(go.UGameObject):
    def __init__(self, x = 0, y = 0, w = 0.2, h = 0.2, tag = "", collidable = False):
        super().__init__(x, y, w, h, tag, collidable)
        self.offset_x = 0
        self.offset_y = 0
        self.offset_float_x = 0
        self.offset_float_y = 0
        self.DISPLAY_W = engine._screen.get_width()
        self.DISPLAY_H = engine._screen.get_height()
        self.CONST_x = -self.DISPLAY_W / 2 + player.rect.center[0] / 2
        self.CONST_y = 400
    def Update(self):
        x = player.rect.x
        y = player.rect.y - player.rect.height
        self.offset_float_x += (x - self.offset_float_x + self.CONST_x)
        self.offset_float_y += (y - self.offset_float_y - self.CONST_y)
        self.offset_x, self.offset_y = int(self.offset_float_x), int(self.offset_float_y)


class Player(go.DUGameObject):
    def __init__(self, x, y, w, h, tag = "", collidable = False):
        super().__init__(x, y, w, h, tag, collidable)
        self.body = world.CreateDynamicBody(position=(x, y))
        shape = b2PolygonShape(box=(w/2, h/2))
        self.fixDef = b2FixtureDef(shape=shape)
        self.fixDef.filter.categoryBits = 0x0002
        self.box = self.body.CreateFixture(self.fixDef)
        self.dirty = 2
        self.image = pg.Surface((w * b2w, h * b2w), pg.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.body.mass = 1.0
        pg.draw.rect(self.image, (0, 101, 164), (x- w/2, y - h/2, w * b2w, h * b2w))
        self.inputs = {
            'left' : False,
            'right' : False,
            'space' : False,
            'shoot' : False
        }
        self.maxSpeed = 2
        self.hasJump = True
        self.isGrounded = False
        self.jumpHeight = 15
        self.jumpDuration = 0
        self.direction = 1
        self.timeSinceShot = pg.time.get_ticks()
        self.weaponCoolDown = 0.3

    def Update(self):
        currentTime = pg.time.get_ticks()
        self.rect.center = self.body.position[0] * b2w, 771  - self.body.position[1] * b2w
        collided = pg.sprite.spritecollide(self, groundGroup, False)
        self.timeSinceShot += 1
        if(len(collided) > 0):
            self.isGrounded = True
            self.hasJump = True
        else:
            self.isGrounded = False
        for event in engine.keyboardInputs:
            self.handleEvent(event)
            if event.type == pg.KEYDOWN:
                if self.isGrounded and event.key == pg.K_SPACE:
                    self.body.ApplyLinearImpulse(b2Vec2(0, self.jumpHeight), self.body.position, True)
                if event.key == pg.K_j and (currentTime - self.timeSinceShot) / 1000 > self.weaponCoolDown:
                    print(currentTime - self.timeSinceShot)
                    updater.add(Bullet(), projectileGroup)
                    self.timeSinceShot = pg.time.get_ticks()
        velocity = self.body.linearVelocity
        speed = velocity.length
        self.handleJump(velocity, speed)
        self.handleMovement(velocity,speed)

    def handleJump(self, velocity, speed):
        if self.hasJump and self.inputs['space']:
            self.jumpDuration += 1
            if(self.jumpDuration >= self.jumpHeight):
                self.hasJump = False
                self.jumpDuration = 0
            if velocity.y > self.jumpHeight:
                self.body.linearVelocity.y = self.maxSpeed * velocity.y / speed
            else:
                self.body.ApplyLinearImpulse(b2Vec2(0, 0.5), self.body.position, True)
    def handleMovement(self, velocity, speed):
        if self.inputs['left'] or self.inputs['right']:
            if abs(velocity.x) > self.maxSpeed:
                self.body.linearVelocity.x = self.maxSpeed * velocity.x / speed
            else:
                self.body.ApplyLinearImpulse((self.direction * self.maxSpeed, 0), self.body.worldCenter, True)
    def Draw(self):
        pass

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.inputs['space'] = True
            if event.key == pg.K_j:
                self.inputs['shoot'] = True
            if event.key == pg.K_a:
                self.inputs['left'] = True
                self.direction = -1
            elif event.key == pg.K_d:
                self.inputs['right'] = True
                self.direction = 1
        elif event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                self.inputs['space'] = False
                self.hasJump = False
                self.jumpDuration = 0
            if event.key == pg.K_j:
                self.inputs['shoot'] = False
            if event.key == pg.K_a:
                self.inputs['left'] = False
                self.body.linearVelocity.x = 0
            elif event.key == pg.K_d:
                self.inputs['right'] = False
                self.body.linearVelocity.x = 0

class Enemy(go.DUGameObject):
    def __init__(self, x, y, w, h, tag = "", collidable = False):
        super().__init__(x, y, w, h, tag, collidable)
        self.body = world.CreateDynamicBody(position=(x, y))
        shape = b2PolygonShape(box=(w/2, h/2))
        self.fixDef = b2FixtureDef(shape=shape)
        self.fixDef = b2FixtureDef(shape=shape)
        self.fixDef.filter.maskBits = 0xFFFF
        self.fixDef.filter.categoryBits = 0x0001
        self.box = self.body.CreateFixture(self.fixDef)
        self.dirty = 2
        self.image = pg.Surface((w * b2w, h * b2w), pg.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.body.mass = 1.0
        pg.draw.rect(self.image, (101, 0, 164), (x- w/2, y - h/2, w * b2w, h * b2w))
        self.maxSpeed = 2
    def Update(self):
        self.rect.center = self.body.position[0] * b2w, 771 - self.body.position[1] * b2w
    def Draw(self):
        pass


class Updater(go.UGameObject):
    def __init__(self, x, y, w, h, tag = "", collidable = False):
        super().__init__(x, y, w, h, tag, collidable)

    def Update(self):
        world.Step(timeStep, vel_iters, pos_iters)
        world.ClearForces()

    def remove(self, object, group = None):
        if group is not None:
            group.remove(object)
        object.body.DestroyFixture(object.box)
        world.DestroyBody(object.body)
        object.kill()
        engine.destroy(object)

    def add(self, object, group):
        engine.currentScene.all_sprites.remove(group)
        if group is not None:
            group.add(object)
        engine.spawn(object)
        engine.currentScene.all_sprites.append(group)

class Tile(go.DUGameObject):
    def __init__(self, x=0, y=0, w=0, h=0, tag="", collidable=False):
        super().__init__(x, y, w, h, tag, collidable)
        self.body = world.CreateStaticBody(position=(x * w2b, y * w2b), shapes=b2PolygonShape(box=(w * w2b, h * w2b)))
        groundGroup.add(self)
    def Draw(self):
        pass
    def Update(self):
        # print(self.rect.x)
        pass

def loadGame():
    file = open("newmap.tmj")
    level = json.load(file)
    level = level['layers'][0]['data']
    sprites = []
    width = 100
    wall = pg.image.load("./assets/DungeonTileset/frames/wall_mid.png")
    t = Tile()
    t.image = pg.Surface((64, 64), pg.SRCALPHA)
    wall = pg.transform.scale(wall, (64, 64))
    t.image.blit(wall, (0, 0))
    t.rect = t.image.get_rect()
    sprites.append(t)
    sprites.append(wall)
    i = 0
    j = 0
    for tile in range(len(level)):
        before = i
        if (not (i := tile % width)) and before != 0:
            j += 1
        print(i, j)
        if level[(j * width) + i] != 0:
            w = i * 64
            h = j * 64
            t = Tile(w, h, 64,64)
            t.image = sprites[0].image
            t.rect = t.image.get_rect()
            t.rect = pg.Rect(w, h, 64, 64)
            # t = Ground(w * w2b, h * w2b, 64 * w2b, 64 * w2b)
            engine.spawn(t)

if __name__ == "__main__":
    scene = scn.Scene()
    print(engine.currentScene)
    groundGroup = pg.sprite.Group()
    playerGroup = pg.sprite.Group()
    enemyGroup = pg.sprite.Group()
    projectileGroup = pg.sprite.Group()
    player = Player(7,5,.5,1)
    enemy = Enemy(3,5,.5,1)
    loadGame()
    playerGroup.add(player)
    enemyGroup.add(enemy)
    engine.spawn(player)
    engine.spawn(enemy)
    scene.all_sprites.append(groundGroup)
    scene.all_sprites.append(playerGroup)
    scene.all_sprites.append(enemyGroup)
    scene.all_sprites.append(projectileGroup)
    camera = Camera()
    engine.spawn(camera)
    updater = Updater(0,0,0,0)
    engine.spawn(updater)
    engine.currentScene.camera = camera
    engine.changeScreenSize(1280,720)
    engine.loop()

