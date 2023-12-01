from cmu_graphics import *
from ingredient import *
from PIL import Image
class Plate:


    def __init__(self, row, col):
        self.row = row
        self.col = col
        

        #holds a list of ingredient objects
        self.contents = []
        self.finished = False
        #from https://stock.adobe.com/search?k=cartoon+plate
        self.image = Image.open('images/Plate.png')
        self.image = CMUImage(self.image.resize((80,80)))



    
    def combine(self):
        
        contentNames = []
        for ingredient in self.contents:
            contentNames.append(ingredient.ingred)
        print(sorted(contentNames))
        if sorted(["Bun", "Cooked Patty", "Sliced Lettuce", "Sliced Tomato"]) == sorted(contentNames):
            self.finished = True
            self.contents = []
            # from https://www.vectorstock.com/royalty-free-vector/hamburger-cartoon-style-isolated-vector-36428301
            burgerPNG = Image.open('images/Burger.png')
            burgerPNG = CMUImage(burgerPNG.resize((80,80)))
            self.contents.append(Ingredient(self.row, self.col, "Burger", "black", burgerPNG))
        
        if sorted(["Bun", "Sliced Lettuce", "Sliced Onion", "Sliced Tomato"]) == sorted(contentNames):
            self.finished = True
            self.contents = []
            # from https://www.istockphoto.com/illustrations/veggie-burger
            vBurger = Image.open('images/Veggie Burger.png')
            vBurger = CMUImage(vBurger.resize((70,70)))
            self.contents.append(Ingredient(self.row, self.col, "Veggie Burger", "green", vBurger))


    def stack(self, ingredient):
        self.contents.append(ingredient)
        self.combine()
        
    

    
        





    
