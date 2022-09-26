from multiprocessing import connection
from numpy import int0
from z3 import *
from math import floor

N_REGION = 3
P_REGION = 3
MID_REGION = 10
GND_REGION = 4
VDD_REGION = 4


class Pin:
    def __init__(self, x: int, y: int, con_num = None, net = None):
        self.con_num = con_num
        self.net = net
        self.x = x
        self.y = y

    def __str__(self):
        return (f"({self.x}, {self.y})")

class Connection:
    def __init__(self, number: int, pin1: Pin, pin2: Pin):
        self.number = number
        self.pin1 = pin1
        self.pin2 = pin2

    def __str__(self):
        return (f"Con: {self.number} | Start Pin: {self.pin1} End Pin: {self.pin2}")


class Net:
    def __init__(self, net_number: int, connections: list):
        self.net_number = net_number
        self.connections = connections
    
    def __str__(self):
        txt = "Net {}\n".format(self.net_number)
        for con in self.connections:
            txt += f"\t {con}\n"

        return txt
    
    def getNumOfConnections(self):
        return len(self.connections)
            

class Grid:
    def __init__(self, layer, x: int, y: int):
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
    mid_region = 10
    gnd_y, vdd_y = 2, 2
    
    min_bandwidth = N_REGION + P_REGION + MID_REGION + VDD_REGION + GND_REGION          #constante
    bandw = max_p_w + max_n_w + mid_region + gnd_y + vdd_y                              #variável
    

    if len(listPCirc)!=len(listNCirc):
        print('Erro estranho kkk')
        return

    count_col = (len(listPCirc)*4) + 5
    count_row = bandw if bandw >= min_bandwidth else min_bandwidth
    
    
    return count_col, count_row

def POLYfill(grPOLY, pcirc, ncirc, grCA):
    #if len(pcirc)!=len(ncirc):
    #    print('Erro estranho kkk')
    #    return
    
    for idx in range(len(ncirc)):
        points = []
        if ncirc[idx].gate == pcirc[idx].gate and ncirc[idx].gate != 0 and pcirc[idx].gate != 0:
            for y in range(P_REGION+N_REGION+MID_REGION):
                points.append([(ncirc[idx].position*4)+4, y+VDD_REGION])
            grPOLY.occupy_points(points, ncirc[idx].gate) 
            grCA.occupy_one_point((ncirc[idx].position*4)+4, floor((P_REGION+N_REGION+MID_REGION+VDD_REGION)/2)+1, ncirc[idx].gate)
        else:
            if ncirc[idx].gate != 0:
                for y in range(N_REGION+2):
                    points.append([(ncirc[idx].position*4)+4, y+VDD_REGION+P_REGION+MID_REGION-2])
                grPOLY.occupy_points(points, ncirc[idx].gate)
                grCA.occupy_one_point((ncirc[idx].position*4)+4, VDD_REGION+P_REGION+MID_REGION-2, ncirc[idx].gate)
                points = []
            if pcirc[idx].gate != 0:
                for y in range(P_REGION+2):
                    points.append([(pcirc[idx].position*4)+4, y+VDD_REGION])
                grPOLY.occupy_points(points, pcirc[idx].gate)
                grCA.occupy_one_point((pcirc[idx].position*4)+4, VDD_REGION+P_REGION+1, pcirc[idx].gate)
        
                 
    grPOLY.print()
    
    

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
            for x in range(1,5):
                for y in range(P_REGION):
                    points.append([(pcirc[idx].position*4)+x, y+VDD_REGION])
            grRX.occupy_points(points)
        else:
            if grRX.grid[pcirc[idx].position*4][VDD_REGION] != 0:
                for x in range(1,4):
                    for y in range(P_REGION):
                        points.append([(pcirc[idx].position*4)+x, y+VDD_REGION])
                    grRX.occupy_points(points)
            
             
        if ncirc[idx].source != 0 and ncirc[idx].drain != 0:
            #ocupa 2*idx+1 e 2*idx+2 para toda n_region
            for x in range(1,5):
                for y in range(N_REGION):
                    points.append([(ncirc[idx].position*4)+x, y+MID_REGION+P_REGION+VDD_REGION])
            grRX.occupy_points(points)
        else:
            if grRX.grid[ncirc[idx].position*4][MID_REGION+P_REGION+VDD_REGION] != 0:
                for x in range(1,4):
                    for y in range(N_REGION):
                        points.append([(ncirc[idx].position*4)+x, y+MID_REGION+P_REGION+VDD_REGION])
                    grRX.occupy_points(points)
    
   
    
    if pcirc[idx_p_max].source != 0 and pcirc[idx_p_max].drain != 0:
        points = []
        for x in range(5,8):
            for y in range(P_REGION):
                points.append([(pcirc[idx_p_max].position*4)+x, y+VDD_REGION])
            grRX.occupy_points(points)
             
    if ncirc[idx_n_max].source != 0 and ncirc[idx_n_max].drain != 0:
        points = []
        for x in range(5,8):    
            for y in range(N_REGION):
                points.append([(ncirc[idx_n_max].position*4)+x, y+MID_REGION+P_REGION+VDD_REGION])
            grRX.occupy_points(points)
        
    grRX.print()
    
