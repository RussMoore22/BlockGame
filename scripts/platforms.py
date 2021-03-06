import pygame as pyg
Platforms = []

with open('map.txt') as file:
    data = file.read()
    data = data.strip()
    data = data.replace('\n', '')
    dataList = data.split("'")
    usableData = dataList[-1]
    usableData= usableData.split("-")


for list in usableData:
    tempList = []
    tempList2 = list.split(",")
    for num in tempList2:
        try:
            tempList.append(int(num))
        except:
            break
    Platforms.append(tempList)
i = 0
for list in Platforms:
    if not list:
        del Platforms[i]
    i += 1


class Platform(object):
    def __init__(self, x, y, width, height, xVel, yVel, min=0, max=1000, color=(230,0,230)):
        self.x = x
        self.y = y
        self.xVel = xVel
        self.yVel = yVel
        self.width = width
        self.height = height
        self.dir = 1
        self.max = max
        self.min = min
        self.color = color

    def create_Platforms():
        Platforms2 = []

        for plat in Platforms:
            try:
                Platforms2.append(Platform(plat[0],plat[1],plat[2],plat[3],plat[4],plat[5], plat[6], plat[7]))
            except:
                Platforms2.append(Platform(plat[0], plat[1], plat[2], plat[3], plat[4], plat[5]))

        return Platforms2

    def move_Platform(object, deltaTime):
        object.x += object.xVel*deltaTime*object.dir
        object.y += object.yVel*deltaTime*object.dir
        if object.y < object.min or object.y > object.max:
            object.dir *= -1

    def circular_Motion(object, deltaTime):
        pass





