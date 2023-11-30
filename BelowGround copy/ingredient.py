from cmu_graphics import *
class Ingredient:

    chopped = {
        
    }
    cooked = {
        "Tomato": "Sliced Tomato",
        "Onion": "Sliced Onion",
        "Raw Patty": "Cooked Patty"
    }

    colorbook = {
        "Sliced Tomato": "orange",
        "Sliced Onion": "pink",
        "Cooked Patty": "sienna"
    }
    
    def __init__(self, row, col, ingred, color): #replace color with image
        self.ingred = ingred
        
        self.row = row
        self.col = col

        #for MVP purposes
        self.color = color
        self.cooked = False

    def coords(self):
        return (self.row, self.col)
    
    def cook(self):
        self.cooked = True
        self.ingred = Ingredient.cooked[self.ingred]
        self.color = Ingredient.colorbook[self.ingred]
    






    
    