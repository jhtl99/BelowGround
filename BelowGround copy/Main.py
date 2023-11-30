from level import *
from button import *
from chef import *
from producer import*
from cmu_graphics import *
from station import *
from plate import *
from PIL import Image



def onAppStart(app):
    app.states = ["Start", "Paused", "Level1", "Level2"]

    #chef image from https://www.creativefabrica.com/product/cute-animal-chef/
    app.chefPNG = Image.open('images/chef.png')
    
    app.stepsPerSecond = 60
    app.mouseX = 0
    app.mouseY = 0
    app.state = app.states[0]
    app.width = 1000
    app.height = 600
    app.moveSpeed = 5
    
    dim1 = (12, 6)
    app.chefPNG = CMUImage(app.chefPNG.resize((int(app.width/dim1[0]*2.5),int(app.width/dim1[0]*2))))
    app.startButton = Button(app.width/2, app.height * 0.7, 300, 80, "Click to start!", "turquoise", "black", True)
    
    # (row, col) eg (y, x)
    counterCoords1 = []
    for i in range(12):
        counterCoords1.append((0,i))
        counterCoords1.append((5,i))
    for i in range(1,5):
        counterCoords1.append((i,0))
        counterCoords1.append((i,11))
    ''''''
    

    app.currCounters = counterCoords1
    # Create Producer ingredients
    producerList1 = dict()
    tomato1 = Ingredient(1, 0, "Tomato", "red")
    onion1 = Ingredient(0, 2, "Onion", "purple")
    lettuce1 = Ingredient(0, 4, "Lettuce", "lightgreen")
    patty1 = Ingredient(0, 7, "Raw Patty", "fireBrick")

    # Plate producer
    plateList1 = dict()
    p1pos = (0,5)
    p2pos = (0,6)
    plate1 = Plate(p1pos[0],p1pos[1])
    plate2 = Plate(p2pos[0],p2pos[1])
    plateList1[p1pos] = plate1
    plateList1[p2pos] = plate2

    #Create Producers
    tomatoProducer1 = Producer(tomato1)
    onionProducer1 = Producer(onion1)
    pattyProducer1 = Producer(patty1)

    #Add producers to list
    producerList1[(tomato1.row, tomato1.col)] = tomatoProducer1
    producerList1[(onion1.row, onion1.col)] = onionProducer1
    producerList1[(patty1.row, patty1.col)] = pattyProducer1
    
    
    
    #If I want to hard code some ingredients that start
    ingredientList1 = dict()
    #ingredientList1[tomato1.coords()] = tomato1
    #ingredientList1[onion1.coords()] = onion1

    #Create stations
    stationList1 = dict()
    cuttingStation1 = Station(5, 3, "Chop", "gray", 1/300, False)
    grillingStation1 = Station(5,7, "Grill", "orange", 1/600, True)
    stationList1[(cuttingStation1.row, cuttingStation1.col)] = cuttingStation1
    stationList1[(grillingStation1.row, grillingStation1.col)] = grillingStation1

    app.level1 = Level(dim1, app.width, app.height, counterCoords1, (3,3), ingredientList1, producerList1, stationList1, plateList1)
    app.currLevel = app.level1
    app.chef = Chef(app.level1.getStartCol(), app.level1.getStartRow())
    app.chefRadius = app.chef.r


def redrawAll(app):
    if app.state == "Start":
        app.startButton.draw()
    elif app.state == "Level1":
        app.level1.drawLevel()
        drawImage(app.chefPNG, app.chef.x, app.chef.y-app.currLevel.cellHeight*0.3, align = 'center')


def onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY
    if app.state == "Start":
        app.startButton.update(mouseX, mouseY)

def onMousePress(app, mouseX, mouseY):
    if app.startButton.hover:
        app.state = "Level1"
        app.startButton.hide()

def onStep(app):
    dx = 0
    dy = 0
    if app.chef.direction == "down":
        dy += app.currLevel.cellHeight
    if app.chef.direction == "right":
        dx += app.currLevel.cellWidth
    if app.chef.direction == "up":
        dy -= app.currLevel.cellHeight
    if app.chef.direction == "left":
        dx -= app.currLevel.cellWidth

    
    
    app.currLevel.selectCell(app.chef.x + dx, app.chef.y + dy)
    
    app.currLevel.updateCooking()

    #iterate timer
    pass

def collide(app, x, y):
    
    height = app.currLevel.cellHeight
    width = app.currLevel.cellWidth

    

    #assumes the chef is a square

    chefTop = y - app.chef.r
    chefBot = y + app.chef.r
    chefLeft = x - app.chef.r
    chefRight = x + app.chef.r

    for cRow, cCol in app.currCounters:
        cTop = cRow * height
        cBot = (cRow + 1) * height
        cLeft = cCol * width
        cRight = (cCol+1) * width
        if chefTop < cBot and chefBot > cTop and chefLeft < cRight and chefRight > cLeft:
            return True
    return False


def onKeyHold(app, keys):
    if len(keys) > 1:
        moveDistance = app.moveSpeed/(2**0.5)
    else:
        moveDistance = app.moveSpeed
    
    #how many pixels should be left between chef and counter
    gap = 15
    if "up" in keys:
        app.chef.direction = "up"
        if not collide(app, app.chef.x, app.chef.y-gap):
            app.chef.y -= moveDistance
        
    if "down" in keys:
        app.chef.direction = "down"
        if not collide(app, app.chef.x, app.chef.y+gap):
            app.chef.y += moveDistance
       
    if "right" in keys:
        app.chef.direction = "right"
        if not collide(app, app.chef.x+gap, app.chef.y):
            app.chef.x += moveDistance
    if "left" in keys:
        app.chef.direction = "left"
        if not collide(app, app.chef.x-gap, app.chef.y):
            app.chef.x -= moveDistance

def onKeyPress(app, key):
    if key == 'space':
        app.level1.interact()
    

runApp()

