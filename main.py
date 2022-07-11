from z3 import *
import placement as pl
import toolutils as ut
import routing as rt

nets = ["netlist.txt", "new_net.txt", "a.txt"]
layers = ['M1', 'CA', 'RX', 'POLY']


for item in nets:
    circuit, nc, pc = [], [], []
    circuit = ut.read_netlist(item)
    pc, nc = pl.placement(circuit)
    
    for pitem in pc:
        print(pitem)        
    for nitem in nc:
        print(nitem)
        
    print(rt.estimateGrid(pc,nc))
    rt.createGridTransistors()
    print('-----------------------------------------------')





        
    

       
    

