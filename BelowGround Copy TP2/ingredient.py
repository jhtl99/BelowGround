from cmu_graphics import *
from PIL import Image
class Ingredient:

    findable = {
        "Tomato",
        "Onion",
        "Lettuce",
        "Raw Patty",
        "Raw Chicken"
    }

    placable = {
        "Sliced Tomato",
        "Sliced Onion",
        "Sliced Lettuce",
        "Cooked Patty",
        "Bun"
    }
    cooked = {
        "Tomato": "Sliced Tomato",
        "Onion": "Sliced Onion",
        "Raw Patty": "Cooked Patty",
        "Lettuce": "Sliced Lettuce"
    }

    imageBook = {
        "Sliced Tomato": "images/Sliced Tomato.png",
        #from https://www.istockphoto.com/vector/tomato-slice-on-white-background-gm1166388616-321291776
        "Sliced Onion": "images/Sliced Onion.png",
        #from https://www.vecteezy.com/vector-art/7938448-simple-vector-image-of-sliced-onion
        "Sliced Lettuce": "images/Sliced Lettuce.png",
        #from https://www.shutterstock.com/image-vector/bright-vector-illustration-colorful-lettuce-cartoon-1236183613
        "Cooked Patty": "images/Cooked Patty.png"
        #from https://www.vectorstock.com/royalty-free-vector/beef-patty-ingredient-for-burger-flat-cartoon-vector-34194950
        
    }
    
    def __init__(self, row, col, ingred, color, image): 
        self.ingred = ingred
        
        self.row = row
        self.col = col
        
        self.image = image

        self.cooked = False
        #for producer purposes
        self.color = color
        

    def coords(self):
        return (self.row, self.col)
    
    def cook(self):
        self.cooked = True
        self.ingred = Ingredient.cooked[self.ingred]

        tempPng = Image.open(Ingredient.imageBook[self.ingred])

        self.image = CMUImage(tempPng.resize((70,70)))

       
    
    






    
    