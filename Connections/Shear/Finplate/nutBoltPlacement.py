'''
Created on 07-Jun-2015

@author: deepa
'''
import numpy
from bolt import Bolt
from nut import Nut
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from ModelUtils import getGpPt

class NutBoltArray():
    def __init__(self,boltPlaceObj,nut,bolt,gap):
        self.origin = None
        self.gaugeDir = None
        self.pitchDir = None
        self.boltDir =  None
        
        self.initBoltPlaceParams(boltPlaceObj)
        
        self.bolt = bolt
        self.nut = nut
        self.gap = gap
        
        self.bolts = []
        self.nuts = []
        self.initialiseNutBolts()
        
        self.positions = []
        #self.calculatePositions()
        
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
        #self.gauge = 30
        self.edge = boltPlaceObj['Bolt']['edge']
        self.end = boltPlaceObj['Bolt']['enddist']
        self.row = boltPlaceObj['Bolt']['numofrow']
        self.col = boltPlaceObj['Bolt']['numofcol']
        #self.row = 3
        #self.col = 2
         
    
    def calculatePositions(self):
        self.positions = []
        for rw in  range(self.row):
            for col in range(self.col):
                pos = self.origin 
                pos = pos + self.edge * self.gaugeDir
                pos = pos + col * self.gauge * self.gaugeDir 
                pos = pos + self.end * self.pitchDir 
                pos = pos + rw * self.pitch * self.pitchDir
                
                self.positions.append(pos)
    
    def place(self, origin, gaugeDir, pitchDir, boltDir):
        self.origin = origin
        self.gaugeDir = gaugeDir
        self.pitchDir = pitchDir
        self.boltDir = boltDir
        
        self.calculatePositions()
        
        for index, pos in enumerate (self.positions):
            self.bolts[index].place(pos, gaugeDir, boltDir)
            self.nuts[index].place((pos + self.gap * boltDir), gaugeDir, -boltDir)
    
        
    def createModel(self):
        for bolt in self.bolts:
            self.models.append(bolt.createModel())        
        
        for nut in self.nuts:
            self.models.append(nut.createModel())
            
        dbg = self.dbgSphere(self.origin)
        self.models.append(dbg)
        
    def dbgSphere(self, pt):
        return BRepPrimAPI_MakeSphere(getGpPt(pt), 2).Shape()
        
    def getnutboltModels(self): 
        return self.models   
        
        