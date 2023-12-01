from level import *
from button import *
from chef import *
from producer import*
from cmu_graphics import *
from station import *
from plate import *
from order import *
from PIL import Image


def onAppStart(app):
    app.states = ["Start", "Paused", "Level1", "Level2"]

    #chef image from https://www.creativefabrica.com/product/cute-animal-chef/
    app.chefPNG = Image.open('images/chef.png')
    
    app.orderTimer = 100
    app.stepsPerSecond = 60
    app.mouseX = 0
    app.mouseY = 0
    app.state = app.states[0]
    app.width = 1300
    app.height = 1000
    app.moveSpeed = 8
    app.chefRow = None
    app.chefCol = None

    
    

    app.dim = (12, 6)
    app.chefPNG = CMUImage(app.chefPNG.resize((int(app.width/app.dim[0]*2.5),int(app.width/app.dim[1]))))
    app.startButton = Button(app.width/2, app.height * 0.7, 300, 80, "Click to start!", "turquoise", "black", True)
    app.pauseButton = Button(10, 10, 50, 50, "Pause", "white", "black", True)
    app.findButton = Button(50, app.height*0.6, 150, 100, "Where to take ingredient?", "lightgrey", "cyan", True,)


    
    # (row, col) eg (y, x)
    counterCoords1 = []
    for i in range(12):
        counterCoords1.append((0,i))
        counterCoords1.append((5,i))
    for i in range(1,5):
        counterCoords1.append((i,0))
        counterCoords1.append((i,11))
    counterCoords1.append((1, 7))
    counterCoords1.append((2, 7))
    counterCoords1.append((3, 4))
    counterCoords1.append((4, 4))

    


    app.currCounters = counterCoords1
    # Create Producer ingredients
    producerList1 = dict()
    
    #from https://www.vectorstock.com/royalty-free-vector/tomato-isolated-single-simple-cartoon-flat-style-vector-24046801
    app.tomatoPNG = Image.open('images/Tomato.png')
    app.tomatoPNG = CMUImage(app.tomatoPNG.resize((70,70)))
    tomato1 = Ingredient(1, 0, "Tomato", "red", app.tomatoPNG)
    
    #from https://www.vecteezy.com/vector-art/7938448-simple-vector-image-of-sliced-onion
    app.onionPNG = Image.open('images/Onion.png')
    app.onionPNG = CMUImage(app.onionPNG.resize((70,70)))
    onion1 = Ingredient(0, 2, "Onion", "purple", app.onionPNG)

    
    #from https://www.vectorstock.com/royalty-free-vector/lettuce-vector-14797363
    app.lettucePNG = Image.open('images/Lettuce.png')
    app.lettucePNG = CMUImage(app.lettucePNG.resize((70,70)))
    lettuce1 = Ingredient(0, 4, "Lettuce", "lightgreen", app.lettucePNG)
    
    #from https://www.vectorstock.com/royalty-free-vector/burger-patty-minced-meat-flattened-and-round-vector-40056216
    app.rawPattyPNG = Image.open('images/Raw Patty.png')
    app.rawPattyPNG = CMUImage(app.rawPattyPNG.resize((100,100)))
    patty1 = Ingredient(0, 8, "Raw Patty", "fireBrick", app.rawPattyPNG)

    #from https://www.vectorstock.com/royalty-free-vector/lush-buns-for-delicious-burgers-flat-cartoon-vector-34194943
    app.bunPNG = Image.open('images/Bun.png')
    app.bunPNG = CMUImage(app.bunPNG.resize((80,80)))
    bun1 = Ingredient(5, 1, "Bun", "orange", app.bunPNG)

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
    lettuceProducer1 = Producer(lettuce1)
    bunProducer1 = Producer(bun1)

    #Add producers to list
    producerList1[(tomato1.row, tomato1.col)] = tomatoProducer1
    producerList1[(onion1.row, onion1.col)] = onionProducer1
    producerList1[(patty1.row, patty1.col)] = pattyProducer1
    producerList1[(lettuce1.row, lettuce1.col)] = lettuceProducer1
    producerList1[(bun1.row, bun1.col)] = bunProducer1
    
    
    
    #If I want to hard code some ingredients that start
    ingredientList1 = dict()
    #ingredientList1[tomato1.coords()] = tomato1
    #ingredientList1[onion1.coords()] = onion1

    #Create stations
    stationList1 = dict()
    cuttingStation1 = Station(5, 3, "Chop", "gray", 1/(60*1), False)
    grillingStation1 = Station(5,7, "Grill", "orange", 1/(60*10), True)
    stationList1[(cuttingStation1.row, cuttingStation1.col)] = cuttingStation1
    stationList1[(grillingStation1.row, grillingStation1.col)] = grillingStation1

    #Trash location
    trashCoords1 = (0,1)

    #Window coordinates
    windowCoords1 = ((4,11),(3, 11))

    app.level1 = Level(app.dim, app.width, app.height, counterCoords1, (3,3), ingredientList1, producerList1, stationList1, plateList1, trashCoords1, windowCoords1)
    app.currLevel = app.level1
    app.levelNum = 1
    app.chef = Chef(app.level1.getStartCol(), app.level1.getStartRow())
    app.chefRadius = app.chef.r


