'''
Created on 07-Jun-2015

@author: deepa
'''
import numpy
from bolt import Bolt
from nut import Nut

class NutBoltArray():
    def __init__(self,boltPlaceObj,nut,bolt,gap):
        self.origin = numpy.array([0.0, 0.0, 0])
        self.gaugeDir = numpy.array([1.0, 0.0, 0])
        self.pitchDir = numpy.array([0.0, 1.0, 0])
        self.boltDir =  numpy.array([0.0, 0.0, -1.0])
        
        self.initBoltPlaceParams(boltPlaceObj)
        
        self.bolt = bolt
        self.nut = nut
        self.gap = gap
        
        self.bolts = []
        self.nuts = []
        self.initialiseNutBolts()
        
        self.positions = []
        self.calculatePositions()
        
        self.models = []
                
    def initialiseNutBolts(self):
        b = self.bolt
        n = self.nut
        for i in range(self.row * self.col):
            self.bolts.append(Bolt(b.R,b.T, b.H, b.r))
            self.nuts.append(Nut(n.R, n.T,n.H, n.r1))
        
    def initBoltPlaceParams(self,boltPlaceObj):
        self.pitch = boltPlaceObj['Bolt']['pitch']
        self.gauge = boltPlaceObj['Bolt']['gauge']
        self.edge = boltPlaceObj['Bolt']['edge']
        self.end = boltPlaceObj['Bolt']['enddist']
        self.row = boltPlaceObj['Bolt']['numofrow']
        self.col = boltPlaceObj['Bolt']['numofcol']
        
    
    def calculatePositions(self):
        self.positions = []
        for rw in  range(1,(self.row +1)):
            for col in range(self.col):
                pos = self.origin +(self.edge + (col * self.gauge))* self.gaugeDir + rw * self.pitch * self.pitchDir
                self.positions.append(pos)
    
    def place(self, origin, gaugeDir, pitchDir, boltDir):
        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir
        
        self.calculatePositions()
        
        for index,pos in enumerate (self.positions):
            self.bolts[index].place(pos,gaugeDir,boltDir)
            self.nuts[index].place((pos + self.gap* boltDir),gaugeDir,pitchDir)
    
        
    def createModel(self):
        for bolt in self.bolts:
            self.models.append(bolt.createModel())
        for nut in self.nuts:
            self.models.append(nut.createModel())
        
    def getnutboltModels(self): 
        return self.models   
        
        