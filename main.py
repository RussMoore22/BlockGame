import pygame as pyg
import time, sys
from scripts.player import *
from scripts.projectiles import *
from scripts.collision import *
from scripts.globals import *

pyg.init()
screenSize = 1000

win = pyg.display.set_mode((screenSize,screenSize))
pyg.display.set_caption("ArdyBlocks")
x = 50
y = 50
width = 40
height = 40
acc = 2

v_i = 0
cSec = 0
cFrame = 0
FPS = 0
deltaTime = 0
is_running = True
tile_size = 32
velMult = 50
grav = 9
NewVel = 0
currentVel = 0
xVel = 0
Bullets = []
groundSize = 100
onGround = False
countDown = 0
collCode = []
BlockMove = 0
minplus = 2
jump = False

fps_font = pyg.font.SysFont('Calibri', 25, True, False)
#fps_font = pyg.font.Font("~/Library/Fonts/Veranda.ttf", 20)


redBlock = Player(x,y,width,height)


vel = 5

clock = pyg.time.Clock()


def show_FPS():
    global FPS, fps_font
    fps_overlay =  fps_font.render(str(FPS), True, (220,220,220))
    win.blit(fps_overlay, (0,0))

def count_FPS():
    global cSec, cFrame, FPS, deltaTime  # cSec:current-second, cFrame:current-frame

    if cSec == time.strftime("%S"):
        cFrame += 1
    else:
        FPS = cFrame  # To what cFrame will get up to
        cFrame = 0
        cSec = time.strftime("%S")
    if FPS > 0:
        deltaTime = 1/FPS
def restart():
    x = -Globals.camera_x + 10
    y =  10
    print(Globals.camera_x)
    return (x,y)


while True:
    pyg.time.delay(20)

    for bullet in Bullets:
        if bullet.x < screenSize + Globals.camera_x and bullet.x > 0+ Globals.camera_x:
            bullet.x += bullet.xVel
        else:
            try:
                bullet.pop(Bullets.index(bullet))
            except:
                Bullets = []



    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()

    Keys = pyg.key.get_pressed()

    if Keys[pyg.K_f] and countDown <= 0:
        if len(Bullets) < 15:
            Bullets.append(Projectile(round(redBlock.x+redBlock.width // 2), round(redBlock.y+redBlock.height // 2), redBlock.facing, 6))
            countDown = 10

    if onGround:
        jump = False

        redBlock.yVel = 0
        if Keys[pyg.K_LEFT]:
            redBlock.xVel = -5
            redBlock.facing = -1
        elif Keys[pyg.K_RIGHT]:
            redBlock.xVel = 5
            redBlock.facing = 1

        if Keys[pyg.K_SPACE]:
            redBlock.yVel = -grav/deltaTime
            onGround = False
            jump = True
        elif not Keys[pyg.K_LEFT] and not Keys[pyg.K_RIGHT]:
            redBlock.xVel = 0


    else:
        if Keys[pyg.K_LEFT]:
            redBlock.xVel -= 1
            redBlock.facing = -1
        if Keys[pyg.K_RIGHT]:
            redBlock.xVel += 1
            redBlock.facing = 1


    # Changing Camera_move






    if Keys[pyg.K_DOWN] and redBlock.yVel < 200:
        redBlock.yVel += 50

    rectangles = [(0 + Globals.camera_x,300,490,50,0,0), (600 + Globals.camera_x, 200+BlockMove, 400, 40, 0, minplus),
                  (0 + Globals.camera_x,screenSize-200,screenSize*100,200,0,0),(500 + Globals.camera_x,
                                                                                screenSize-300,100,100,0,0), (1400 + Globals.camera_x, 400+BlockMove, 300, 60, 0, minplus),
                  (100 + Globals.camera_x, 650, 55, 70, 0, 0)]

    for rec in rectangles:
        (c,yV) = Collide_Detect(redBlock.x, redBlock.y, redBlock.width, redBlock.height, redBlock.xVel, redBlock.yVel * deltaTime, rec[0],rec[1],rec[2],rec[3], rec[4], rec[5])
        collCode.append(c)
        if c == 0 and yV != 0 and not jump:
            redBlock.y += round(yV)
    for code in collCode:
        if code == 5:
            try:
                code.pop(collCode.index(code))
            except:
                pass

    if 0 in collCode:
        onGround = True
        if 1 in collCode:
            (redBlock.x, redBlock.y) = restart()



    elif 1 in collCode:
        redBlock.yVel = 0
        redBlock.y += 5


    elif 2 in collCode:
        redBlock.xVel = 0

    elif 3 in collCode:
        redBlock.xVel = 0

    elif FPS > 2:
        onGround = False
        redBlock.y = redBlock.y + deltaTime * redBlock.yVel
        redBlock.yVel = redBlock.yVel + .5 * deltaTime * grav * grav

    if redBlock.x > screenSize - redBlock.width - 200 and redBlock.xVel > 0:
        Globals.camera_move = 1


    elif redBlock.x < 200 and redBlock.xVel < 0:
        Globals.camera_move = 2


    if redBlock.xVel > 4:
        redBlock.xVel = 4
    elif redBlock.xVel < -4:
        redBlock.xVel = -4

    redBlock.x += redBlock.xVel
    collCode = []

    #LOGIC


    count_FPS()
    countDown -= 1



    win.fill((0,0,100))
    pyg.draw.rect(win, (10, 15, 10), (0 + Globals.camera_x, screenSize- groundSize, screenSize, groundSize))
    pyg.draw.rect(win, (225, 0, 0), (round(redBlock.x), round(redBlock.y), redBlock.width, redBlock.height))
    for rec in rectangles:
        pyg.draw.rect(win, (200,200,200), (rec[0],rec[1],rec[2],rec[3]), 10)
    #pyg.draw.rect(win, (0,200,0,), (200,0, 600,1000), 3)
    # Bullet Logic

    for bullet in Bullets:
        bullet.draw(win)
    # Block Move Logic

    BlockMove += minplus
    if BlockMove >= 400 or BlockMove <= 0:
        minplus = -minplus

    # camera Logic
    if Globals.camera_move == 1:
        Globals.camera_x -= redBlock.xVel
        redBlock.x -= redBlock.xVel
        Globals.camera_move = 0

    elif Globals.camera_move == 2:
        Globals.camera_x -= redBlock.xVel
        redBlock.x -= redBlock.xVel
        Globals.camera_move = 0



    show_FPS()

    # DEGUB

    pyg.display.update()


pyg.quit()