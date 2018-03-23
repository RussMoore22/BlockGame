import pygame as pyg

pyg.init()

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.facing = 1
        self.xVel = 0
        self.yVel = 0

    def facing_get(self, cVel):
        if cVel > 0:
            d = 1
        elif cVel < 0:
            d = -1
        else:
            d = 1
        return d




