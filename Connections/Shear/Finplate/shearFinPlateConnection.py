'''
Created on 04-Jun-2015

@author: deepa
'''
class ShearFinPlate(object):
    
    def __init__(self,Beam,Column,Weld,Plate,Nutlist,Boltlist,outputObj):
        self.beam = Beam
        self.column = Column
        self.weld = Weld
        self.plate = Plate
        self.nutlist = Nutlist
        self.boltlist = Boltlist 
        self.pitch = outputObj['Bolt']['pitch']
        self.gauge = outputObj['Bolt']['gauge']
        self.edge = outputObj['Bolt']['edge']
        self.end = outputObj['Bolt']['enddist']
        self.row = outputObj['Bolt']['numofrow']
        self.col = outputObj['Bolt']['numofcol']
        
    
    
    