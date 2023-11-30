from ingredient import *
from cmu_graphics import *
from producer import *
from station import *
class Level:

    #((rows, cols), [(0,0), (0,1)]... ,[('carrot', 3, 0), ('spinach', 6, 8)]... ,[('cutting', 3, 0), ('cooking', 6, 8)]... 
    #def __init__(dimensions, counterCoords, ingredCoords, stationCoords, startCoords):
       # pass
    
    # ingredient list is a dictionary; coordinate points to ingredient object
    # producerList is a dictionary; coordinate points to ingredient object
    # stationList 
    def __init__(self, dimensions, screenWidth, screenHeight, counterCoords, startCoords, ingredientList, producerList, stationList, plateList):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight * 0.8

        self.producerList = producerList
        '''
        tomato = Ingredient(0,3, "Tomato", "red")
        tempProducer = Producer(tomato)
        self.producerList = {(tomato.row, tomato.col): tempProducer}
        '''
        self.ingredientList = ingredientList

        self.counterCoords = counterCoords
        self.cellWidth = self.screenWidth/self.width
        self.cellHeight = self.screenHeight/self.height

        self.plateList = plateList
        self.startCoords = startCoords
        self.stationList = stationList

        self.selectedCell = None
        self.ingredHeld = None

    def getStartRow(self):
        return self.startCoords[0] * self.cellHeight + self.cellHeight/2
    
    def interact(self):

        

        #if not holding and selecting a producer
        if self.ingredHeld == None and self.selectedCell in self.producerList:
            self.ingredHeld = self.producerList[self.selectedCell].produce()

        #if not holding and counter has an ingredient
        elif self.ingredHeld == None and self.selectedCell in self.ingredientList:
            self.ingredHeld = self.ingredientList[self.selectedCell]
            self.ingredientList.pop(self.selectedCell)
            if self.selectedCell in self.stationList:
                if self.stationList[self.selectedCell].on == True:
                    self.stationList[self.selectedCell].on = False
                    self.stationList[self.selectedCell].progress = 0

        # placing ingredient into station
        elif self.ingredHeld != None and self.selectedCell in self.stationList:
            station = self.stationList[self.selectedCell]
            if self.ingredHeld.ingred in Station.stationBook[station.stationType]:
                #start cooking
                station.on = True
                self.ingredientList[self.selectedCell] = self.ingredHeld
                self.ingredHeld.row = self.selectedCell[0]
                self.ingredHeld.col = self.selectedCell[1]
                self.ingredHeld = None
                
            else:
                print('invalid')

        #putting down item
        elif self.ingredHeld != None and self.selectedCell in self.counterCoords and self.selectedCell not in self.producerList and self.selectedCell not in self.ingredientList:
            self.ingredientList[self.selectedCell] = self.ingredHeld
            self.ingredHeld.row = self.selectedCell[0]
            self.ingredHeld.col = self.selectedCell[1]
            self.ingredHeld = None
        


    def getStartCol(self):
        return self.startCoords[1] * self.cellWidth + self.cellWidth /2
    
    def drawLevel(self):
        
        if self.ingredHeld == None:
            drawLabel(f"Currently Holding nothing", 100, 550)
        else:
            drawLabel(f"Currently Holding: {self.ingredHeld.ingred}", 100, 550)
        
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

        for (row, col) in self.plateList:
            drawCircle(col*self.cellWidth + self.cellWidth / 2, row * self.cellHeight + self.cellHeight/2, 20, fill = "white")

        #draws selected cell
        if self.selectedCell != None:
            drawRect(self.selectedCell[1]*self.cellWidth, self.selectedCell[0]*self.cellHeight, self.cellWidth, self.cellHeight, fill = None, border = 'lightGreen', borderWidth = 3)

        #draws visible ingredients
        for ingred in list(self.ingredientList.values()):

            drawCircle(ingred.col*self.cellWidth + self.cellWidth / 2, ingred.row*self.cellHeight + self.cellHeight/2, 10, fill = ingred.color)
        

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
        
    def updateCooking(self):
        for station in list(self.stationList.values()):
            if station.on:
                if station.selfCook or self.selectedCell == (station.row, station.col):
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

        
    
    
