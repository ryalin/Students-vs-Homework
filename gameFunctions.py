#handles the computation of the game 
import random, time, copy, math, decimal
from cmu_112_graphics import *

################ Game Screen ##################

#sets up board that shows the alternation of grass patterns
def gameRunning_board(app):
    board = [[1, 0, 1, 0, 1, 0, 1, 0, 1],
             [0, 1, 0, 1, 0, 1, 0, 1, 0],
             [1, 0, 1, 0, 1, 0, 1, 0, 1],
             [0, 1, 0, 1, 0, 1, 0, 1, 0],
             [1, 0, 1, 0, 1, 0, 1, 0, 1],]
    return board

def gameRunning_appStarted(app):
    #background and field images
    backgroundUrl = "https://www.chippenham.gov.uk/wp-content/uploads/2020/09/grounds-maintainence-1000-x-426.jpg"
    image = app.loadImage(backgroundUrl)
    app.background1 = app.scaleImage(image.crop((0, 0, 400, 400)), 1/4)
    app.background2 = app.scaleImage(image.crop((600, 0, 1000, 400)), 1/4)
    brickUrl = "http://images.unsplash.com/photo-1495578942200-c5f5d2137def?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max"
    app.background3 = app.scaleImage(app.loadImage(brickUrl), 1.2)

    app.gear = app.scaleImage(app.loadImage("gear-icon-png-2246.png"), 1/7)
    app.board = gameRunning_board(app)

    app.clock = app.loadImage("Clock.png")
    shovelUrl = "https://www.pngarts.com/files/3/Shovel-PNG-Free-Download.png"
    app.shovelPic = app.loadImage(shovelUrl)
    app.boom = app.loadImage("boom.png")
    #homework images
    app.regularZombie = app.scaleImage(app.loadImage("HW2normal.png"), 1/2)
    app.coneZombie = app.scaleImage(app.loadImage("HW4cone.png"), 1/2)
    app.bucketZombie = app.scaleImage(app.loadImage("HW8bucket.png"), 1/2)
    app.speedZombie = app.scaleImage(app.loadImage("HW10speed.png"), 1/2)
    app.zombiePictureList = (app.regularZombie, app.coneZombie, app.bucketZombie,
                        app.speedZombie)
    #student images
    app.student1 = app.loadImage("Student1.jpg").resize((100,100))
    app.student2 = app.loadImage("Student2.jpg").resize((100,100))
    app.student3 = app.loadImage("Student3.jpg").resize((100,100))
    app.student4 = app.loadImage("Student4.jpg").resize((100,100))
    app.student5 = app.loadImage("Student5.jpg").resize((100,100))
    app.student6 = app.loadImage("Student6.jpg").resize((100,100))
    app.studentList = (app.student1, app.student2, app.student3, app.student4,
                    app.student5, app.student6)
    app.studentNames = ("Kronos", "Peabody", "Elsa", "Mad Max", "Wal-linda", 
                    "Peabody's Sister")
    #projectile images
    rockUrl = "http://clipart-library.com/image_gallery2/Rock-PNG.png"
    app.rock = app.loadImage(rockUrl)
    app.blueRock = app.loadImage("BlueOrb.png")
    app.openMenu = False
    pass

def gameRunning_mouseMoved(app, event):
    if app.viewLawn == False:
        return
    if app.hoveredOver != None:
        app.hoveredOver = None
    for plant in app.plantsOnBoard:
        lawnViewYPosition = (300 + (600 * ((4/5)**plant.col + (4/5)**(plant.col + 1)))) / 2
        lawnViewXPosition = (app.width + 40 - ((lawnViewYPosition/3) * (4 - 2*plant.row))) / 2
        size = 50 * ((4/5)**plant.col)
        if ((lawnViewXPosition - size <= event.x <= lawnViewXPosition + size) and 
        (lawnViewYPosition - size <= event.y <= lawnViewYPosition + size)):
            app.hoveredOver = plant
    for zombie in app.zombiesOnBoard:
        zombieCol = ((zombie.position - 130) / 100)
        lawnViewYPosition = (300 + (600 * ((4/5)**zombieCol + (4/5)**(zombieCol + 1)))) / 2
        lawnViewXPosition = (app.width + 40 - ((lawnViewYPosition/2.5) * (4 - 2*zombie.row))) / 2
        size = 100 * ((4/5)**zombieCol)
        if ((lawnViewXPosition - size <= event.x <= lawnViewXPosition + size) and 
        (lawnViewYPosition - 2*size <= event.y <= lawnViewYPosition + 2*size)):
            app.hoveredOver = zombie
    pass

