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

pg.mixer.music.load("./assets/SoundEffects/metmhide.mid")
shooting = pg.mixer.Sound("./assets/SoundEffects/507016__mrthenoronha__gun-shot-3-8-bit.wav")
enemyHitSound = pg.mixer.Sound("./assets/SoundEffects/138480__justinvoke__bullet-blood-3.wav")
wallHitSound = pg.mixer.Sound("./assets/SoundEffects/522401__filmmakersmanual__bullet-concrete-hit-4.wav")
pg.mixer.Sound.set_volume(1.0)

class StaticObject(go.DGameObject):
    def __init__(self, x, y, w, h, collidable, cb = 0x0000, mb = 0xFFFF):
        super().__init__(x, y, w, h, collidable)
        shape = b2PolygonShape(box=(w * w2b / 2, h * w2b / 2))
        self.body = world.CreateStaticBody(position=(x * w2b, y * w2b), shapes = shape)
        self.fixDef = b2FixtureDef(shape=shape)
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
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        pg.draw.circle(self.image, (0, 101, 164), self.rect.center, w/2)
        self.velocity = b2Vec2(player.direction * 0.05, 0)
    def Update(self):
        self.rect.center = self.body.position.x * b2w, 770 - self.body.position.y * b2w
        enemyCollisions = pg.sprite.spritecollide(self, enemyGroup, False)
        groundCollisions = pg.sprite.spritecollide(self, groundGroup, False)
        collided = len(enemyCollisions) + len(groundCollisions)
        if collided > 0:
            updater.remove(self)
            if enemyCollisions:
                pg.mixer.Sound.play(enemyHitSound)
            if groundCollisions:
                pg.mixer.Sound.play(wallHitSound)
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
        self.dirty = 2
        self.image = pg.Surface((w, h), pg.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
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
                pg.mixer.Sound.play(shooting)
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
        pg.draw.rect(self.image, (101, 230, 164), (self.rect.x, self.rect.y, w, h))
        self.maxSpeed = 2
        self.velocity = b2Vec2(1,0)
        # loadSprite("enemy", "./assets/DungeonTileset/frames/big_demon_idle_anim_f1.png",sprites)
        # loadSprite("enemy-walk", "/assets/DungeonTileset/frames/big_demon_run_anim_f1.png", sprites)
        # loadSprite("player", "/assets/DungeonTileset/frames/elf_m_idle_anim_f3.png", sprites)
        # loadSprite("player-walk-odd", "/assets/DungeonTileset/frames/elf_m_run_anim_f1.png", sprites)
        # loadSprite("player-walk-even", "/assets/DungeonTileset/frames/elf_m_run_anim_f2.png", sprites)
        # loadSprite("player-jump", "/assets/DungeonTileset/frames/elf_m_run_anim_f3.png", sprites)
    def Update(self):
        self.rect.center = self.body.position.x * b2w, 771 - self.body.position.y * b2w
        self.body.ApplyLinearImpulse(self.velocity, self.body.position, True)
        collision = pg.sprite.spritecollide(self, groundGroup, False)
        if not len(collision):
            self.velocity *= -1
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

def loadSprite(key, path, sprites):
    t = Tile()
    t.image = pg.Surface((64, 64), pg.SRCALPHA, 32)
    sprite = pg.transform.scale(pg.image.load(path), (64, 64))
    t.image.blit(sprite, (0, 0, 64, 64))
    sprites[key] = t.image

def loadGame():
    file = open("newmap.tmj")
    level = json.load(file)
    level = level['layers']
    width = 100
    height = 20
    size = 2000
    loadSprite("wall", "./assets/DungeonTileset/frames/wall_mid.png",sprites)
    loadSprite("collider", "./assets/DungeonTileset/frames/crate.png",sprites)
    pg.mixer.music.play(-1)
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
                engine.spawn(t)

if __name__ == "__main__":
    sprites = {}
    scene = scn.Scene()
    groundGroup = pg.sprite.Group()
    playerGroup = pg.sprite.Group()
    enemyGroup = pg.sprite.Group()
    projectileGroup = pg.sprite.Group()
    player = Player(2000,-30,64,125)
    enemy = Enemy(2000,-150,64,125)
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

