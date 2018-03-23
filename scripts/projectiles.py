import pygame as pyg

pyg.init()

class Projectile(object):
    def __init__(self, x, y, facing, radius, color=(230,0,230), yVel=0):
        self.x = x
        self.y = y
        self.xVel = facing*10
        self.yVel = yVel
        self.radius = radius
        self.color = color


    def draw(self, win):
        pyg.draw.circle(win, self.color, (self.x, self.y), self.radius)