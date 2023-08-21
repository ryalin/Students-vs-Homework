#handles all of the draw functions in the game state
import random, time, copy, math, decimal
from cmu_112_graphics import *

######################## Normal View Draw Functions ############################

#draws the background the playing field
def drawBackgroundAndField(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
                        image=ImageTk.PhotoImage(app.background3))
    for i in range(len(app.board)):
        for j in range(len(app.board[i])):
            if app.board[i][j] == 1:
                picture = app.background1
            else:
                picture = app.background2
            canvas.create_image(250 + j * 100, app.height/3 + i * 100, 
                                image=ImageTk.PhotoImage(picture))

#draws the user interface
def drawSunCount(app, canvas):
    canvas.create_oval(120, 30, 160, 70, fill="lightGrey", width=0)
    canvas.create_rectangle(60, 30, 140, 70, fill="lightGrey", width=0)
    canvas.create_text(110, 48, text=f"{app.suns}", font="arial 20 bold")
    clock = app.scaleImage(app.clock, 1/12)
    canvas.create_image(50, 50, image=ImageTk.PhotoImage(clock))
    canvas.create_image(app.width - 40, 40, image=ImageTk.PhotoImage(app.gear))

#draws the settings menu after the gears are clicked
def drawMenu(app, canvas):
    canvas.create_rectangle(app.width/2 - 200, app.height/2 - 100, 
                            app.width/2 + 200, app.height/2 + 100, 
                            fill="peach puff", width=5)
    canvas.create_rectangle(app.width/2 - 180, app.height/2 + 40,  
                            app.width/2 - 10, app.height/2 + 80,
                            fill="grey", width=5)
    canvas.create_text(app.width/2 - 95, app.height/2 + 60, text="Main Menu", 
                    font="arial 25 bold")
    canvas.create_rectangle(app.width/2 + 10, app.height/2 + 40,  
                            app.width/2 + 180, app.height/2 + 80,
                            fill="red2", width=5)
    canvas.create_text(app.width/2 + 95, app.height/2 + 60, text="Restart Game", 
                    font="arial 25 bold")
    canvas.create_text(app.width/2 - 180, app.height/2 - 40, 
        text=f"Current Level: {app.level}\nNumber of Plants: {len(app.plantsOnBoard)}\nHomework Defeated: {len(app.killedZombies)}",
        font="arial 30 bold", anchor=W)

def drawShovel(app, canvas):
    canvas.create_rectangle(200, 20, 400, 80, fill="brown")
    if app.shovel == False:
        canvas.create_image(300, 50, image=ImageTk.PhotoImage(app.scaleImage(app.shovelPic, 1/20)))

def drawZombieProgressBar(app, canvas):
    if app.win == True:
        return
    canvas.create_rectangle(app.width/2 - 100, 30, app.width/2 + 100, 50, fill="grey26")
    canvas.create_rectangle(app.width/2 + 95 - (190*(len(app.killedZombies)/len(app.startingZombieList))), 
                        33, app.width/2 + 95, 47, fill="red4")
    text = app.level + 1
    if text == 6:
        text = "Win"
    canvas.create_oval(app.width/2 - 120, 20, app.width/2 - 80, 60, fill="yellow")
    canvas.create_text(app.width/2 - 100, 40, text=f"{text}", font="arial 20 bold")
    canvas.create_oval(app.width/2 + 80, 20, app.width/2 + 120, 60, fill="yellow")
    canvas.create_text(app.width/2 + 100, 40, text=f"{app.level}", font="arial 20 bold")
    pass

#draws zombies on the board
def drawZombies(app, canvas):
    for zombie in app.zombiesOnBoard:
        location = zombie.position 
        row = 270 + zombie.row * 100
        if zombie.kind == "base": image = app.regularZombie
        elif zombie.kind == "cone": image = app.coneZombie
        elif zombie.kind == "bucket": image = app.bucketZombie
        else: image = app.speedZombie
        canvas.create_image(location, row, image=ImageTk.PhotoImage(image))

