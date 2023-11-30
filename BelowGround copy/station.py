class Station:

    stationBook = {
        "Chop" : {"Tomato", "Onion"},
        "Grill": {"Raw Patty","Raw Chicken"}
    }
    def __init__(self, row, col, stationType, color, rate, selfCook):
        self.row = row
        self.col = col

        #progress ranges from 0 to 1
        self.progress = 0
        self.rate = rate
        self.selfCook = selfCook
        self.on = False
        
        self.color = color

        #stations include Grill, Chop, Window(to send food out)
        self.stationType = stationType
    
    def incProgress(self):
        self.progress += self.rate
    
    
    


