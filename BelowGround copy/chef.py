from cmu_graphics import *

class Chef:

    def __init__(self, startX, startY):
        
        self.x = startX
        self.y = startY
        self.direction = "down"
        self.lookx = None
        self.looky = None
        

        # for demo
        self.r = 20
    
    
    def draw(self):
        drawImage
        
        drawCircle(self.x, self.y, self.r, fill = "White", border = 'blue')
        
        if self.direction == "down":
            drawLine(self.x, self.y, self.x, self.y+self.r)
        if self.direction == "up":
            drawLine(self.x, self.y, self.x, self.y-self.r)
        if self.direction == "right":
            drawLine(self.x, self.y, self.x+self.r, self.y)
        if self.direction == "left":
            drawLine(self.x, self.y, self.x-self.r, self.y)
        
        



    