def CAfill(grCA, ppos, npos):
    
    yp = floor(P_REGION/2)
    yn = floor(N_REGION/2)
    
    for idp, pmos in enumerate(ppos):
        if pmos != 0:
            grCA.occupy_one_point((idp*4)+2, yp+VDD_REGION, pmos)
            
    for idn, nmos in enumerate(npos):
        if nmos != 0:
            grCA.occupy_one_point((idn*4)+2, yn+MID_REGION+P_REGION+VDD_REGION, nmos)
            
    # for idx in range(math.ceil(grCA.x_size/2)-1):
    #     grCA.occupy_one_point((idx*2)+1, 0, 2)
    #     grCA.occupy_one_point((idx*2)+1, N_REGION + P_REGION + MID_REGION + VDD_REGION + GND_REGION-1, 1)
        
    grCA.occupy_one_point(floor(grCA.x_size/2), 1, 2)
    grCA.occupy_one_point(floor(grCA.x_size/2), N_REGION + P_REGION + MID_REGION + VDD_REGION + GND_REGION-2, 1)
    
    grCA.print()

def createGridTransistors(layers, col, row, pcirc, ncirc, ppos, npos):
    
    grRX = Grid(layers[0], col, row)
    grCA = Grid(layers[1], col, row)
    grPoly = Grid(layers[2], col, row)
     
    RXfill(grRX, pcirc, ncirc)
    POLYfill(grPoly, pcirc, ncirc, grCA)
    CAfill(grCA, ppos, npos)
    
    
    
    return grRX, grCA, grPoly


def defineNets(grCA):
    pinlist = {}
    netlist = []
    
    for idx_x in range(grCA.x_size):
        for idx_y in range(grCA.y_size):
            if grCA.grid[idx_x][idx_y] != 0:
                if grCA.grid[idx_x][idx_y] in pinlist.keys():
                    pinlist[grCA.grid[idx_x][idx_y]].append([idx_x, idx_y])
                else:
                    pinlist[grCA.grid[idx_x][idx_y]] = [[idx_x, idx_y]]

    netsToBeRemoved = []

    for key in pinlist.keys():
        if len(pinlist[key]) < 2:
            if pinlist[key][0][1] > MID_REGION+P_REGION+VDD_REGION or pinlist[key][0][1] < P_REGION+VDD_REGION:
                print(key)
                grCA.grid[pinlist[key][0][0]][pinlist[key][0][1]] = 0
                netsToBeRemoved.append(key)

    for rm in netsToBeRemoved:
        pinlist.pop(rm)

    aux_cons = []
    con_count = 0

    for n in pinlist:
        for idx, ps in enumerate(pinlist[n]):
            for i in range(idx+1, len(pinlist[n])):
                aux_cons.append(Connection(con_count, Pin(ps[0], ps[1], con_count, n), Pin(pinlist[n][i][0], pinlist[n][i][1], con_count, n)))
                con_count = con_count + 1

        con_count = 0
        netlist.append(Net(n, aux_cons))
        aux_cons = []
    
    for n in netlist:
        print(n)
    
    print(pinlist)
    return netlist, pinlist


def route(metalLayers, nets, pins, grid_x, grid_y):
    
    s = Solver()
    
    num_metal = len(metalLayers)
    metal_grid_3d = [[[Int("s_%i_%i_%i" % (j,i,k)) for j in range (grid_x)] for i in range(grid_y)] for k in range(num_metal)]
    #print(metal_grid_3d)
    
    # for net in nets:
    #     print(net, nets[net])
    #     for point in nets[net]:
    #         print(point[0], point[1])
    #         s.add(metal_grid_3d[0][point[1]][point[0]] == net)
        
    net_number = [Int("net_%i" % (n.net_number)) for n in nets]
    
    cons_number = sum(int(n.getNumOfConnections()) for n in nets) 
    
    for z in range(num_metal):
        for x in range(grid_x):
            s.add(metal_grid_3d[z][0][x] == 0)
            s.add(metal_grid_3d[z][grid_y-1][x] == 0)
        for y in range(grid_y):
            s.add(metal_grid_3d[z][y][0] == 0)
            s.add(metal_grid_3d[z][y][grid_x-1] == 0)
        
    
    print(cons_number)   
    
    for n in net_number:
        print(n)     
        
    for p in pins:
        for ps in pins[p]:
                s.add(metal_grid_3d[0][ps[1]][ps[0]] == p)
                
                
    if s.check()==sat:
        m = s.model()
        print('OK')
        
        for j in range(grid_y):
            l = []
            for i in range(grid_x):
                l.append(m.eval(metal_grid_3d[0][j][i]))
            print(l)
    else:
        print('UNSAT')
    
""" nt = {5: [[1, 3], [11, 3]], 4: [[2, 6], [6, 10]], 2: [[3, 3], [6, 0]], 15: [[3, 13], [11, 13]], 7: [[4, 8]], 8: [[5, 3], [7, 3]], 11: [[5, 13], [9, 3]], 1: [[6, 16], [9, 13]], 13: [[8, 8]], 10: [[10, 8]]}
route(['m1', 'm2', 'm3'], nt, 25, 20) """