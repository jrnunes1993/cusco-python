from multiprocessing import connection
from z3 import *
from math import floor
import heapq
import numpy as np

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
    def __init__(self, net_number: int, connections: list, pinslist: list):
        self.net_number = net_number
        self.connections = connections
        self.pinslist = pinslist
    
    def __str__(self):
        txt = "Net {}\n".format(self.net_number)
        for con in self.connections:
            txt += f"\t {con}\n"

        return txt
    
    def getNumOfConnections(self):
        return len(self.connections)
            
    def getPins(self):
        listOfPins = []
        
        for c in self.connections:
            if c.pin1 not in listOfPins:
                listOfPins.append(c.pin1)
            if c.pin2 not in listOfPins:
                listOfPins.append(c.pin2)
        
        return listOfPins
            
            

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
    uniquepins = []
    con_count = 0

    for n in pinlist:
        if len(pinlist[n])>1:    
            for idx, ps in enumerate(pinlist[n]):
                for i in range(idx+1, len(pinlist[n])):
                    aux_cons.append(Connection(con_count, Pin(ps[0], ps[1], con_count, n), Pin(pinlist[n][i][0], pinlist[n][i][1], con_count, n)))
                    con_count = con_count + 1
                uniquepins.append(Pin(ps[0], ps[1], con_count, n))

            con_count = 0
            netlist.append(Net(n, aux_cons, uniquepins))
            aux_cons = []
            uniquepins = []
        
    for n in netlist:
        print(n)
    
    print(pinlist)
    return netlist, pinlist

def createEmptyGrid(n_lines, n_columns):
    grid = np.zeros((n_lines, n_columns)).astype(int)
    return grid


def fillPinsInGrid(grid, pins):
    for key, values in pins.items():
        for pin in values:
           grid[pin[0], pin[1]] = key
    return grid



def route(metalLayers, nets, pins, grid_x, grid_y):
    grid = createEmptyGrid(grid_x,grid_y)
    met1Grid = Grid('M1', grid_x, grid_y)
    grid = fillPinsInGrid(grid, pins)
    print(grid)
    for key, values in pins.items():
        ##Não deve procurar caminhos para pontos isolados
        if(len(values) <= 1):
            continue

        start = tuple(values[0])
        goal = tuple(values[1])


        applyAStarRouting(grid, met1Grid, key, start, goal)
        if(len(values) == 3):
            start = tuple(values[1])
            goal = tuple(values[2])
            applyAStarRouting(grid, met1Grid, key, start, goal)

    print("\n\n##################### GRID FINAL ###############################\n")
    print(grid)
    return met1Grid

def applyAStarRouting(grid, met1Grid, key, start, goal):
    came_from, cost_so_far = astar(start, goal, grid, heuristic)
    path = [goal]
    node = goal
    while node != start:
        node = came_from[node]
        path.append(node)
    path.reverse()

    for point in path:
        grid[point] = key
        met1Grid.occupy_one_point(point[0], point[1],key)
    

def astar(start, goal, graph, heuristic):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current_node = heapq.heappop(frontier)

        if current_node == goal:
            break

        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            x, y = current_node[0] + dx, current_node[1] + dy
            if 0 <= x < graph.shape[0] and 0 <= y < graph.shape[1]:
                neighbor = (x, y)
                cost = graph[x][y]
                new_cost = cost_so_far[current_node] + cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(goal, neighbor)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current_node

    return came_from, cost_so_far

def heuristic(a, b):
    # Estimativa heurística de distância entre os nós a e b
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def routea(metalLayers, nets, pins, grid_x, grid_y):


    s = Solver()
    
    num_metal = len(metalLayers)
    metal_grid_3d = [[[Int("s_%i_%i_%i" % (j,i,k)) for j in range (grid_x)] for i in range(grid_y)] for k in range(num_metal)]
    print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    print(grid_x, grid_y, pins)
    print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    
    nets_set = set([n.net_number for n in nets])
    net_number = []
    
    for idx, n in enumerate(nets_set):
        net_number.append(Int("net_%i" % (n)))
        s.add(net_number[idx] == n)

    for p in pins:
        if p not in nets_set:
            print(p)
            s.add(And(metal_grid_3d[0][pins[p][0][1]+1][pins[p][0][0]+1] == 0,
                    metal_grid_3d[0][pins[p][0][1]-1][pins[p][0][0]+1] == 0,
                    metal_grid_3d[0][pins[p][0][1]+1][pins[p][0][0]-1] == 0,
                    metal_grid_3d[0][pins[p][0][1]-1][pins[p][0][0]-1] == 0,
                    metal_grid_3d[0][pins[p][0][1]][pins[p][0][0]] == 0,
                    metal_grid_3d[0][pins[p][0][1]+1][pins[p][0][0]] == 0,
                    metal_grid_3d[0][pins[p][0][1]-1][pins[p][0][0]] == 0,
                    metal_grid_3d[0][pins[p][0][1]][pins[p][0][0]+1] == 0,
                    metal_grid_3d[0][pins[p][0][1]][pins[p][0][0]-1] == 0
    
                )
            )


                
    if s.check()==sat:
        m = s.model()
        print('OK')
        
        met1Grid = Grid('M1', grid_x, grid_y)

        for j in range(grid_y):
            l = []
            for i in range(grid_x):
                l.append(int(str(m.eval(metal_grid_3d[0][j][i])))) if type(m.eval(metal_grid_3d[0][j][i])) is z3.z3.IntNumRef else l.append(0)
                #met1Grid.occupy_one_point(i,j,int(str(m.eval(metal_grid_3d[0][j][i]))) if type(m.eval(metal_grid_3d[0][j][i])) is z3.z3.IntNumRef else 0)
                
            print(l)
            
        first_route = False
        print("#####################################################")
        print(met1Grid)
        print("#####################################################")
 
        return met1Grid
    
    print('###########################################')
    