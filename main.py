#calls the gameFuncitions and gameRunningDrawFunctions File
import random, time, copy, math, decimal
from cmu_112_graphics import *
from gameFunctions import *
from gameRunningDrawFunctions import *

############# 15-112 Term Project ##############
# Name: Ryan Lin                               #
# AndrewID: rlin2                              #
################################################

#Plant and Zombie ideas, as well as the gameplay, is inspired by Plants vs Zombies
######################### Citations #########################

#grass from https://www.chippenham.gov.uk/wp-content/uploads/2020/09/grounds-maintainence-1000-x-426.jpg
#brick background from http://images.unsplash.com/photo-1495578942200-c5f5d2137def?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max
#gear from https://www.freeiconspng.com/downloadimg/2246
#clock from https://www.pngitem.com/middle/hwooJiR_transparent-background-clock-clipart-hd-png-download/
#snowflake from https://www.stickpng.com/img/download/5846a02acef1014c0b5e47fa
#rock from http://clipart-library.com/image_gallery2/Rock-PNG.png
#blue "rock" from https://lh3.googleusercontent.com/proxy/sJd-qEFdf44BqGTYxGfGssrDdIShDsi22edP663w7D4QqDlevTTczSljFwKi889JYGKBdexcqIi_pIAmvC3kXuY
#shovel image from https://www.pngarts.com/files/3/Shovel-PNG-Free-Download.png
#boom from https://lh3.googleusercontent.com/proxy/GLWvfZRgV0AWAMBKAvTF8MfK6vodvUuF47jGBNsH-W9XSrcjKzoLT3CMs82KG7tB3nOD9c72mdmt-3MB-ivEuqQQ8wiMm-MUzb-6GUka0NJ2PGYbF2vLC8usNMw
#student1 from https://www.collegegrant.net/images/college-student.jpg
#student2 from https://www.pngkit.com/png/detail/237-2372133_college-student-transparent-background.png
#student3 from https://s.clipartkey.com/mpngs/s/130-1303947_student-png-images-free-download-girl-student-image.png
#student4 from https://st.depositphotos.com/1771835/1477/i/600/depositphotos_14779185-stock-photo-confident-young-student-back-to.jpg
#student5 from https://media.istockphoto.com/photos/confident-female-college-student-picture-id481212580?k=6&m=481212580&s=612x612&w=0&h=zw1Or4chTMAZGfU4kQWGwciiJH4crqWti6aFap5z4zY=
#student6 from https://thumbs.dreamstime.com/b/college-student-standing-white-background-15264232.jpg

######################### Game Code #########################

#calls all other appStarted functions
def appStarted(app):
    app.mode = "mainMenu"
    app.gameStarted = False
    app.gameOver = False
    app.win = False
    app.viewLawn = False
    app.level = 1
    mainMenu_appStarted(app)
    gameRunning_appStarted(app)
    gallery_appStarted(app)
    intermediate_appStarted(app)
    interactions_appStarted(app)

################## Main Menu ###################

#appStarted for the title screen
#code background from https://c0.wallpaperflare.com/preview/84/694/443/codes-coding-css-css3.jpg
def mainMenu_appStarted(app):
    app.title = app.scaleImage(app.loadImage("Title.png"), 1.5)
    backgroundUrl = "https://c0.wallpaperflare.com/preview/84/694/443/codes-coding-css-css3.jpg"
    app.titleBackground = app.scaleImage(app.loadImage(backgroundUrl), 1.5)
    app.buttonY1 = app.height/2 + 80
    app.buttonY2 = app.height/2 + 150

#handles the mouse press events for the main screen
def mainMenu_mousePressed(app, event):
    if app.mode != "mainMenu":
        return
    if ((app.width/2 - 250 <= event.x <= app.width/2 - 10) and 
        (app.buttonY1 <= event.y <= app.buttonY2)):
        app.mode = "gameRunning"
        app.gameStarted = True
    if ((app.width/2 + 10 <= event.x <= app.width/2 + 250) and 
        (app.buttonY1 <= event.y <= app.buttonY2)):
        app.mode = "helpScreen"
    
#draws the title and calls other draw functions to draw the buttons
def mainMenu_redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
                        image=ImageTk.PhotoImage(app.titleBackground))
    canvas.create_image(app.width/2, app.height/2.5, 
                        image=ImageTk.PhotoImage(app.title))
    mainMenu_drawButtons(app, canvas)

