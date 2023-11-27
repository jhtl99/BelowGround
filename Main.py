from level import *
from button import *
from chef import *
from cmu_graphics import *

def onAppStart(app):
    app.states = ["Start", "Paused", "Level1", "Level2"]
    app.startButton = Button(50, 50, 100, 50, "Hello", "yellow", "black", True)
    app.stepsPerSecond = 30
    app.mouseX = 0
    app.mouseY = 0
    app.state = app.states[0]
    app.width = 1000
    app.height = 600
    
    dim1 = (20, 10)
    
    # (row, col) eg (y, x)
    counterCoords1 = [(0, 0), (0,1), (0,2), (0,3), (1, 0), (2, 0), (3, 0), (8, 15), (9, 15)]

    app.level1 = Level(dim1, app.width, app.height, counterCoords1, (8,5))
    app.currLevel = app.level1
    app.chef = Chef(app.level1.getStartCol(), app.level1.getStartRow())
    


def redrawAll(app):
    if app.state == "Start":
        app.startButton.draw()
    elif app.state == "Level1":
        app.level1.drawLevel()
        app.chef.draw()


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
    
    #iterate timer
    pass

def onKeyHold(app, keys):
    if "up" in keys:
        app.chef.y -= 5
        app.chef.direction = "up"
    if "down" in keys:
        app.chef.y += 5
        app.chef.direction = "down"
    if "right" in keys:
        app.chef.x += 5
        app.chef.direction = "right"
    if "left" in keys:
        app.chef.x -=5
        app.chef.direction = "left"

def onKeyPress(app, key):
    if key == 'space':
        app.level1.interact()
    

runApp()

