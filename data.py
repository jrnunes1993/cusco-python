#-----------------------------------------------------------------------------------------------------------   

class Device:   # Classe que define o transistor
    def __init__(self, name = None, source = None, gate = None, drain = None, rtype = None, pos = None, flip = None):
        
        self.name = name
        self.source = source
        self.gate = gate
        self.drain = drain
        self.rtype = rtype
        self.position = pos
        self.flipped = flip
        
    def __str__(self):
        return "pos:" + str(self.position) + " source:" + str(self.source) + " gate:" + str(self.gate) + " drain:" + str(self.drain) + " type:" + str(self.rtype) + " flipped:" + str(self.flipped)
    def setDrain(self, drain):
        self.drain = drain
    
    def setGate(self, gate):
        self.gate = gate

    def setSource(self, source):
        self.source = source
        
    def setType(self, rtype):
        self.rtype = rtype

#----------------------------------------------------------------------------------------------------------- 