import pygame as pyg
import math
from scripts.player import *
from scripts.projectiles import *


def Collide_Detect(x_1, y_1, width_1, height_1, xVel_1, yVel_1, x_2, y_2, width_2, height_2, xVel_2, yVel_2):
    x_1_L = x_1 + xVel_1
    x_1_R = x_1 + width_1 + xVel_1
    y_1_T = y_1 + yVel_1
    y_1_B = y_1 + height_1 + yVel_1

    x_2_L = x_2 + xVel_2
    x_2_R = x_2 + width_2 + xVel_2
    y_2_T = y_2 + yVel_2
    y_2_B = y_2 + height_2 + yVel_2
    coll = 5


    if x_1_L <= x_2_R and x_1_L >= x_2_L and y_1_B >= y_2_T and y_1_B <= y_2_B:
        # Bottom left corner is in second box

        if abs(x_1_L - x_2_R) > abs(y_1_B - y_2_T):
            # meaning Bottom side coll
            coll = 0
        else:
            # meaning Right side coll
            coll = 3

    elif x_1_R <= x_2_R and x_1_R >= x_2_L and y_1_B >= y_2_T and y_1_B <= y_2_B:
        # Bottom right corner is in the second box

        if abs(x_1_R - x_2_L) > abs(y_1_B - y_2_T):
            # meaning bottom side coll
            coll = 0
        else:
            # meaning right side coll
            coll = 3

    elif x_1_L <= x_2_R and x_1_L >= x_2_L and y_1_T >= y_2_T and y_1_T <= y_2_B:
        # Top left corner is in the second box

        if abs(x_1_L - x_2_R) > abs(y_1_T - y_2_B):
            # meaning Top side coll
            coll = 1
        else:
            # meaning Left side coll
            coll = 2

    elif x_1_R <= x_2_R and x_1_R >= x_2_L and y_1_T >= y_2_T and y_1_T <= y_2_B:
        # Top right corner is in the second box

        if abs(x_1_R - x_2_L) > abs(y_1_T - y_2_B):
            # meaning Top side coll
            coll = 1
        else:
            # meaning Right side coll
            coll = 2

    return coll, yVel_2