#draws the start and help buttons on the main screen
def mainMenu_drawButtons(app, canvas):
    #Start button
    canvas.create_rectangle(app.width/2 - 250, app.buttonY1, 
                        app.width/2 - 10, app.buttonY2, 
                        fill="orange", width=5)
    if app.gameStarted == False:
        message = "Start Game"
    else:
        message = "Resume Game"
    canvas.create_text((app.width - 260)/2, (app.buttonY1 + app.buttonY2)/2, 
                        text=message, font="Arial 28 bold")
    #Rules/Gallery button
    canvas.create_rectangle(app.width/2 + 10, app.buttonY1, app.width/2 + 250, 
                        app.buttonY2, fill="grey", width=5)
    canvas.create_text((app.width + 260)/2, (app.buttonY1 + app.buttonY2)/2, 
                        text="Rules/Gallery",font="Arial 28 bold")

################# Help Screen ##################

#manages the mouse press events in the help screen
def helpScreen_mousePressed(app, event):
    if ((app.width/2 - 210 <= event.x <= app.width/2 - 10) and 
        (6*app.height/7 <= event.y <= 6*app.height/7 + 60)):
        app.mode = "mainMenu"
    elif ((app.width/2 + 10 <= event.x <= app.width/2 + 210) and 
        (6*app.height/7 <= event.y <= 6*app.height/7 + 60)):
        app.mode = "gallery"

#draws or calls everything in the help screen
def helpScreen_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="LightSteelBlue1")
    drawRulesAndExplanations(app, canvas)
    #Back Button
    canvas.create_rectangle(app.width/2 - 200, 6*app.height/7, 
                            app.width/2 - 10, 6*app.height/7 + 60, 
                            fill="grey", width=5)
    canvas.create_text(app.width/2 - 105, 6*app.height/7 + 30, 
                    text="Main Menu", font="Arial 28 bold")
    #Gallery Button
    canvas.create_rectangle(app.width/2 + 10, 6*app.height/7,
                            app.width/2 + 210, 6*app.height/7 + 60,
                            fill="brown", width=5)
    canvas.create_text(app.width/2 + 105, 6*app.height/7 + 30, 
                    text="Gallery", font="Arial 28 bold")

#draws the text explaning the all the rules
def drawRulesAndExplanations(app, canvas):
    canvas.create_text(50, 50, text="Rules and Explanations", 
                    font="Times 50 bold", anchor=W)
    canvas.create_text(50, 80, text="________________________________________\
________________________________", 
                    font="bold", anchor=W)
    rules = ["- Place down students in order to fight off incoming homework.",
            "- The clock is your in-game currency. Use it to buy students.", 
            "- Click the shovel and click a square to remove the student on that square.",
            "- Homework spawns on the right and if they reach the left side of the lawn, you fail.",
            "- Defeat all the homework to reach the next round.",
            "- Each student has different attributes. Explore them in the Gallery.", 
            "- Each homework has different attributes. Explore them in the Gallery."]
    for i in range(len(rules)):
        line = rules[i]
        canvas.create_text(50, 120 + i*60, text=line, font="times 30 bold", 
                        anchor=W)
    
############### Gallery Screen #################

def plantDescriptions(app):
    information = [
"""
Kronos
-----------------------
Other than being a 112
student, Kronos is 
secretly the titan of 
time. He has an ability 
to just generate time 
at his will.


Health: 5
Damage: None
""",
"""
Peabody
-----------------------
As a Luigi fanboy, 
Peabody loves to fight 
adversaries and throw 
rocks at homeworks, 
even if the homework
is digital. He is 
known as a very 
dependable person.


Health: 5
Damage: 1
""",
"""
Elsa
-----------------------
Perhaps her parents 
fell in love with 
Frozen(tm), but she 
has lived up to her 
name. Known as a very
cold person, she 
extends her aura to 
homework.


Health: 5
Damage: 1
Perks: Slowing Factor
""",
"""
Mad Max
-----------------------
Diagnosed with being 
mad as a child, Mad 
Max has a tumultuous 
history with social 
workers. He explodes
with anger at his 
homework often.


Health: Doesn't matter
Damage: Defeat all
Perks: He leaves quickly
""",
"""
Wal-linda
-----------------------
Joining MENSA at an
age of "while still
in the womb", Wal-linda
breezes through the 
work and has somewhat
gotten complacent. 
Homework builds up 
and she tries to hold 
it back.


Health: 50
Damage: None
""",
"""
Peabody's Sister
-----------------------
Sadly, everyone knows 
that Peabody's sister 
is better than Peabody 
in every way. Even at
throwing rocks at 
homework. How oddly 
specific is that??


Health: 50
Damage: 2
"""]
    return information

