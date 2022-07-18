from sqlalchemy import false
from z3 import *
import placement as pl
import toolutils as ut
import routing as rt
import drawing as dr

nets = ["netlist.txt", "new_net.txt", "a.txt"]
layers = ['M1', 'CA', 'RX', 'POLY']


for item in nets:
    circuit, pc, nc, ppos, npos = [], [], [], [], []
    circuit = ut.read_netlist(item)
    pc, nc, ppos, npos = pl.placement(circuit)
    
    
    for pitem in pc:
        print(pitem)        
    for nitem in nc:
        print(nitem)
        
    col, row = rt.estimateGrid(pc,nc)
        
    print(col, row)
    grRX, grCA, grPoly = rt.createGridTransistors(['RX', 'CA', 'POLY'], col, row, pc, nc, ppos, npos)
    
    dr.drawLayers([grRX, grPoly, grCA], col, row)
    
    print('-----------------------------------------------')






        
    

       
    