#draws the plant selection menu on the left and cooldowns
#some code from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#getAndPutPixels
def drawPlantMenu(app, canvas):
    for i in range(len(app.plantList)):
        image = app.studentList[i]
        cost = app.costList[i]
        greyImage = image.copy()
        cooldown = app.plantCooldownList[i]
        for x in range(image.width):
            for y in range(image.height):
                r, g, b = greyImage.getpixel((x, y))
                greyImage.putpixel((x, y), (r//3, g//3, b//3))
        cooldownRatio = app.plantCooldownList[i] / app.referenceCooldownList[i]
        canvas.create_rectangle(28, (i + 1) * 110 - 12, 132, (i + 1) * 110 + 92, fill="black")
        canvas.create_image(80, (i + 1) * 110 + 40, image=ImageTk.PhotoImage(greyImage))
        canvas.create_image(80, (i + 1) * 110 + 90, 
        image=ImageTk.PhotoImage(image.crop([0,(cooldownRatio) * 100, 100, 100])), anchor=S)
        canvas.create_rectangle(30, (i + 1) * 110 + 70, 130, (i + 1) * 110 + 90,
                            fill="ivory2")
        canvas.create_image(40, (i + 1) * 110 + 80, 
        image=ImageTk.PhotoImage(app.scaleImage(app.clock, 1/20)))
        canvas.create_text(90, (i + 1) * 110 + 80, text=f"{cost}", 
                            font="arial 15 bold")

#draws each plant on the grass field
def drawPlants(app, canvas):
    for plant in app.plantsOnBoard:
        health = plant.health
        for i in range(len(app.totalPlants)):
            if plant.kind == app.totalPlants[i]:
                image = app.studentList[i]
        x, y = 230 + plant.col * 100, app.height/3 + plant.row * 100
        canvas.create_image(x + 20, y, image=ImageTk.PhotoImage(app.scaleImage(image, 3/4)))
        if plant.kind == "explodingCherry":
            canvas.create_image(x, y, image=ImageTk.PhotoImage(app.scaleImage(app.boom, 4/3)))

def drawProjectiles(app, canvas):
    for plant in app.plantsOnBoard:
        if plant.kind not in ("explodingCherry", "walnut", "sunflower"):
            if plant.kind == "peashooter": image = app.scaleImage(app.rock, 1/10)
            elif plant.kind == "iceshooter": image = app.scaleImage(app.blueRock, 1/20)
            elif plant.kind == "doubleShooter": image = app.scaleImage(app.rock, 1/10)
            for zombie in app.zombiesOnBoard:
                if (zombie.row == plant.row) and (zombie.position < 1200):
                    position = plant.projectilePosition
                    yCoord = app.height/3 + plant.row * 100
                    canvas.create_image(position, yCoord, image=ImageTk.PhotoImage(image))
                    if plant.kind == "doubleShooter":
                        canvas.create_image(position - 40, yCoord, image=ImageTk.PhotoImage(image))

def drawSuns(app, canvas):
    for sun in app.sunList:
        canvas.create_image(sun.x, sun.y, image=ImageTk.PhotoImage(app.scaleImage(app.clock, 1/20)))

#draws a game over screen
def drawGameOver(app, canvas):
    if app.gameOver == True:
        message = "Game Over!"
    else:
        message = "You Win!"
    canvas.create_rectangle(app.width/2 - 200, app.height/2 - 100, app.width/2 + 200, 
                            app.height/2 + 100, fill="grey", width=3)
    canvas.create_text(app.width/2, app.height/2 - 50, text=message, font="arial 40 bold")
    canvas.create_rectangle(app.width/2 - 100, app.height/2, app.width/2 + 100, 
                        app.height/2 + 50, fill="grey", width=3)
    canvas.create_text(app.width/2, app.height/2 + 25, text="Main Menu",
                    font="arial 30 bold")

######################### Lawn POV Draw Functions ##############################
    
def draw3dField(app, canvas):
    for i in range(6):
        lowerY, higherY = 750, 230
        lowerX = app.width / 2 - (2.5 - i) * (lowerY/3) + 20
        higherX = app.width / 2 - (2.5 - i) * (higherY/3) + 20
        canvas.create_line(lowerX, lowerY, higherX, higherY, width=2)
    for i in range(10):
        y = 150 + (600 * ((4/5)**i))
        leftX = app.width / 2 - 2.5 * (y/3) + 20
        rightX = app.width / 2 + 2.5 * (y/3) + 20
        canvas.create_line(leftX, y, rightX, y, width=2)

def viewLawnDrawPlants(app, canvas):
    for plant in app.plantsOnBoard:
        lawnViewYPosition = (300 + (600 * ((4/5)**plant.col + (4/5)**(plant.col + 1)))) / 2
        lawnViewXPosition = (app.width + 40 - ((lawnViewYPosition/3) * (4 - 2*plant.row))) / 2
        size = 50 * ((4/5)**plant.col)
        for i in range(len(app.totalPlants)):
            if plant.kind == app.totalPlants[i]:
                image = app.studentList[i]
        canvas.create_image(lawnViewXPosition, lawnViewYPosition, 
                        image=ImageTk.PhotoImage(app.scaleImage(image, size / 50)))
        if plant.kind == "explodingCherry":
            canvas.create_image(lawnViewXPosition, lawnViewYPosition, 
                    image=ImageTk.PhotoImage(app.scaleImage(app.boom, size/15)))

def viewLawnDrawZombies(app, canvas):
    for zombie in app.zombiesOnBoard:
        zombieCol = ((zombie.position - 130) / 100)
        lawnViewYPosition = (300 + (600 * ((4/5)**zombieCol + (4/5)**(zombieCol + 1)))) / 2
        lawnViewXPosition = (app.width + 40 - ((lawnViewYPosition/2.5) * (4 - 2*zombie.row))) / 2
        size = 50 * ((4/5)**zombieCol)
        if zombie.kind == "base": image = app.regularZombie
        elif zombie.kind == "cone": image = app.coneZombie
        elif zombie.kind == "bucket": image = app.bucketZombie
        else: image = app.speedZombie
        health = zombie.health
        canvas.create_image(lawnViewXPosition, lawnViewYPosition, 
                        image=ImageTk.PhotoImage(app.scaleImage(image, size / 10)))

def viewLawnDrawProjectiles(app, canvas):
    for plant in app.plantsOnBoard:
        if plant.kind not in ("explodingCherry", "walnut", "sunflower"):
            if plant.kind == "peashooter": image = app.rock
            elif plant.kind == "iceshooter": image = app.scaleImage(app.blueRock, 1/2)
            elif plant.kind == "doubleShooter": image = app.rock
            for zombie in app.zombiesOnBoard:
                if (zombie.row == plant.row) and (zombie.position < 1200):
                    projectileCol = ((plant.projectilePosition - 230) / 100)
                    lawnViewYPosition = (300 + (600 * ((4/5)**projectileCol + (4/5)**(projectileCol + 1)))) / 2
                    lawnViewXPosition = (app.width + 40 - ((lawnViewYPosition/3) * (4 - 2*plant.row))) / 2
                    size = ((4/5)**projectileCol) / 4
                    canvas.create_image(lawnViewXPosition, lawnViewYPosition, 
                            image=ImageTk.PhotoImage(app.scaleImage(image, size)))
                    if plant.kind == "doubleShooter":
                        projectileCol = ((plant.projectilePosition - 260) / 100)
                        lawnViewYPosition = (300 + (600 * ((4/5)**projectileCol + (4/5)**(projectileCol + 1)))) / 2
                        lawnViewXPosition = (app.width + 40 - ((lawnViewYPosition/3) * (4 - 2*plant.row))) / 2
                        canvas.create_image(lawnViewXPosition, lawnViewYPosition, 
                            image=ImageTk.PhotoImage(app.scaleImage(image, size)))

def viewLawnInformation(app, canvas):
    canvas.create_text(app.width/2, 70, text="Information Mode", 
                    fill="chartreuse3", font="arial 15 bold")
    canvas.create_rectangle(app.width/2 + 140, 20, app.width/2 + 520, 160, 
                        fill="ivory2", width=0)
    if app.hoveredOver == None:
        return
    if app.hoveredOver.kind in app.totalPlants:
        canvas.create_text(app.width/2 + 160, 40, text=f"Entity: Student", 
                    font="arial 20 bold", fill="green", anchor=W)
        health = int(app.hoveredOver.health / 10)
        if health <= 0:
            health = "Consumed By Homework"
        for i in range(len(app.studentNames)):
            if app.totalPlants[i] == app.hoveredOver.kind:
                name = app.studentNames[i]
        canvas.create_text(app.width/2 + 160, 70, text=f"Name: {name}",
                        font="arial 20 bold", anchor=W)
        canvas.create_text(app.width/2 + 160, 130, 
                        text=f"Happiness Level: Depressed",
                        font="arial 20 bold", anchor=W)
    else:
        canvas.create_text(app.width/2 + 160, 40, text=f"Entity: Homework", 
                    font="arial 20 bold", fill="red", anchor=W)
        distance = app.hoveredOver.position - 180
        if distance <= 0:
            distance = "Too late"
        health = app.hoveredOver.health
        speed = app.hoveredOver.speed           
        canvas.create_text(app.width/2 + 160, 70, text=f"Speed: {speed}",
                        font="arial 20 bold", anchor=W)
        canvas.create_text(app.width/2 + 160, 130, 
                        text=f"Distance to End: {distance}",
                        font="arial 20 bold", anchor=W)
    canvas.create_text(app.width/2 + 160, 100, text=f"Health: {health}",
                    font="arial 20 bold", anchor=W)

