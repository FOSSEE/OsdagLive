'''
Created on 07-Jun-2015

@author: deepa
'''
import numpy

class NutBoltArray():
    def __init__(self,boltPlaceObj,nut,bolt):
        
        self.pitch = boltPlaceObj['Bolt']['pitch']
        self.gauge = boltPlaceObj['Bolt']['gauge']
        self.edge = boltPlaceObj['Bolt']['edge']
        self.end = boltPlaceObj['Bolt']['enddist']
        self.row = boltPlaceObj['Bolt']['numofrow']
        self.col = boltPlaceObj['Bolt']['numofcol']
        self.gap = boltPlaceObj['beam_tw'] + boltPlaceObj['plate_thick']
        self.nut = nut
        self.bolt = bolt
        self.origin = numpy.array([0.0, 0.0, 0])
        self.uDir = numpy.array([1.0, 0.0, 0])
        self.vDir = numpy.array([0.0, 1.0, 0])
        self.positions = []
        for rw in  range(1,(len(self.row)+1)):
            for col in range(self.col):
                pos = self.pitch +(self.edge + (col * self.gauge))* self.uDir + (rw * self.pitch) * self.vDir
                self.positions.append(pos)
                
    
    def place(self, secOrigin, uDir, vDir):
        for pos in self.position:
            self.bolt.place(pos,uDir,vDir)
            self.nut.place(pos + self.gap,uDir,vDir)
        
    def createModel(self):
        
        pass
    def getnutboltModel(self):    
        pass 
        
        