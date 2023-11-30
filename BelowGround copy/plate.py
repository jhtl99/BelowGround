from cmu_graphics import *
class Plate:


    def __init__(self, row, col):
        self.row = row
        self.col = col

        #holds a list of ingredient objects
        self.contents = []
        self.finished = False

        
    

    def add(self, ingredient):
        self.contents.add(ingredient.ingred)
        self.contents.sort()
        print(self.contents)
        combine(self)
        
    

    def combine(self):
        
        contentNames = []
        for ingredient in self.contents:
            contentNames.append(ingredient.ingred)
        if ["Buns", "Cooked Patty", "Sliced Lettuce", "Sliced Onion", "Sliced Tomato"].sort() == self.contentNames.sort():
            self.finished = True
        





    