def zombieDescriptions(app):
    information = [
"""
Homework 2
-----------------------
Born from the brains
of some genius 
scientists but became
evil over time, 
Homework 2 used math
in order to fight 
against the students.


Health: 10
""",
"""
Homework 4
-----------------------
Forged in the depths 
of the CS department, 
Homework 2 was one of
the first challenges 
the students faced in
the realm of 
animations.


Health: 20
""",
"""
Homework 8
-----------------------
Pitting students 
against one of the
most beloved games
of all time, students
were forced to put 
down their nostalgia,
making Homework 8 
harder to defeat.


Health: 30
""",
"""
Homework 10
-----------------------
Trying to intimidate
students with the 
increasing depths
of recursion, the 
experienced students
would have to 
dispatch it quickly
in order to win.


Health: 10
Speed: 2x
"""]
    return information

def gallery_appStarted(app):
    app.studentSelection = None
    app.zombieSelection = None
    app.plantMessages = plantDescriptions(app)
    app.zombieMessages = zombieDescriptions(app)

def gallery_mousePressed(app, event):
    for i in range(len(app.studentList)):
        if ((30 <= event.x <= 130) and 
        ((i + 1) * 125 - 90 <= event.y<= (i + 1) * 125 + 10)):
            app.studentSelection = app.studentList[i]
            return
    for i in range(len(app.zombiePictureList)):
        if ((app.width/2 + 20 <= event.x <= app.width/2 + 80)
        and ((i + 1) * 120 - 100 <= event.y <= (i + 1) * 120 + 20)):
            app.zombieSelection = app.zombiePictureList[i]
            return
    if ((app.width - 450 <= event.x <= app.width - 30) and 
    (app.height - 110 <= event.y <= app.height - 30)):
        app.mode = "helpScreen"
    app.studentSelection = None
    app.zombieSelection = None
    
def gallery_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="peach puff")
    drawPlantZombieInfo(app, canvas)
    #back button
    canvas.create_rectangle(app.width - 450, app.height - 110, app.width - 30, 
                        app.height - 30, fill="grey", width=5)
    canvas.create_text(app.width - 240, app.height - 70, text="Back to Rules",
                        font="arial 30 bold")

def drawPlantZombieInfo(app, canvas):
    for i in range(len(app.studentList)):
        student = app.studentList[i]
        canvas.create_image(80, (i + 1) * 125 - 40, 
                            image=ImageTk.PhotoImage(student))
    for i in range(len(app.zombiePictureList)):
        zombie = app.scaleImage(app.zombiePictureList[i], 1.3)
        canvas.create_image(app.width/2 + 50, (i + 1) * 120 - 40, 
                            image=ImageTk.PhotoImage(zombie))
    if app.studentSelection != None:
        canvas.create_oval(160, 30, 220, 90, fill="wheat1", width=0)
        canvas.create_oval(app.width/2 - 60, 30, app.width/2, 90, 
                        fill="wheat1", width=0)
        canvas.create_oval(160, app.height - 90, 220, app.height - 30, 
                        fill="wheat1", width=0)
        canvas.create_oval(app.width/2 - 60, app.height -90, app.width/2, 
                        app.height - 30, fill="wheat1", width=0)
        canvas.create_rectangle(190, 30, app.width/2 - 30, app.height - 30, 
                        fill="wheat1", width=0)
        canvas.create_rectangle(160, 60, app.width/2, app.height - 60, 
                        fill="wheat1", width=0)
    if app.zombieSelection != None:
        canvas.create_oval(app.width/2 + 130, 30, app.width/ 2 + 190, 90, 
                        fill="wheat1", width=0)
        canvas.create_oval(app.width - 90, 30, app.width - 30, 90, 
                        fill="wheat1", width=0)
        canvas.create_oval(app.width/2 + 130, app.height - 200, app.width/2 + 190, app.height - 140, 
                        fill="wheat1", width=0)
        canvas.create_oval(app.width - 90, app.height - 200, app.width - 30, 
                        app.height - 140, fill="wheat1", width=0)
        canvas.create_rectangle(app.width/2 + 160, 30, app.width - 60, app.height - 140, 
                        fill="wheat1", width=0)
        canvas.create_rectangle(app.width/2 + 130, 60, app.width - 30, app.height - 170, 
                        fill="wheat1", width=0)
    for i in range(len(app.studentList)):
        if app.studentList[i] == app.studentSelection:
            canvas.create_text(app.width/4 - 100, 50, text=app.plantMessages[i], 
                            font="arial 30", fill="grey27", anchor=NW)
    for i in range(len(app.zombiePictureList)):
        if app.zombiePictureList[i] == app.zombieSelection:
            canvas.create_text(3*app.width/4 - 130, 50, text=app.zombieMessages[i],
                            font="arial 30", fill="grey27", anchor=NW)
    

