from cmu_graphics import *
from random import randint
from PIL import Image
class Order:

    orders1 = ["Burger", "Veggie Burger"]
    orders2 = ["Burger", "Veggie Burger", "Fries"]

    def __init__(self, rate, levelNum):
        self.patience = 1
        self.rate = rate
        
        if levelNum == 1:
            self.request = Order.orders1[randint(0, len(Order.orders1)-1)]
            self.image = Image.open(f"images/{self.request}.png")
            self.image = CMUImage(self.image.resize((80,80)))
    
    
    def decPatience(self):
        self.patience -= self.rate
    
    

    
    



    

