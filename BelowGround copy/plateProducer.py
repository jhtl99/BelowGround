from plate import *
class PlateProducer:
    def __init__(self, plate):
        self.row = plate.row
        self.col = plate.col
        

    def produce(self):
        return Plate(self.row, self.col)
