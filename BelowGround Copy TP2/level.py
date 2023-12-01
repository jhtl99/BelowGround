from ingredient import *
from cmu_graphics import *
from producer import *
from station import *
from plate import *
from order import *
class Level:

    #((rows, cols), [(0,0), (0,1)]... ,[('carrot', 3, 0), ('spinach', 6, 8)]... ,[('cutting', 3, 0), ('cooking', 6, 8)]... 
    #def __init__(dimensions, counterCoords, ingredCoords, stationCoords, startCoords):
       # pass
    
    # ingredient list is a dictionary; coordinate points to ingredient object
    # producerList is a dictionary; coordinate points to ingredient object
    # stationList 
    def __init__(self, dimensions, screenWidth, screenHeight, counterCoords, startCoords, ingredientList, producerList, stationList, plateList, trashCoords, windowCoords):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight * 0.6
        self.realHeight = screenHeight
        self.trashCoords = trashCoords
        self.producerList = producerList

        self.ingredientList = ingredientList

        self.orderList = []
        self.windowCoords = windowCoords
        self.counterCoords = counterCoords
        self.cellWidth = self.screenWidth/self.width
        self.cellHeight = self.screenHeight/self.height

        self.plateList = plateList
        self.startCoords = startCoords
        self.stationList = stationList

        #whether or not to look for findingCell
        self.finding = False
        self.findingCell = None
        self.findPath = []
        self.selectedCell = None
        self.held = None
        self.money = 0

    def getStartRow(self):
        return self.startCoords[0] * self.cellHeight + self.cellHeight/2
    
    def interact(self):
        cell = self.selectedCell
        ## if not holding anything
        if self.held == None:
            
            # picking up plate
            if cell in self.plateList:
                self.held = self.plateList[cell]
                self.plateList.pop(cell)

            # picking up item from producer
            elif cell in self.producerList:
                self.held = self.producerList[cell].produce()

            # picking up ingredient
            elif cell in self.ingredientList:
                self.held = self.ingredientList[cell]
                self.ingredientList.pop(cell)

                # if ingredient was cooking, reset progress
                if cell in self.stationList:
                    if self.stationList[cell].on == True:
                        self.stationList[cell].on = False
                        self.stationList[cell].progress = 0
        
        ## if holding ingredient
        elif type(self.held) == Ingredient:
            
            # cannot put ingredients into window
            if cell in self.windowCoords:
                print("Plates only!")
            
            # throw away ingredient
            elif cell == self.trashCoords:
                self.held = None

            # place ingredient onto plate
            elif cell in self.plateList:
                plate = self.plateList[cell]
                if plate.finished == True:
                    print('dish completed already')
                elif self.held.ingred in Ingredient.placable:
                    plate.stack(self.held)
                    self.held = None
                    print('stacked!')
                else:
                    print('not cooked!')

            # cannot pick up when holding ingredient
            elif cell in self.ingredientList:
                print('hands full')


            # place ingredient on counter
            elif cell in self.counterCoords and cell not in self.producerList and not cell in self.stationList:
                self.ingredientList[cell] = self.held
                self.held.row = cell[0]
                self.held.col = cell[1]
                self.held = None

            # place ingredient into station
            elif cell in self.stationList:
                station = self.stationList[cell]
                if self.held.ingred in Station.stationBook[station.stationType]:
                    station.on = True
                    self.ingredientList[cell] = self.held
                    self.held.row = cell[0]
                    self.held.col = cell[1]
                    self.held = None
                    self.finding = False
                    self.findPath = []
                else:
                    print('invalid ingredient for station')
            
            
        
        elif type(self.held) == Plate:
            if cell in self.windowCoords:
                plate = self.held
                if plate.finished:
                    # search for first instance of request, remove from order list, add money
                    for i in range(len(self.orderList)):
                        if plate.contents[0].ingred == self.orderList[i].request:
                            self.orderList.pop(i)
                            break
                    self.held.contents = []
                    self.held.finished = False
                    print('made money!')
                    self.money += 12.70
            elif cell == self.trashCoords:
                self.held.contents = []

            elif cell in self.counterCoords and cell not in self.producerList and cell not in self.ingredientList and cell not in self.plateList and cell not in self.stationList:
                self.plateList[cell] = self.held
                self.held.row = cell[0]
                self.held.col = cell[1]
                self.held = None

        '''
        #if not holding and counter has an ingredient
        elif self.held == None and self.selectedCell in self.ingredientList:
            self.held = self.ingredientList[self.selectedCell]
            self.ingredientList.pop(self.selectedCell)
            if self.selectedCell in self.stationList:
                if self.stationList[self.selectedCell].on == True:
                    self.stationList[self.selectedCell].on = False
                    self.stationList[self.selectedCell].progress = 0
        

        # placing ingredient into station
        elif self.held != None and self.selectedCell in self.stationList:
            station = self.stationList[self.selectedCell]
            if self.held.ingred in Station.stationBook[station.stationType]:
                #start cooking
                station.on = True
                self.ingredientList[self.selectedCell] = self.held
                self.held.row = self.selectedCell[0]
                self.held.col = self.selectedCell[1]
                self.held = None
                
            else:
                print('invalid')

        #putting down item
        elif self.held != None and self.selectedCell in self.counterCoords and self.selectedCell not in self.producerList and self.selectedCell not in self.ingredientList:
            self.ingredientList[self.selectedCell] = self.held
            self.held.row = self.selectedCell[0]
            self.held.col = self.selectedCell[1]
            self.held = None
        '''
    def drawInventory(self):
        drawRect(50, self.realHeight - 50, 100, 100, border = 'Black', fill = "lightgrey", align = 'center')
        if self.held == None:
            pass
        elif type(self.held) == Ingredient:
            drawImage(self.held.image, 50, self.realHeight - 50, align = 'center')
        elif type(self.held) == Plate:
            drawImage(self.held.image, 50, self.realHeight - 50, align = 'center')
            for i in range(len(self.held.contents)):
                drawRect(150 + i*100, self.realHeight-50, 100, 100, border = 'Black', fill = None, align = 'center')
                drawImage(self.held.contents[i].image, 150+i*100, self.realHeight-50, align = 'center')

    def generateOrder(self, levelNum, rate):
        if levelNum == 1:
            self.orderList.append(Order(rate,1))
        if levelNum == 2:
            pass
    
    # returns coords of the station that the held ingredient needs to go to
    def ingredStationCoords(self):
        if type(self.held) == Ingredient and self.held.cooked != True:
            ingredName = self.held.ingred
            #station name
            for name in Station.stationBook:
                if ingredName in Station.stationBook[name]:
                    stationName = name
            for coords in self.stationList:
                if self.stationList[coords].stationType == stationName:
                    self.findingCell = coords
                    return coords
            return None
        else:
            self.findingCell = None

    def drawOrders(self):
        for i in range(len(self.orderList)):
            drawRect(self.screenWidth - 50 - i*100, self.realHeight-50, 100, 100, border = 'Black', fill = None, align = 'center')
            drawImage(self.orderList[i].image, self.screenWidth - 50 - i*100, self.realHeight-50, align = 'center')

    def getStartCol(self):
        return self.startCoords[1] * self.cellWidth + self.cellWidth /2
    
    def drawLevel(self):
        
        '''
        if self.held == None:
            drawLabel(f"Currently Holding nothing", 100, 550)
        elif type(self.held) == Ingredient:
            drawLabel(f"Currently Holding: {self.held.ingred}", 100, 550)
        elif type(self.held) == Plate:
            drawLabel(f"Currently Holding: {self.held.contents}", 100, 550)
        '''

        #draws floor grid
        for row in range(self.height):
            for col in range(self.width):
                drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, self.cellHeight, fill = 'snow', border = 'gray', borderWidth = 1)

        #draws counter
        for (row, col) in self.counterCoords:
            drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, self.cellHeight, fill = 'peru', border = 'darkSlateGray')

        #draws producers and icon
        for (row,col) in self.producerList:
            color = self.producerList[(row,col)].color
            drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, 
                             self.cellHeight, fill = 'yellow', border = color, borderWidth = 4)
            drawCircle(col*self.cellWidth + self.cellWidth / 2, row * self.cellHeight + self.cellHeight/2, 10, fill = color)
        
        #draws stations including progress
        for (row, col) in self.stationList:
            station = self.stationList[(row,col)]
            color = station.color
            drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, 
                             self.cellHeight, fill = 'lightblue', border = color, borderWidth = 4)
            if station.on:
                drawRect(col*self.cellWidth, row*self.cellHeight, max(1, self.cellWidth*station.progress), self.cellHeight, fill = 'green')
        #draw trashbin
        drawRect(self.trashCoords[1]*self.cellWidth, self.trashCoords[0]*self.cellHeight, self.cellWidth, 
                             self.cellHeight, fill = 'black', border = "gray", borderWidth = 4)
        
        #draw window
        for (row, col) in self.windowCoords:
            drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, 
                             self.cellHeight, fill = 'green', border = "gray", borderWidth = 4)
        #draw plates
        for (row, col) in self.plateList:
            plate = self.plateList[(row,col)]
            drawImage(plate.image, col*self.cellWidth + self.cellWidth / 2, row * self.cellHeight + self.cellHeight/2, align = 'center')
            for ingredient in plate.contents:
                drawImage(ingredient.image, col*self.cellWidth + self.cellWidth / 2, row * self.cellHeight + self.cellHeight/2, align = 'center')
            
            #drawCircle(col*self.cellWidth + self.cellWidth / 2, row * self.cellHeight + self.cellHeight/2, 20, fill = "white")

        #draws selected cell
        if self.selectedCell != None:
            drawRect(self.selectedCell[1]*self.cellWidth, self.selectedCell[0]*self.cellHeight, self.cellWidth, self.cellHeight, fill = None, border = 'lightGreen', borderWidth = 3)

        # draw finding cell
        if self.finding and self.findingCell != None:
            drawRect(self.findingCell[1]*self.cellWidth, self.findingCell[0]*self.cellHeight, self.cellWidth, self.cellHeight, fill = None, border = 'cyan', borderWidth = 3)

        for (row, col) in self.findPath:
            drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, self.cellHeight, fill = None, border = 'green', borderWidth = 3)

        #draws visible ingredients, i represents ingredient object
        for i in list(self.ingredientList.values()):

            drawImage(i.image, i.col*self.cellWidth + self.cellWidth/2, i.row*self.cellHeight + self.cellHeight/2, align = 'center')
            
            #drawCircle(ingred.col*self.cellWidth + self.cellWidth / 2, ingred.row*self.cellHeight + self.cellHeight/2, 10, fill = ingred.color)
        

        #how the level was previously drawn, for reference only
        '''
        for row in range(self.height):
            for col in range(self.width):
                
                if (row, col) in self.counterCoords:
                    drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, self.cellHeight, fill = 'brown', border = 'grey')
                else:
                    drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, self.cellHeight, fill = None, border = 'black', borderWidth = 1)
                
                if (row, col) in self.producerList:
                    color = self.producerList[(row,col)].color
                    drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, 
                             self.cellHeight, fill = 'yellow', border = color, borderWidth = 4)
                    drawCircle(col*self.cellWidth + self.cellWidth / 2, row * self.cellHeight + self.cellHeight/2, 10, fill = color)
                    
                if (row, col) == self.selectedCell:
                    drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, self.cellHeight, fill = None, border = 'lightGreen', borderWidth = 3)
        '''
        
    def update(self):
        for station in list(self.stationList.values()):
            if station.on:
                if station.selfCook or (self.selectedCell == (station.row, station.col) and self.held == None):
                    station.incProgress()
                    if station.progress >1:
                        row, col = station.row, station.col
                        ingredient = self.ingredientList[(row,col)]
                        ingredient.cook()
                        station.on = False
                        station.progress = 0
        



        


    
    #update which cell the chef is looking at
    def selectCell(self, x, y):
        selectedRow = int(y // self.cellHeight)
        selectedCol = int(x // self.cellWidth)
        
        self.selectedCell = (selectedRow, selectedCol)
    
    
    '''
    def findShortestPath(self, targetRow, targetCol):
        startRow = self.selectedCell[0]
        startCol = self.selectedCell[1]
        path = pathHelper(startRow, startCol, targetRow, targetCol, [])
        for cellRow, cellCol in path:
            drawRect(cellCol*self.cellWidth, cellRow*self.cellHeight, self.cellWidth, self.cellHeight, fill = 'green')
    
    def pathHelper(self, currRow, currCol, targetRow, targetCol, currPath):
        if currRow == targetRow and currCol == targetCol:
            return currPath
    '''

        
    
    
