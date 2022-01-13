import pyxel
import numpy as np
import random

class Hitbox:
    w = 80
    h = 30
    m = 3
    def __init__(self,x,y,tp):
        self.x = x
        self.y = y
        self.tp = tp
    
    def ball_bound(ball):
        if self.tp == 'x':
            ball.hit_x_bar()
        
        if self.tp == 'y':
            ball.hit_y_bar()

    def check_hit(self,ball):
        if self.tp == 'x':
            if ball.y >= self.y and ball.y <= self.y+self.m and ball.x >= self.x and ball.x<= self.x + self.w:
                ball.hit_y_bar()
                return True
        if self.tp == 'y':
            if ball.y <= self.y+self.h and ball.y>=self.y and ball.x >= self.x and ball.x <= self.x + self.m:
                ball.hit_x_bar()
                return True



class Block:
    w = 80
    h = 30
    hitboxes = []
    def __init__(self,x,y,c):
        self.x = x
        self.y = y
        self.color = c
        self.exist = True
        self.set_hitbox()
    def set_hitbox(self):
        self.hitboxes=[
            Hitbox(self.x,self.y,'x'),
            Hitbox(self.x,self.y,'y'),
            Hitbox(self.x,self.y+27,'x'),
            Hitbox(self.x+77,self.y,'y'),
        ]
    def reset(self):
        self.exist = True

    def check_hit(self,ball):
        for hitbox in self.hitboxes:
            if hitbox.check_hit(ball):
                return True


class Ball:
    r = 5
    color = 0
    res_x = 200
    res_y = 300
    life = 3
    game_over = False
    def __init__(self):
        self.spone()
    def spone(self):
        self.x = self.res_x
        self.y = self.res_y
        self.dirc_x = random.choice([-1,1])
        self.dirc_y = random.choice([-1,1])
        self.rad = random.randint(10,50)
        self.speed = 5
    def move(self,player):
        self.x += self.dirc_x*self.speed*(np.cos(self.rad))
        self.y += self.dirc_y*self.speed*(np.sin(self.rad))

        if self.x < 0 or self.x >400:
            self.hit_x_bar()
        if self.y < 0 :
            self.hit_y_bar()
        if self.y>=395 and self.x >= player.x and player.x + 30 >= self.x:
            self.hit_y_bar()
        if self.y >400:
            self.life -= 1
            if self.life <= 0:
                self.game_over = True
            else:
                self.spone()
    def hit_x_bar(self):
        self.dirc_x *= -1

    def hit_y_bar(self):
        self.dirc_y *= -1

class Player:
    center = 185
    y = 395
    w = 30
    h = 5
    color = 3
    def __init__(self):
        self.spone()

    def spone(self):
        self.x = self.center

    def move(self):
        self.x = pyxel.mouse_x


class App:
    blocks = []
    player = Player()
    ball = Ball()
    def __init__(self):
        self.spone_blocks()
        
        pyxel.init(400,400,title="block_game")
        pyxel.run(self.update,self.draw)
    def restart(self):
        self.spone_blocks()
        self.ball.life = 3
        self.ball.game_over = False
    def spone_blocks(self):
        y = 10
        for i in range(3):
            x = 10
            c = i+8
            for j in range(4):
                self.blocks.append(Block(x,y,c))
                x += 100
            y+=50

    def update(self):
        if self.ball.game_over:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.restart()
        else:
            self.player.move()
            self.ball.move(self.player)
            for i,block in enumerate(self.blocks):
                if block.check_hit(self.ball):
                    del self.blocks[i]
            if self.blocks == []:
                self.ball.game_over = True
    def draw(self):
        if self.ball.game_over:
            pyxel.cls(0)
        else:
            pyxel.cls(7)
        
            for block in self.blocks:
                pyxel.rect(block.x,block.y,block.w,block.h,block.color)
            pyxel.rect(self.player.x,self.player.y,self.player.w,self.player.h,self.player.color)
            pyxel.circ(self.ball.x,self.ball.y,self.ball.r,self.ball.color)
        
App()