def viewLawnMousePressed(app, event):
    if app.selection != None:
        placePlantsOnLawn(app, event)
    if app.shovel == True:
        row, col = getLawnRowCol(app, event)
        if row != None and col != None:
            shovel(app, row, col)
    pass

def getLawnRowCol(app, event):
    row, col = None, None
    for i in range(9):
        yUpperBound = 150 + (600 * ((4/5)**i))
        yLowerBound = 150 + (600 * ((4/5)**(i + 1)))
        if yLowerBound <= event.y <= yUpperBound:
            col = i
    for i in range(5):
        xLeftBound = app.width / 2 - (2.5 - i) * (event.y/3) + 20
        xRightBound = app.width / 2 - (1.5 - i) * (event.y/3) + 20
        if xLeftBound <= event.x <= xRightBound:
            row = i
    return row, col
    
def placePlantsOnBoard(app, event):
    if (200 <= event.x <= 1100) and (218 <= event.y <= 718):
        row = (event.y - 218) // 100
        col = (event.x - 200) // 100
        for plant in app.plantsOnBoard:
            if plant.row == row and plant.col == col:
                return
        app.plantPlacements[row][col] = app.selection
        plantDefiner(app, row, col)
        app.selection = None

def placePlantsOnLawn(app, event):
    row, col = None, None
    for i in range(9):
        yUpperBound = 150 + (600 * ((4/5)**i))
        yLowerBound = 150 + (600 * ((4/5)**(i + 1)))
        if yLowerBound <= event.y <= yUpperBound:
            col = i
    if col == None:
        return
    for i in range(5):
        xLeftBound = app.width / 2 - (2.5 - i) * (event.y/3) + 20
        xRightBound = app.width / 2 - (1.5 - i) * (event.y/3) + 20
        if xLeftBound <= event.x <= xRightBound:
            row = i
    if row == None:
        return
    for plant in app.plantsOnBoard:
        if plant.row == row and plant.col == col:
            return
    app.plantPlacements[row][col] = app.selection
    plantDefiner(app, row, col)
    app.selection = None

#timerFired function while game is running
def gameRunning_timerFired(app):
    if app.gameOver == True or app.win == True or app.openMenu == True:
        return
    if time.time() - app.plantCooldowns > 1:
        for i in range(len(app.plantCooldownList)):
            if app.plantCooldownList[i] > 0:
                app.plantCooldownList[i] = app.plantCooldownList[i] - 1
        app.plantCooldowns = time.time()
    for zombie in app.zombiesOnBoard:
        zombie.zombieMove()
        if zombie.position < 180:
            app.gameOver = True
    if app.zombiesAdded < len(app.zombies):
        #time to spawn between zombies
        if time.time() - app.startTime >= 20 - 2*app.level:
            app.zombies[app.zombiesAdded].row = chooseLowestDamageRow(app)
            app.zombiesOnBoard = app.zombiesOnBoard + [app.zombies[app.zombiesAdded]]
            app.startTime = time.time()
            app.zombiesAdded = app.zombiesAdded + 1
    plantAndZombieCollide(app)
    zombieEatingPlant(app)
    sunflowerSuns(app)
    for plant in app.plantsOnBoard:
        for zombie in app.zombiesOnBoard:
            if (zombie.row == plant.row) and (zombie.position < 1200):
                plant.projectilePosition = plant.projectilePosition + 20

#manages the key press events of the game screen
def gameRunning_keyPressed(app, event):
    if app.gameOver == True or app.win == True or app.openMenu == True:
        return
    if event.key == "s":
        app.suns = app.suns + 25
    elif event.key in ("0", "1", "2", "3"):
        app.startingZombieList.append(int(event.key))
    elif event.key == "v":
        app.viewLawn = not app.viewLawn
    elif event.key == "k":
        app.level = app.level + 1
        interactions_appStarted(app)
        if app.level == 6:
            app.win = True
            return
        app.mode = "intermediateScreen"
    pass

