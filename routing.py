from z3 import *

N_REGION = 3
P_REGION = 3
MID_REGION = 5
GND_REGION = 2
VDD_REGION = 2
SIDE_REGION = 1

class Grid:
    def __init__(self, layer, x, y):
        self.layer = layer
        grid = []
        self.x_size = x
        self.y_size = y

        for _ in range(x):
            bandwith = []
            for _ in range(y):
                bandwith.append(0)
            grid.append(bandwith)
        
        self.grid = grid
        
    def increase_x(self, increase_in):
        
        for _ in range(increase_in):
            bandwith = []
            for _ in range(self.y_size):
                bandwith.append(0) 
            self.grid.append(bandwith)
    
   
    def occupy_points(self, listOfPoints):
        for point in listOfPoints:
            self.occupy_one_point(point[0],point[1])


   
    def occupy_one_point(self, x, y):
        
        self.grid[x][y] = 1
        


    def print(self):
        print('Layer:', self.layer)
        for idx in range(self.y_size):
            for row in self.grid:
                print(row[idx] , end=', ')
            print()
        
        return



def estimateGrid(listPCirc, listNCirc):

    max_p_w = 3
    max_n_w = 3
    mid_region = 5
    gnd_y, vdd_y = 2, 2
    
    min_bandwidth = N_REGION + P_REGION + MID_REGION + VDD_REGION + GND_REGION          #constante
    bandw = max_p_w + max_n_w + mid_region + gnd_y + vdd_y                              #variável
    

    if len(listPCirc)!=len(listNCirc):
        print('Erro estranho kkk')
        return

    count_col = (len(listPCirc)*2) + 3
    count_row = bandw if bandw >= min_bandwidth else min_bandwidth
    
    

    return count_col, count_row



def RXfill(grRX, pcirc, ncirc):
    
    if len(pcirc)!=len(ncirc):
        print('Erro estranho kkk')
        return
    p_max_pos = 0
    n_max_pos = 0
    idx_p_max = 0
    idx_n_max = 0
    
    for idx in range(len(pcirc)):
        points = []  
        
        if pcirc[idx].position == len(pcirc)-1:
            idx_p_max = idx
            
        if ncirc[idx].position == len(ncirc)-1:
            idx_n_max = idx
        
        print(p_max_pos, n_max_pos)
        
        if pcirc[idx].source != 0 and pcirc[idx].drain != 0:
            #ocupa 2*idx+1 e 2*idx+2 para toda p_region
            for x in range(1,3):
                for y in range(P_REGION):
                    points.append([(pcirc[idx].position*2)+x, y+VDD_REGION])
                    pass
            grRX.occupy_points(points)
            pass
        else:
            if grRX.grid[pcirc[idx].position*2][VDD_REGION] != 0:
                for y in range(P_REGION):
                    points.append([(pcirc[idx].position*2)+1, y+VDD_REGION])
                grRX.occupy_points(points)
           
             
        if ncirc[idx].source != 0 and ncirc[idx].drain != 0:
            #ocupa 2*idx+1 e 2*idx+2 para toda n_region
            for x in range(1,3):
                for y in range(N_REGION):
                    points.append([(ncirc[idx].position*2)+x, y+MID_REGION+P_REGION+VDD_REGION])
                    pass
            grRX.occupy_points(points)
            pass
        else:
            if grRX.grid[ncirc[idx].position*2][MID_REGION+P_REGION+VDD_REGION] != 0:
                for y in range(N_REGION):
                    points.append([(ncirc[idx].position*2)+1, y+MID_REGION+P_REGION+VDD_REGION])
                grRX.occupy_points(points)
    
   
    
    if pcirc[idx_p_max].source != 0 and pcirc[idx_p_max].drain != 0:
        points = []
        for y in range(P_REGION):
            points.append([(pcirc[idx_p_max].position*2)+3, y+VDD_REGION])
        grRX.occupy_points(points)
             
    if ncirc[idx_n_max].source != 0 and ncirc[idx_n_max].drain != 0:
        points = []
        for y in range(N_REGION):
            points.append([(ncirc[idx_n_max].position*2)+3, y+MID_REGION+P_REGION+VDD_REGION])
        grRX.occupy_points(points)
    
    grRX.print()
    
    pass


def createGridTransistors(layerRX, layerCA, layerPoly, col, row, pcirc, ncirc):
    
    grRX = Grid(layerRX, col, row)
    grCA = Grid(layerCA, col, row)
    grPoly = Grid(layerPoly, col, row)
     
    RXfill(grRX, pcirc, ncirc)
    
    return grRX, grCA, grPoly
