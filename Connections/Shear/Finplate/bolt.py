'''
Created on 29-Nov-2014

@author: deepa
'''
import numpy
from ModelUtils import *
import math
from OCC.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.BRepAlgo import BRepAlgo_BooleanOperations
from OCC.gp import gp_Pnt, gp_Dir, gp_Pln, gp_Ax2
from OCC.BRepAlgoAPI import  BRepAlgoAPI_Fuse


class Bolt(object):
    #
    def __init__(self,R,T,H,r):        
        self.R = R
        self.H = H
        self.T = T
        self.r = r
        self.secOrigin = numpy.array([0, 0, 0])
        self.uDir = numpy.array([1.0, 0, 0])
        self.wDir = numpy.array([0.0, 0, 1.0])
        self.computeParams()
    
    def place(self, secOrigin, uDir, wDir):
        self.secOrigin = secOrigin
        self.uDir = uDir
        self.wDir = wDir        
        self.computeParams()
        
    def getPoint(self,theta):
        theta = math.radians(theta)
        point = self.secOrigin + (self.R * math.cos(theta)) * self.uDir + (self.R * math.sin(theta)) * self.vDir 
        return point
    
    def computeParams(self):
        
        self.vDir = numpy.cross(self.wDir, self.uDir)
        self.a1 = self.getPoint(0)
        self.a2 = self.getPoint(60)
        self.a3 = self.getPoint(120)
        self.a4 = self.getPoint(180)
        self.a5 = self.getPoint(240)
        self.a6 = self.getPoint(300)
        self.points = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6]
       
    
        
    def createModel(self):
        
        edges = makeEdgesFromPoints(self.points)
        wire = makeWireFromEdges(edges)
        aFace = makeFaceFromWire(wire)
        extrudeDir = self.T * self.wDir # extrudeDir is a numpy array
        boltHead =  makePrismFromFace(aFace, extrudeDir)
        cylOrigin = self.secOrigin + self.T * self.wDir
      
        boltCylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(cylOrigin), getGpDir(self.wDir)), self.r, self.H).Shape()
        whole_Bolt = BRepAlgoAPI_Fuse(boltHead,boltCylinder).Shape()
        
        return whole_Bolt

        
    
            