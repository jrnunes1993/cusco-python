from data import Device

#-----------------------------------------------------------------------------------------------------------

def read_netlist(filename):     # Função que faz a leitura do arquivo e retorna uma lista de dispositivos e suas conexões/atributos
    f = open(filename, "r")     # Por enquanto, a leitura e o parser são simplificados 
    circlist = []
    circDict = {'GND': 1,'VDD': 2, 'VCC': 3, 'VSS': 4}
    count = 5
    
    for line in f:
        if line != '\n':
            circ = line.split()
            for word in circ:
                if word.upper() != 'PMOS' and word.upper() != 'NMOS':
                    if word.upper() not in circDict:
                        circDict[word.upper()] = count
                        count = count + 1
                
            if circ[4].upper() != 'PMOS' and circ[4].upper() != 'NMOS':
                print('ERRO')       #colocar try catch depois
                return
                
            circlist.append(Device(circDict[circ[0].upper()],circDict[circ[1].upper()],circDict[circ[2].upper()],circDict[circ[3].upper()],circ[4].upper()))       # Cria lista do objeto transistor conforme a descrição da net 
            print(Device(circDict[circ[0].upper()],circDict[circ[1].upper()],circDict[circ[2].upper()],circDict[circ[3].upper()],circ[4].upper()))
    print(circDict)
    
    return circlist

#-----------------------------------------------------------------------------------------------------------