############# Intermediate Screen ##############

def intermediate_appStarted(app):
    app.studentShortInfo = [ 
"""
    Elsa is known for being cold and distant.
    Although she works on her homework as 
    well as others, she likes to procrastinate 
    and ask for extensions. Notice what she 
    does to the speed of the homework.""", 
"""
    Mad Max is a kid with anger issues. While 
    doing homework, he gets stuck and 
    becomes enraged, ripping all of his 
    homework to shreds.""", 
"""
    Wal-linda is a brainiac and has built up 
    so much extra credit at the start of the 
    semester that she doesn't care about 
    homework anymore. She blocks all 
    homework that comes her way.""", 
"""
    Peabody's sister will always be better 
    than poor Peabody because she is a natural 
    at coding, getting through homework faster 
    than anyone else."""]

def intermediateScreen_mousePressed(app, event):
    if ((app.width - 330 <= event.x <= app.width - 30) and 
    (app.height - 130 <= event.y <= app.height - 30)):
        app.mode = "gameRunning"

def intermediateScreen_keyPressed(app, event):
    if event.key == "Enter":
        app.mode = "gameRunning"

def intermediateScreen_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="NavajoWhite3")
    canvas.create_rectangle(app.width - 330, app.height - 130, 
                        app.width - 30, app.height - 30, fill="grey", width=5)
    canvas.create_text(app.width - 180, app.height - 80, text="Next Level",
                        font="arial 40 bold")
    drawLevelMessage(app, canvas)
    drawCharacterDescription(app, canvas)
    drawHomeworkStatus(app, canvas)

def drawLevelMessage(app, canvas):
    canvas.create_oval(300, 60, 380, 140, fill="ivory2", width=0)
    canvas.create_oval(820, 60, 900, 140, fill="ivory2", width=0)
    canvas.create_rectangle(340, 60, 860, 140, fill="ivory2", width=0)
    canvas.create_text(app.width/2, 100, text=f"You Reached Level {app.level}!",
                    fill="grey27", font="arial 50 bold")
    canvas.create_rectangle(app.width/4 - 190, app.height/2 - 190, app.width/4 + 260,
                        app.height/2 + 210, fill="black")
    canvas.create_rectangle(app.width/4 - 200, app.height/2 - 200, app.width/4 + 250, 
                        app.height/2 + 200, fill="bisque", width=0)
    unlockedCharacter = app.studentNames[app.level]
    if unlockedCharacter == "Peabody's Sister":
        canvas.create_text(app.width/4 + 25, app.height/2 - 150, 
                    text=f"You unlocked Peabody's\n                Sister:",
                    fill="grey27", font="arial 30 bold")
    else:
        canvas.create_text(app.width/4 + 25, app.height/2 - 150, 
                    text=f"You unlocked {unlockedCharacter}:",
                    fill="grey27", font="arial 30 bold")
    canvas.create_image(app.width/4 + 25, app.height/2, 
    image=ImageTk.PhotoImage(app.scaleImage(app.studentList[app.level], 2)))

def drawCharacterDescription(app, canvas):
    canvas.create_rectangle(3*app.width/4 - 240, app.height/2 - 190, 
                            3*app.width/4 + 210, app.height/2, fill="black")
    canvas.create_rectangle(3*app.width/4 - 250, app.height/2 - 200, 
                            3*app.width/4 + 200, app.height/2 - 10, 
                            fill="bisque", width=0)
    characterDescrip = app.studentShortInfo[app.level - 2]
    canvas.create_text(app.width/2 + 45, app.height/2 - 140, 
                    text=characterDescrip, font="arial 20 bold", fill="grey27", 
                    anchor=W)

