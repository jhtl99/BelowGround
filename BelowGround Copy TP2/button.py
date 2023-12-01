from cmu_graphics import *
class Button:

    def __init__(self, x, y, width, height, text, color, hoverColor, visible):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hoverColor = hoverColor
        self.hover = False
        self.visible = visible

    def update(self, mouseX, mouseY):
        self.hover = self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height
        
    def hide(self):
        self.visible = False
        self.hover = False
    
    def show(self):
        self.visible = True

    def draw(self):
        if not self.hover:
            drawRect(self.x, self.y, self.width, self.height, fill = self.color)
            drawLabel(self.text, self.x + self.width/2, self.y + self.height/2)
        else:
            drawRect(self.x, self.y, self.width, self.height, fill = self.color, border = self.hoverColor)
            drawLabel(self.text, self.x + self.width/2, self.y + self.height/2)

    

