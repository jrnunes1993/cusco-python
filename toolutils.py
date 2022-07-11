from data import Device

#-----------------------------------------------------------------------------------------------------------

def read_netlist(filename):     # Função que faz a leitura do arquivo e retorna uma lista de dispositivos e suas conexões/atributos
    f = open(filename, "r")     # Por enquanto, a leitura e o parser são simplificados 
    circlist = []
    
    for line in f:
        if line != '\n':
            circ = line.split()
            circlist.append(Device(circ[0],circ[1],circ[2],circ[3]))       # Cria lista do objeto transistor conforme a descrição da net 
    
    return circlist

#-----------------------------------------------------------------------------------------------------------