from z3 import *
import placement as pl
import toolutils as ut
import routing as rt


circuit = ut.read_netlist("netlist.txt")
pc, nc = pl.placement(circuit)
for pitem in pc:
    print(pitem)
    
for nitem in nc:
    print(nitem)
    
number_of_transistors = len(circuit)
print('-----------------------------------------------')

circuit = ut.read_netlist("new_net.txt")
pl.placement(circuit)
number_of_transistors = len(circuit)
print('-----------------------------------------------')

circuit = ut.read_netlist("a.txt")
pl.placement(circuit)
number_of_transistors = len(circuit)
print('-----------------------------------------------')


        
    

       
    