#appStarted that handles movement and user interaction
def interactions_appStarted(app):
    if app.level == 1:
        app.plantList = ["sunflower", "peashooter"]
        app.startingZombieList = zombieListPerLevel(app)
    if app.level == 2:
        app.plantList = ["sunflower", "peashooter", "iceshooter"]
        app.startingZombieList = zombieListPerLevel(app)
    if app.level == 3:
        app.plantList = ["sunflower", "peashooter", "iceshooter", "explodingCherry"]
        app.startingZombieList = zombieListPerLevel(app)
    if app.level == 4:
        app.plantList = ["sunflower", "peashooter", "iceshooter", "explodingCherry", 
                    "walnut"]
        app.startingZombieList = zombieListPerLevel(app)
    if app.level == 5:
        app.plantList = ["sunflower", "peashooter", "iceshooter", "explodingCherry", 
                    "walnut", "doubleShooter"]
        app.startingZombieList = zombieListPerLevel(app)
    app.totalPlants = ["sunflower", "peashooter", "iceshooter", "explodingCherry", 
                    "walnut", "doubleShooter"]
    app.plantsOnBoard = []
    app.zombies = zombieDefiner(app)
    app.zombiesAdded = 0
    app.hoveredOver = None
    app.zombiesOnBoard = []
    app.startTime = time.time()
    app.costList = [50, 100, 150, 150, 50, 225]
    app.plantCooldownList = [10, 10, 15, 30, 30, 15]
    app.referenceCooldownList = [10, 10, 15, 30, 30, 15]
    app.selection = None
    app.shovel = False
    app.plantPlacements = [ [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0] ]
    app.killedZombies = []
    app.suns = 200
    app.sunList = []
    app.cherryTime = None
    app.sunflowerTime = time.time()
    app.plantCooldowns = time.time()

def zombieListPerLevel(app):
    zombieList = []
    for i in range(6 - app.level):
        for num in range(5):
            zombieList.append(0)
    for i in range(app.level):
        zombieList.append(1)
        for num in range(5):
            zombieList.append(2)
            zombieList.append(3)
    return zombieList

#defines a class of zombies
class zombies(object):
    def __init__(self, health, speed, position, row, kindOfZombie):
        self.health = health
        self.speed = speed
        self.position = position
        self.row = row
        self.kind = kindOfZombie

    def zombieMove(self):
        self.position = self.position - self.speed
        return self.position

#defines a class of plants
class plants(object):
    def __init__(self, health, kindOfPlant, row, col, damage, cost):
        self.health = health
        self.kind = kindOfPlant
        self.row = row
        self.col = col
        self.damage = damage
        self.cost = cost
        self.projectilePosition = self.col * 100 + 270

