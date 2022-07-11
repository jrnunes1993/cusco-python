from z3 import *


class Grid:
    def __init__(self, layer, x, y):
        self.layer = layer
        grid = []
        self.x_size = x
        self.y_size = y

        for _ in range(x):
            bandwith = []
            for _ in range(y):
                bandwith.append(False)
            grid.append(bandwith)
        
        self.grid = grid
        
    def increase_x(self, increase_in):
        
        for _ in range(increase_in):
            bandwith = []
            for _ in range(self.y_size):
                bandwith.append(False) 
            self.grid.append(bandwith)
    
   
    def occupy_points(self, listOfPoints):
        for point in listOfPoints:
            self.occupy_one_point(point[0],point[1])

   
    def occupy_one_point(self, x, y):
        
        self.grid[x][y] = True
        


    def print(self):
        print('Layer:', self.layer)
        for idx in range(self.y_size):
            for row in self.grid:
                print(int(row[idx]) , end=', ')
            print()
        
        return



def estimateGrid(listPCirc, listNCirc):

    max_p_w = 3
    max_n_w = 3
    mid_region = 5
    gnd_y, vdd_y = 2, 2
    
    min_bandwidth = 15
    bandw = max_p_w + max_n_w + mid_region + gnd_y + vdd_y
    

    if len(listPCirc)!=len(listNCirc):
        print('Erro estranho kkk')
        return

    count_col = (len(listPCirc)*2) + 3
    count_row = bandw if bandw >= min_bandwidth else min_bandwidth
    
    

    return count_col, count_row


def createGrid(layer, col, row):
    gr = Grid(layer, col, row)
    
    return gr


def createGridTransistors(layerRX, layerCA, layerPoly, col, row, pcirc, ncirc):
    
    grRX = createGrid(layerRX, col, row)
    grCA = createGrid(layerCA, col, row)
    grPoly = createGrid(layerPoly, col, row)
    
    for ptrans in pcirc:
        if ptrans.source != 0 and ptrans.drain != 0 and ptrans.gate != 0:
            pass
    
    
    return