def drawHomeworkStatus(app, canvas):
    canvas.create_rectangle(3*app.width/4 - 240, app.height/2 + 20, 
                            3*app.width/4 + 210, app.height/2 + 210, fill="black")
    canvas.create_rectangle(3*app.width/4 - 250, app.height/2 + 10, 
                            3*app.width/4 + 200, app.height/2 + 200, 
                            fill="bisque", width=0)
    for i in range(len(app.zombiePictureList)):
        image = app.zombiePictureList[i]
        canvas.create_image(app.width/2 + 100 * i + 130, app.height/2 + 80,
                            image=ImageTk.PhotoImage(image))
    canvas.create_text(3*app.width/4 - 15, app.height/2 + 160, 
                    text="Harder homeworks will spawn more frequently!",
                    font="arial 20 bold", fill="grey27")

#manages the drawing of background and user interface
def gameRunning_redrawAll(app, canvas):
    if app.viewLawn == False:
        drawBackgroundAndField(app, canvas)
    else:
        draw3dField(app, canvas)
    drawSunCount(app, canvas)
    if app.viewLawn == False:
        canvas.create_text(app.width/2, 70, text="Normal Mode", 
                    fill="dodger blue", font="arial 15 bold")
        drawPlants(app, canvas)
        drawZombies(app, canvas)
        drawProjectiles(app, canvas)
        drawSuns(app, canvas)
    else:
        viewLawnDrawZombies(app, canvas)
        viewLawnDrawPlants(app, canvas)
        viewLawnDrawProjectiles(app, canvas)
        viewLawnInformation(app, canvas)
    drawZombieProgressBar(app, canvas)
    drawPlantMenu(app, canvas)
    drawShovel(app, canvas)
    if app.win == True or app.gameOver == True:
        drawGameOver(app, canvas)
    if app.openMenu == True:
        drawMenu(app, canvas)

#manages the mouse press events of the game screen
def gameRunning_mousePressed(app, event):
    if app.gameOver == True or app.win == True:
        if ((app.width/2 - 100 <= event.x <= app.width/2 + 100) and 
        (app.height/2 <= event.y <= app.height/2 + 50)):
            app.mode = "mainMenu"
            appStarted(app)
    if app.shovel == False:
        if (200 <= event.x <= 400) and (20 <= event.y <= 80):
            app.shovel = True
    if app.openMenu == True:
        if (app.width - 80 <= event.x <= app.width) and (0 <= event.y <= 80):
            app.openMenu = False
        elif ((app.width/2 - 180 <= event.x <= app.width/2 - 10)
            and (app.height/2 + 40 <= event.y <= app.height/2 + 80)):
            app.mode = "mainMenu"
            app.openMenu = False
        elif ((app.width/2 + 10 <= event.x <= app.width/2 + 180)
            and (app.height/2 + 40 <= event.y <= app.height/2 + 80)):
            appStarted(app)
            app.openMenu = False
            app.gameStarted = True
            app.mode = "gameRunning"
    #clicking gear to open settings
    elif (app.width - 80 <= event.x <= app.width) and (0 <= event.y <= 80):
        app.openMenu = True
    for i in range(len(app.plantList)): #clicking plants to place down
        if ((30 <= event.x <= 130) and 
        ((i + 1) * 110 - 10 <= event.y <= (i + 1) * 110 + 90)):
            app.selection = app.plantList[i]
    for sun in app.sunList:
        if ((sun.x - 20 <= event.x <= sun.x + 20) and 
        (sun.y - 20 <= event.y <= sun.y + 20)):
            app.suns = app.suns + 25
            app.sunList.remove(sun)
    if app.viewLawn == True:
        viewLawnMousePressed(app, event)
        return
    if app.selection != None and app.openMenu == False:
        placePlantsOnBoard(app, event)
    if app.shovel == True:
        if (200 <= event.x <= 1100) and (218 <= event.y <= 718):
            row = (event.y - 218) // 100
            col = (event.x - 200) // 100
            shovel(app, row, col)

runApp(width=1200,height=800)