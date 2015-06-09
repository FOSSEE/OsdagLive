'''
Created on 11-May-2015

@author: deepa
'''

import numpy
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from bolt import Bolt
from nut import Nut 

import copy
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.gp import gp_Pnt
from nutBoltPlacement import NutBoltArray
#from Connections.Shear.Finplate.nutBoltPlacement import NutBoltArray

class ColWebBeamWeb(object):
    
    def __init__(self,column,beam,Fweld,plate,nutBoltArray):
        self.column = column
        self.beam = beam
        self.weldLeft = Fweld
        self.weldRight = copy.deepcopy(Fweld)
        self.plate = plate
        self.nutBoltArray = nutBoltArray
        self.columnModel = None
        self.beamModel = None
        self.weldModelLeft = None
        self.weldModelRight = None
        self.plateModel = None
        self.clearDist = 20.0 # This distance between edge of the column web/flange and beam cross section
        
    def create_3dmodel(self):
        self.creatColumGeometry()
        self.createBeamGeometry()
        self.createPlateGeometry()
        self.createFilletWeldGeometry()
        self.createNutBoltArray()
        
        # Call for createModel
        self.columnModel = self.column.createModel()
        self.beamModel = self.beam.createModel()
        self.plateModel = self.plate.createModel()
        self.weldModelLeft = self.weldLeft.createModel()
        self.weldModelRight = self.weldRight.createModel()
        self.nutboltArrayModels = self.nutBoltArray.createModel()
        
    def creatColumGeometry(self):
        columnOrigin = numpy.array([0, 0, 0])
        column_uDir = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 0, 1.0])
        self.column.place(columnOrigin, column_uDir, wDir1)
        
    def createBeamGeometry(self):
        uDir = numpy.array([0, 1.0, 0])
        wDir = numpy.array([1.0, 0, 0.0])
        origin2 = self.column.secOrigin + (self.column.t/2 * self.column.uDir) + (self.column.length/2 * self.column.wDir) + (self.clearDist * self.column.uDir) 
        self.beam.place(origin2, uDir, wDir)
        
    def createButtWeld(self):
        pass
        # plateThickness = 10
        # uDir3 = numpy.array([0, 1.0, 0])
        # wDir3 = numpy.array([1.0, 0, 0.0])
        # origin3 = (self.column.secOrigin + 
        #            self.column.t/2.0 * self.column.uDir + 
        #            self.column.length/2.0 * self.column.wDir +
        #            self.beam.t/2.0 * (-self.beam.uDir)+
        #            self.weld.W/2.0 * (-self.beam.uDir))
        # #origin3 = numpy.array([0, 0, 500]) + t/2.0 *wDir3 + plateThickness/2.0 * (-self.beam.uDir)
        # self.weld.place(origin3, uDir3, wDir3)
        
    def createPlateGeometry(self):
        plateOrigin = (self.column.secOrigin + 
                   self.column.t/2.0 * self.column.uDir + 
                   self.column.length/2.0 * self.column.wDir +
                   self.beam.t/2.0 * (-self.beam.uDir)+
                   self.plate.T/2.0 * (-self.beam.uDir))
        uDir = numpy.array([0, 1.0, 0])
        wDir = numpy.array([1.0, 0, 0.0])
        self.plate.place(plateOrigin, uDir, wDir)
        
    def createFilletWeldGeometry(self):
        uDir = numpy.array([1.0, 0.0, 0])
        wDir = numpy.array([0.0, 0.0, 1.0])
        filletWeld1Origin = (self.plate.secOrigin + self.plate.T/2.0 *self.weldLeft.vDir + self.weldLeft.L/2.0 * (-self.weldLeft.wDir) )
        self.weldLeft.place(filletWeld1Origin, uDir, wDir)
         
        uDir1 = numpy.array([0.0, -1.0, 0])
        wDir1 = numpy.array([0.0, 0.0, 1.0])
        filletWeld2Origin = (filletWeld1Origin + self.plate.T * (-self.weldLeft.vDir))
        self.weldRight.place(filletWeld2Origin,uDir1,wDir1)
        
    def createNutBoltArray(self):
        nutboltArrayOrigin = self.plate.secOrigin 
        nutboltArrayOrigin -= self.plate.T/2.0 * self.plate.uDir  
        nutboltArrayOrigin += self.plate.L/2.0 * self.plate.vDir
        
        gaugeDir = self.plate.wDir
        pitchDir = -self.plate.vDir
        boltDir = self.plate.uDir
        self.nutBoltArray.place(nutboltArrayOrigin, gaugeDir, pitchDir, boltDir)
        
    def get_models(self):
        '''Returning 3D models
        '''
        return [self.columnModel,self.beamModel,
                self.weldModelLeft,self.weldModelRight,
                self.plateModel]+ self.nutBoltArray.getnutboltModels()
                
                
                
                
                