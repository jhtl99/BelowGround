from ingredient import *
class Counter:

    def __init__(self, row, col, item):
        self.row = row
        self.col = col

        #if blank counter, item = None
        #otherwise, pickup food from counter
        self.item = item
    
#Produces ingredients on top of the counter if there are none
class Producer:
    def __init__(self, row, col, ingredient, color):
        self.row = row
        self.col = col
        self.ingredient = ingredient
        self.color = color
        self.empty = True
    
    def produce(self):
        newIngred = Ingredient(self.row, self.col, self.ingredient, self.color)

