from data import Device

#-----------------------------------------------------------------------------------------------------------

def read_netlist(filename):     # Função que faz a leitura do arquivo e retorna uma lista de dispositivos e suas conexões/atributos
    f = open(filename, "r")     # Por enquanto, a leitura e o parser são simplificados 
    circlist = []
    circDict = {'GND': 1,'VCC': 2}
    count = 3
    
    for line in f:
        if line != '\n':
            circ = line.upper().split()
            for id, word in enumerate(circ):
                if word != 'PMOS' and word != 'NMOS':
                    if word == 'VDD':
                        circ[id] = 'VCC'
                    elif word == 'VSS':
                        circ[id] = 'GND'
                    elif word not in circDict:
                        circDict[word] = count
                        count = count + 1
                
            if circ[4] != 'PMOS' and circ[4] != 'NMOS':
                print('ERRO')       #colocar try catch depois
                return
                
            circlist.append(Device(circDict[circ[0]],circDict[circ[1]],circDict[circ[2]],circDict[circ[3]],circ[4]))       # Cria lista do objeto transistor conforme a descrição da net 
            print(Device(circDict[circ[0]],circDict[circ[1]],circDict[circ[2]],circDict[circ[3]],circ[4]))
    print(circDict)
    
    return circlist, circDict

#-----------------------------------------------------------------------------------------------------------