class suns(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

#defines the states of each zombie and creates a list of the instances of zombies
def zombieDefiner(app):
    allZombies = []
    for zombie in app.startingZombieList:
        if zombie == 0: #Base Zombies
            zombieInstance = zombies(10, 3, 1230, None, "base")
        elif zombie == 1: #Conehead Zombies
            zombieInstance = zombies(20, 3, 1230, None, "cone")
        elif zombie == 2: #Buckethead Zombies
            zombieInstance = zombies(30, 3, 1230, None, "bucket")
        else: #Speed Zombies
            zombieInstance = zombies(10, 6, 1230, None, "speed")
        allZombies = allZombies + [zombieInstance]
    return allZombies

#returns the best row for the zombie to spawn in
def chooseLowestDamageRow(app):
    bestRow = None
    lowestDmg = 1000
    ties = []
    if len(app.plantsOnBoard) > 0: 
        for i in range(5):
            damage = 0
            for plant in app.plantsOnBoard:
                if plant.row == i:
                    damage = damage + plant.damage
            if damage < lowestDmg:
                lowestDmg = damage
                bestRow = i
                ties = []
            elif damage == lowestDmg:
                ties = ties + [bestRow] + [i]
        if len(ties) > 0:
            return random.choice(ties)
        return bestRow
    else:
        return random.randint(0, 4)

#defines the stats of each plant
#in order of health, type, row, column, projectile damage, and price
def plantDefiner(app, row, col):
    if app.selection == "sunflower":
        plantInstance = plants(50, app.selection, row, col, 0, 50)
    elif app.selection == "peashooter":
        plantInstance = plants(50, app.selection, row, col, 1, 100)
    elif app.selection == "iceshooter":
        plantInstance = plants(50, app.selection, row, col, 1, 150)
    elif app.selection == "explodingCherry":
        plantInstance = plants(50, app.selection, row, col, 0, 150)
    elif app.selection == "walnut":
        plantInstance = plants(500, app.selection, row, col, 0, 50)
    else:
        plantInstance = plants(50, app.selection, row, col, 2, 225)
    if app.suns - plantInstance.cost >= 0:
        for i in range(len(app.plantList)):
            if (app.plantList[i] == app.selection and app.plantCooldownList[i] == 0 
            and app.gameOver == False):
                app.plantsOnBoard = app.plantsOnBoard + [plantInstance]
                app.suns = app.suns - plantInstance.cost
                if app.selection == "sunflower": app.plantCooldownList[i] = 10
                elif app.selection == "peashooter": app.plantCooldownList[i] = 10
                elif app.selection == "iceshooter": app.plantCooldownList[i] = 15
                elif app.selection == "explodingCherry": 
                    app.plantCooldownList[i] = 30
                    app.cherryTime = time.time()
                elif app.selection == "walnut": app.plantCooldownList[i] = 30
                else: app.plantCooldownList[i] = 15
    else:
        app.plantPlacements[row][col] = 0
        
#handles the plants shooting zombies and zombies eating plants
def plantAndZombieCollide(app):
    for plant in app.plantsOnBoard:
        plantXCoord = plant.col * 100 + 270
        if plant.kind != "explodingCherry":
            for i in range(5):
                leftZombie = leftestZombieInRow(app, i, plantXCoord - 20)
                #plants shooting zombies
                if leftZombie != None:
                    if leftZombie.row == plant.row:
                        if plant.projectilePosition + 10 >= leftZombie.position:
                            leftZombie.health = leftZombie.health - plant.damage
                            if plant.kind == "iceshooter":
                            #zombie slowing
                                if leftZombie.kind == "speed":
                                    if leftZombie.speed == 6:
                                        leftZombie.speed = 18 / 4
                                else:
                                    if leftZombie.speed == 3:
                                        leftZombie.speed = 9 / 4
                            plant.projectilePosition = plantXCoord
                            #removal of zombie if its health reaches 0
                            if leftZombie.health <= 0:
                                app.zombiesOnBoard.remove(leftZombie)
                                app.killedZombies.append(leftZombie)
        else: #exploding cherry
            if time.time() - app.cherryTime >= 1:
                for zombie in app.zombiesOnBoard:
                    if ((plantXCoord - 150 <= zombie.position <= plantXCoord + 150)
                    and (plant.row - 1 <= zombie.row <= plant.row + 1)):
                        app.zombiesOnBoard.remove(zombie)
                        app.killedZombies.append(zombie)
                app.plantsOnBoard.remove(plant)
                app.cherryTime = None
    #move onto next level when all the zombies are killed
    if len(app.killedZombies) == len(app.zombies):
        app.level = app.level + 1
        if app.level == 6:
            app.win = True
            return
        interactions_appStarted(app)
        app.mode = "intermediateScreen"
                                 
#edits plant health as zombies eat it
def zombieEatingPlant(app):
    for zombie in app.zombiesOnBoard:
        for plant in app.plantsOnBoard:
            plantXCoord = plant.col * 100 + 270
            if zombie.row == plant.row:
                if plantXCoord - 20 <= zombie.position <= plantXCoord:
                    zombie.speed = 0
                    plant.health = plant.health - 1
                    #removes plant if plant health reaches 0
                    if plant.health <= 0:
                        if plant in app.plantsOnBoard:
                            app.plantsOnBoard.remove(plant)
                            for zombie in app.zombiesOnBoard:
                                if ((zombie.row == plant.row) and 
                                (plantXCoord - 20 <= zombie.position <= plantXCoord)):
                                    #resets zombie speeds if ice shooter dies
                                    if zombie.kind == "speed":
                                        zombie.speed = 6
                                    else:
                                        zombie.speed = 3
            
#returns a dictionary that maps each zombie to each row
def leftestZombieInRow(app, row, plantPosition):
    leftest = 10000
    leftestZombie = None
    for zombie in app.zombiesOnBoard:
        if zombie.row == row:
            if (zombie.position < leftest) and (zombie.position >= plantPosition):
                leftest = zombie.position
                leftestZombie = zombie
    return leftestZombie

#given the location of the click, removes the plant in that tile
def shovel(app, row, col):
    app.shovel = False
    app.plantPlacements[row][col] == 0
    for plant in app.plantsOnBoard:
        if plant.row == row and plant.col == col:
            app.plantsOnBoard.remove(plant)
            plantXCoord = plant.col * 100 + 270
            for zombie in app.zombiesOnBoard:
                if ((zombie.row == plant.row) and 
                    (plantXCoord - 20 <= zombie.position <= plantXCoord)):
                        #resets speed of zombie if ice shooter is removed
                        if zombie.kind == "speed":
                            zombie.speed = 6
                        else:
                            zombie.speed = 3

#adds suns for each sunflower as time goes on
def sunflowerSuns(app):
    if time.time() - app.sunflowerTime >= 4:
        for plant in app.plantsOnBoard:
            if plant.kind == "sunflower":
                app.sunflowerTime = time.time()
                chance = random.randint(0, 3)
                if chance == 0:
                    sunInstance = suns(plant.col * 100 + 250 + random.randint(0, 25), 
                                    plant.row * 100 + 270 + random.randint(0, 25))
                    app.sunList = app.sunList + [sunInstance]