def redrawAll(app):
    if app.state == "Start":
        app.startButton.draw()
    elif app.state == "Pause":
        app.pauseButton.draw()
    elif app.state == "Level1":
        app.level1.drawLevel()
        app.level1.drawInventory()
        app.level1.drawOrders()
        app.findButton.draw()
        app.pauseButton.draw()
        drawImage(app.chefPNG, app.chef.x, app.chef.y-app.currLevel.cellHeight*0.3, align = 'center')

        drawLabel(f"Money: {app.currLevel.money}", 800, 700)
    



def onMouseMove(app, mouseX, mouseY):
    app.mouseX = mouseX
    app.mouseY = mouseY
    if app.state == "Start":
        app.startButton.update(mouseX, mouseY)
    if app.state == "Level1":
        app.pauseButton.update(mouseX, mouseY)
        app.findButton.update(mouseX, mouseY)

def onMousePress(app, mouseX, mouseY):
    if app.startButton.hover:
        app.state = "Level1"
        app.startButton.hide()
    
    if app.findButton.hover:
        app.currLevel.finding = not app.currLevel.finding
    
    if app.pauseButton.hover:
        if app.state != "Pause":
            app.state = "Pause"
            app.pauseButton.text = "Resume"
        else:
            app.state = f"Level{app.levelNum}"
            app.pauseButton.text = "Pause"
        
    
    

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

    if len(app.currLevel.orderList) < 5 and app.state == "Level1":
        app.orderTimer -= 1
        if app.orderTimer <= 0:
            app.orderTimer = 300
            app.currLevel.generateOrder(1, 1/1000)
            
            tempList = []
            for i in range(len(app.currLevel.orderList)):
                tempList.append(app.currLevel.orderList[i].request)
    
    ## calculate chef row and col
    if app.currLevel.finding and type(app.currLevel.held) == Ingredient and app.currLevel.held.ingred in Ingredient.findable:
        findCoords = app.currLevel.ingredStationCoords()

        app.chefRow = int(app.chef.y // (app.currLevel.cellHeight))
        app.chefCol = int(app.chef.x // (app.currLevel.cellWidth))
        app.chefPos = (app.chefRow, app.chefCol)

        app.currLevel.findPath = find(app, app.chefPos, findCoords)
        
    else:
        app.currLevel.findingCell = None
        


    

    if app.state != "Pause" and app.state != "Start":
    
        app.currLevel.selectCell(app.chef.x + dx, app.chef.y + dy)
        
        app.currLevel.update()

    #iterate timer
    pass



def moves():
    return [(0,1),(1, 0),(0, -1),(-1,0)]


### using queue concept from https://geeksforgeeks.org/queue-in-python/
# and BFS algorithm from https://en.wikipedia.org/wiki/Breadth-first_search
def find(app, startCoords, endCoords):

    rows = app.dim[1]
    cols = app.dim[0]
    counterCoords = app.currLevel.counterCoords
    seen = []
    for i in range(rows):
        rowList = []
        for j in range(cols):
            rowList.append(False)
        seen.append(rowList)
    
    # each element in the queue is the cell coords followed by the path taken to get there
    queue = [((startCoords, [startCoords]))]

    while queue != []:

        # BFS searches the oldest added cell to search all cells the same distance away first
        currCoords, path = queue.pop(0)
        
        row = currCoords[0]
        col = currCoords[1]

        # set the start cell as seen
        seen[row][col] = True

        # traverse to other cells
        for move in moves():
            nRow = row + move[0]
            nCol = col + move[1]

            # return path if station is next to current cell
            if (nRow, nCol) == endCoords:
                return path
            
            # add all valid cells adjacent to current cell
            elif 0 <= nRow < rows and 0 <= nCol < cols and not seen[nRow][nCol] and (nRow, nCol) not in counterCoords:
                queue.append(((nRow, nCol), path + [(nRow, nCol)]))




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
    gap = 30
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

