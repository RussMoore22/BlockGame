import pygame as pyg
import time, sys
from scripts.player import *
from scripts.projectiles import *
from scripts.collision import *
from scripts.globals import *
from scripts.platforms import *

pyg.init()
screenSize_x,screenSize_y = 1280, 800
x, y, width, height, vel, grav = 50, 50, 40, 40, 5, 20
centerScreen = [screenSize_x/2, screenSize_y/2]
cSec, cFrame, FPS, deltaTime, countDown = 0, 0, 0, 0, 0
Bullets = []
collCode = []
jump, onGround = False, False
lastGlobalscam_x = 0
PlatformTest = Platform.create_Platforms()
fps_font = pyg.font.SysFont('Calibri', 25, True, False)
lose_font = pyg.font.SysFont('Calibri', 150, True, False)

redBlock = Player(x,y,width,height)
clock = pyg.time.Clock()

win = pyg.display.set_mode((screenSize_x,screenSize_y))
pyg.display.set_caption("ArdyBlocks")
flags = pyg.DOUBLEBUF | pyg.HWSURFACE | pyg.FULLSCREEN
pyg.display.set_mode((screenSize_x, screenSize_y), flags)

def show_FPS():
    global FPS, fps_font
    fps_overlay =  fps_font.render(str(FPS), True, (220,220,220))
    win.blit(fps_overlay, (0,0))

def show_coord(x,y):
    global fps_font
    overlay = fps_font.render(str(x)+" , "+str(y), True, (200,200,200))
    win.blit(overlay, (0,15))

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
    y = 10
    return (x,y)
def youLose():
    global fps_font
    overlay = lose_font.render("YOU LOSE", True, (50,50,50))
    win.blit(overlay,(10,screenSize_y/2-100))
    overlay2 = lose_font.render("Hold Down q", True, (200,200,200))
    overlay3 = lose_font.render("to exit game", True, (200, 200, 200))
    win.blit(overlay2, (10,screenSize_y-200))
    win.blit(overlay3, (10, screenSize_y - 100))


is_running = True
while True:
    print(Globals.camera_x)
    pyg.time.delay(20)

    # PROJECTILES
    for bullet in Bullets:
        if bullet.x > 0 and bullet.x < 10000:
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
        if len(Bullets) < 150:
            Bullets.append(Projectile(round(redBlock.x+redBlock.width // 2), round(redBlock.y+redBlock.height // 2), redBlock.facing, 6))
            countDown = 5
    elif Keys[pyg.K_q] or Keys[pyg.K_ESCAPE]:
        pyg.quit()
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
            redBlock.yVel = -200
            onGround = False
            jump = True
        elif not Keys[pyg.K_LEFT] and not Keys[pyg.K_RIGHT]:
            redBlock.xVel = 0
    else:
        if Keys[pyg.K_LEFT]:
            redBlock.xVel -= 1
            redBlock.facing = -1
        elif Keys[pyg.K_RIGHT]:
            redBlock.xVel += 1
            redBlock.facing = 1
        if Keys[pyg.K_DOWN] and redBlock.yVel < 200:
            redBlock.yVel += 50

    if Keys[pyg.K_UP] and Keys[pyg.K_RSHIFT]:
        redBlock.yVel = -50

    for platform in PlatformTest:
        platform.x += Globals.camera_x - lastGlobalscam_x

    for rec in PlatformTest:
        (c,yV) = Collide_Detect(redBlock.x, redBlock.y, redBlock.width, redBlock.height, redBlock.xVel, redBlock.yVel * deltaTime, rec.x,rec.y,rec.width,rec.height, rec.xVel, rec.yVel)
        collCode.append(c)
        if c == 0 and yV != 0 and not jump:
            redBlock.y += round(yV)

    # SORT THROUGH COLLIDE RESULTS
    for code in collCode:
        if code == 5:
            try:
                code.pop(collCode.index(code))
            except:
                pass
    # 
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

    # TAILORING VALUES
    elif FPS > 2:
        onGround = False
        redBlock.y = redBlock.y + deltaTime * redBlock.yVel
        redBlock.yVel = redBlock.yVel + .5 * deltaTime * grav * grav
    if redBlock.x > screenSize_x - redBlock.width - 200 and redBlock.xVel > 0:
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
    if Globals.camera_x != lastGlobalscam_x:
        centerScreen[0] -= Globals.camera_x - lastGlobalscam_x
    lastGlobalscam_x = Globals.camera_x
    win.fill((0,0,100))
    pyg.draw.rect(win, (225, 0, 0), (round(redBlock.x), round(redBlock.y), redBlock.width, redBlock.height))
    for rec in PlatformTest:
        pyg.draw.rect(win, (200,200,200), (rec.x,rec.y,rec.width,rec.height), 10)

    # Bullet Logic
    for bullet in Bullets:
        bullet.draw(win)
        print(bullet.x,bullet.y)

    # camera Logic
    if Globals.camera_move == 1:
        Globals.camera_x -= redBlock.xVel
        redBlock.x -= redBlock.xVel
        Globals.camera_move = 0
    elif Globals.camera_move == 2:
        Globals.camera_x -= redBlock.xVel
        redBlock.x -= redBlock.xVel
        Globals.camera_move = 0
    if redBlock.y > screenSize_y + 50:
        youLose()
        Globals.camera_x -= 20
        time.sleep(1)

    show_FPS()
    show_coord(int(redBlock.x-Globals.camera_x),int(redBlock.y-Globals.camera_y))
    pyg.display.update()

pyg.quit()
