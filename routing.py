from z3 import *

class Point:
    def __init__(self, x = None, y = None, occupied = None):
        self.x = x
        self.y = y
        self.occupied = occupied
        
    def changeBoolOccupied(self, newBoolValue):
        self.occupied = newBoolValue
        
    
        

