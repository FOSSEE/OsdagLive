'''
Created on 12-Dec-2014
NUT COMMENT
@author: deepa
'''

import math
import numpy
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut
from ModelUtils import getGpPt,getGpDir,makeEdgesFromPoints,makeWireFromEdges,makePrismFromFace,makeFaceFromWire
from OCC.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.gp import gp_Ax2

class Nut(object):
    
    '''
        a3  X-------------------+  a2
           X                   X|X
          X                   X | X
         X                   X  |  X
        X                   X   |   X
       X                   X    |    X
      X                   X     |     X
     X                   X 60   |      X
a4  X                   XXXXXXXXXXXXXXXXX  a1
     X                                 X
      X                               X
       XX                            X
        X                           X
         X                         X
          X                       X
           X                     X
            X-------------------X
                                   a6
            a5

    '''
    
    def __init__(self,R,T,H,innerR1):        
        self.R = R
        self.H = H
        self.T = T
        self.r1 = innerR1
        #self.r2 = outerR2
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
        prism =  makePrismFromFace(aFace, extrudeDir)
                
        cylOrigin = self.secOrigin
        innerCyl = BRepPrimAPI_MakeCylinder(gp_Ax2(getGpPt(cylOrigin), getGpDir(self.wDir)), self.r1, self.H).Shape()
        
        result_shape = BRepAlgoAPI_Cut(prism, innerCyl).Shape() 
        
        return result_shape
    
            