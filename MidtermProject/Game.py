import json
import sys

import pygame.transform

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


class StaticObject(go.DGameObject):
    def __init__(self, x, y, w, h, collidable, cb = 0x0000, mb = 0xFFFF):
        super().__init__(x, y, w, h, collidable)
        shape = b2PolygonShape(box=(w * w2b / 2, h * w2b / 2))
        self.body = world.CreateStaticBody(position=(x * w2b, y * w2b), shapes = shape)
        self.fixDef = b2FixtureDef(shape=shape)
        self.fixDef.shape._radius = 0.1
        self.fixDef.filter.categoryBits = cb
        self.fixDef.filter.maskBits = mb
        self.box = self.body.CreateFixture(self.fixDef)
        self.image = pg.Surface((w, h), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2w, 768 - self.body.position.y * b2w

    def Draw(self):
        pass

class Bullet(go.DUGameObject):
    def __init__(self, w = 25, h = 25):
        super().__init__(w=w, h=h)
        self.body = world.CreateDynamicBody(position=(player.body.position.x, player.body.position.y), gravityScale = 0.0)
        shape = b2PolygonShape(box=(w * w2b/2, h * w2b/2))
        self.fixDef = b2FixtureDef(shape=shape, density=.5)
        self.fixDef.filter.categoryBits = 0x0003
        self.fixDef.filter.maskBits &= ~0x0002
        self.fixDef.filter.maskBits &= ~0x0003
        self.box = self.body.CreateFixture(self.fixDef)
        self.dirty = 2
        d = w
        self.image = pg.Surface((d, d), pg.SRCALPHA, 32)
        self.image = sprites['Bullet']
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.velocity = b2Vec2(player.direction * 0.05, 0)
        self.image = pygame.transform.rotate(self.image, player.direction * 270)
    def Update(self):
        self.rect.center = self.body.position.x * b2w, 770 - self.body.position.y * b2w
        enemyCollisions = pg.sprite.spritecollide(self, enemyGroup, False)
        groundCollisions = pg.sprite.spritecollide(self, groundGroup, False)
        collided = len(enemyCollisions) + len(groundCollisions)
        if collided > 0:
            for object in enemyCollisions:
                object.health -= 1
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
        self.body = world.CreateDynamicBody(position=(x * w2b, y * w2b))
        shape = b2PolygonShape(box=(w * w2b/2, h * w2b/2))
        self.fixDef = b2FixtureDef(shape=shape)
        self.fixDef.filter.categoryBits = 0x0002
        self.box = self.body.CreateFixture(self.fixDef)
        self.fixDef.friction = 0
        self.dirty = 2
        self.image = pg.Surface((w, h), pg.SRCALPHA, 32)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.body.mass = 1.0
        pg.draw.rect(self.image, (0, 101, 164), (self.rect.x, self.rect.y, w, h))
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
        self.image = sprites['Player']
        self.health = 5
    def Update(self):
        currentTime = pg.time.get_ticks()
        self.rect.center = self.body.position.x * b2w, 771 - self.body.position.y * b2w
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
                    updater.add(Bullet(), projectileGroup)
                    self.timeSinceShot = pg.time.get_ticks()
        if self.health < 0:
            updater.remove(self, playerGroup)
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
                if self.direction != -1:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.direction = -1
            elif event.key == pg.K_d:
                self.inputs['right'] = True
                if self.direction != 1:
                    self.image = pygame.transform.flip(self.image, True, False)
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
        self.body = world.CreateDynamicBody(position=(x * w2b, y * w2b))
        shape = b2PolygonShape(box=(w * w2b/2, h * w2b/2))
        self.fixDef = b2FixtureDef(shape=shape)
        self.fixDef.filter.maskBits = 0xFFFF
        self.fixDef.filter.categoryBits = 0x0001
        self.box = self.body.CreateFixture(self.fixDef)
        self.dirty = 2
        self.image = pg.Surface((w, h), pg.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.body.mass = 1.0
        pg.draw.rect(self.image, (101, 0, 164), (self.rect.x, self.rect.y, w, h))
        self.maxSpeed = 2
        self.velocity = b2Vec2(1,0)
        self.image = sprites['Enemy']
        self.health = 5
    def Update(self):
        self.rect.center = self.body.position.x * b2w, 771 - self.body.position.y * b2w
        self.body.ApplyLinearImpulse(self.velocity, self.body.position, True)
        colliderCollision = pg.sprite.spritecollide(self, enemyColliderGroup, False)
        playerCollision = pg.sprite.spritecollide(self, playerGroup, False)
        if len(playerCollision) > 0:
            player.health -= 1
            self.velocity *= -1
        elif len(colliderCollision) > 0:
            self.velocity *= -1
        if self.health < 0:
            updater.remove(self, enemyGroup)

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

class Tile(go.DGameObject):
    def __init__(self):
        super().__init__()
    def Draw(self):
        pass

def loadSprite(key, path, w = 64, h = 64):
    t = Tile()
    t.image = pg.Surface((w, h), pg.SRCALPHA, 32)
    sprite = pg.transform.scale(pg.image.load(path), (w, h))
    t.image.blit(sprite, (0, 0, w, h))
    sprites[key] = t.image
    print(sprites[key])

def loadGame():
    file = open("newmap.tmj")
    level = json.load(file)
    level = level['layers']
    width = 100
    height = 20
    size = 2000
    loadSprite("wall", "./assets/DungeonTileset/frames/wall_mid.png")
    loadSprite("collider", "./assets/DungeonTileset/frames/crate.png")
    i = 0
    j = 0
    for tile in range(2000):
        before = i
        if (not (i := tile % width)) and before != 0:
            j += 1
        for layers in level:
            data = layers['data'][(j * width) + i]
            if data != 0 and data != 37:
                x = i * 64
                y = j * 64
                if data == 69:
                    t = StaticObject(x, y * -1, 64, 64, True)
                    t.image = sprites['wall']
                    groundGroup.add(t)
                elif data == 91:
                    shape = b2PolygonShape(box=(64 * w2b / 2, 64 * w2b / 2))
                    t = StaticObject(x, y * -1, 64, 64, False, 0x0005, 0x0001)
                    t.fixDef = b2FixtureDef(shape=shape)
                    # t.fixDef.filter.categoryBits = cb
                    t.fixDef.filter.maskBits = 0x0001
                    t.box = t.body.CreateFixture(t.fixDef)
                    t.image = sprites['collider']
                    enemyColliderGroup.add(t)
                engine.spawn(t)

if __name__ == "__main__":
    sprites = {}
    loadSprite("Enemy", "./assets/DungeonTileset/frames/big_demon_idle_anim_f0.png", 64, 125)
    loadSprite("Player", "./assets/DungeonTileset/frames/knight_m_idle_anim_f0.png", 64, 125)
    loadSprite("Bullet", "./assets/DungeonTileset/frames/weapon_arrow.png", 10, 25)
    scene = scn.Scene()
    groundGroup = pg.sprite.Group()
    playerGroup = pg.sprite.Group()
    enemyGroup = pg.sprite.Group()
    enemyColliderGroup = pg.sprite.Group()
    projectileGroup = pg.sprite.Group()
    player = Player(2000,-30,64,125)
    enemy = Enemy(2000,-600,64,125)
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

