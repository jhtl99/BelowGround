from ingredient import *
from cmu_graphics import *
class Level:

    #((rows, cols), [(0,0), (0,1)]... ,[('carrot', 3, 0), ('spinach', 6, 8)]... ,[('cutting', 3, 0), ('cooking', 6, 8)]... 
    #def __init__(dimensions, counterCoords, ingredCoords, stationCoords, startCoords):
       # pass
    
    # ingredient list is a dictionary; coordinate points to ingredient
        
    def __init__(self, dimensions, screenWidth, screenHeight, counterCoords, startCoords):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight * 0.8

        #self.producerList = producerList
        tempIngredient = Ingredient(1, 0, "Tomato", "red")
        self.ingredientList = {(tempIngredient.row, tempIngredient.col): tempIngredient}

        self.counterCoords = counterCoords
        self.cellWidth = self.screenWidth/self.width
        self.cellHeight = self.screenHeight/self.height

        self.startCoords = startCoords

        self.selectedCell = None
        self.ingredHeld = None

    def getStartRow(self):
        return self.startCoords[0] * self.cellHeight + self.cellHeight/2
    
    def interact(self):
        if self.ingredHeld == None and self.selectedCell in self.ingredientList:
            self.ingredHeld = self.ingredientList[self.selectedCell]
            self.ingredientList.pop(self.selectedCell)
            print(self.ingredHeld.ingred)

        elif self.ingredHeld != None and self.selectedCell in self.counterCoords:
            self.ingredHeld = None

    def getStartCol(self):
        return self.startCoords[1] * self.cellWidth + self.cellWidth /2
    def drawLevel(self):

        drawLabel(f"Currently Holding: {self.ingredHeld.ingred}", 50, 550)
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) == self.selectedCell:
                    drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, self.cellHeight, fill = 'green')
                elif (row, col) in self.counterCoords:
                    drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, self.cellHeight, fill = 'brown', border = 'grey')
                else:
                    drawRect(col*self.cellWidth, row*self.cellHeight, self.cellWidth, self.cellHeight, fill = None, border = 'black', borderWidth = 1)
        
        for ingred in list(self.ingredientList.values()):
            drawCircle(ingred.col*self.cellWidth + self.cellWidth / 2, ingred.row*self.cellHeight + self.cellHeight/2, 10, fill = ingred.color)
        
        for counterx, countery in self.counterCoords:
            #fix logic here to reduce boolean checks above
            pass
    
    def updateLevel(self):
        pass
    
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

        
    
    
