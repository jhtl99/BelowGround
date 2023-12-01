from ingredient import *

#Produces ingredients on the counter
class Producer:
    def __init__(self, ingredient):
        self.row = ingredient.row
        self.col = ingredient.col
        self.ingredient = ingredient
        self.color = ingredient.color

    
    def produce(self):
        return Ingredient(self.row, self.col, self.ingredient.ingred, self.color, self.ingredient.image)
    


    


