from z3 import *
from math import floor

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
    
   
    def occupy_points(self, listOfPoints, value=1):
        for point in listOfPoints:
            self.occupy_one_point(point[0],point[1], value)
   
    def occupy_one_point(self, x, y, value=1):
        
        self.grid[x][y] = value
        
        
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

def POLYfill(grPOLY, pcirc, ncirc):
    #if len(pcirc)!=len(ncirc):
    #    print('Erro estranho kkk')
    #    return
    
    for idx in range(len(ncirc)):
        points = []
        if ncirc[idx].gate == pcirc[idx].gate and ncirc[idx].gate != 0 and pcirc[idx].gate != 0:
            for y in range(P_REGION+N_REGION+MID_REGION):
                points.append([(ncirc[idx].position*2)+2, y+VDD_REGION])
        else:
            if ncirc[idx].gate != 0:
                for y in range(N_REGION):
                    points.append([(ncirc[idx].position*2)+2, y+VDD_REGION+P_REGION+MID_REGION])
            if pcirc[idx].gate != 0:
                for y in range(P_REGION):
                    points.append([(pcirc[idx].position*2)+2, y+VDD_REGION])
            
        grPOLY.occupy_points(points)
        
            
    #grPOLY.print()
    
    

def RXfill(grRX, pcirc, ncirc):
    
    #if len(pcirc)!=len(ncirc):
    #    print('Erro estranho kkk')
    #    return

    idx_p_max = 0
    idx_n_max = 0
    
    for idx in range(len(pcirc)):
        points = []  
        
        idx_p_max = len(pcirc)-1
        idx_n_max = len(pcirc)-1
        
        if pcirc[idx].source != 0 and pcirc[idx].drain != 0:
            #ocupa 2*idx+1 e 2*idx+2 para toda p_region
            for x in range(1,3):
                for y in range(P_REGION):
                    points.append([(pcirc[idx].position*2)+x, y+VDD_REGION])
            grRX.occupy_points(points)
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
            grRX.occupy_points(points)
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
    
    #grRX.print()
    
def CAfill(grCA, ppos, npos):
    
    points = []
    yp = floor(P_REGION/2)
    yn = floor(N_REGION/2)
    
    for idp, pmos in enumerate(ppos):
        if pmos != 0:
            points.append([(idp*2)+1, yp+VDD_REGION])
            grCA.occupy_one_point((idp*2)+1, yp+VDD_REGION, pmos)
            
    for idn, nmos in enumerate(npos):
        if nmos != 0:
            points.append([(idn*2)+1, yn+MID_REGION+P_REGION+VDD_REGION])
            grCA.occupy_one_point((idn*2)+1, yn+MID_REGION+P_REGION+VDD_REGION, nmos)
        
    
    grCA.print()

def createGridTransistors(layers, col, row, pcirc, ncirc, ppos, npos):
    
    grRX = Grid(layers[0], col, row)
    grCA = Grid(layers[1], col, row)
    grPoly = Grid(layers[2], col, row)
     
    RXfill(grRX, pcirc, ncirc)
    POLYfill(grPoly, pcirc, ncirc)
    CAfill(grCA, ppos, npos)
    
    
    
    return grRX, grCA, grPoly
