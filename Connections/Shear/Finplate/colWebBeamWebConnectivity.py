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
class ColWebBeamWeb(object):
    
    def __init__(self,column,beam,Fweld,plate,boltRadius,nutRadius,boltPlaceObj):
        self.column = column
        self.beam = beam
        self.weldLeft = Fweld
        self.weldRight = copy.deepcopy(Fweld)
        self.plate = plate
        self.boltRadius = boltRadius
        self.nutRadius = nutRadius
        self.pitch = boltPlaceObj['Bolt']['pitch']
        self.gauge = boltPlaceObj['Bolt']['gauge']
        self.edge = boltPlaceObj['Bolt']['edge']
        self.end = boltPlaceObj['Bolt']['enddist']
        self.row = boltPlaceObj['Bolt']['numofrow']
        self.col = boltPlaceObj['Bolt']['numofcol']
        self.columnModel = None
        self.beamModel = None
        self.weldModelLeft = None
        self.weldModelRight = None
        self.plateModel = None
        self.bolts =[]
        self.nuts = []
        self.boltModels = []
        self.nutModels = []
        self.clearDist = 20.0 # This distance between edge of the column web/flange and beam cross section
        
    def create_3dmodel(self):

        # ISection COLUMN
        columnOrigin = numpy.array([0, 0, 0])
        column_uDir = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 0, 1.0])
        t = 8.9
        weldThick = 8
        
        self.column.place(columnOrigin, column_uDir, wDir1)
        
        # ISection BEAM
        uDir2 = numpy.array([0, 1.0, 0])
        wDir2 = numpy.array([1.0, 0, 0.0])
        d = t/2.0 + weldThick
        origin2 = columnOrigin + (self.column.t/2 * self.column.uDir) + (self.column.length/2 * self.column.wDir) + (self.clearDist * self.column.uDir) 
        #origin2 = numpy.array([0, 0, 500]) + (d+7.55) * wDir2 
        #origin2 = numpy.array([0, 0, 500]) + 20 * wDir2 
        #self.beam = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        self.beam.place(origin2, uDir2, wDir2)
        
        # # WELD
        #    
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
          
        # PLATE
        
        uDir4 = numpy.array([0, 1.0, 0])
        wDir4 = numpy.array([1.0, 0, 0.0])
        #origin4 = self.weld.secOrigin + self.weld.T * self.weld.wDir
        plateOrigin = (self.column.secOrigin + 
                   self.column.t/2.0 * self.column.uDir + 
                   self.column.length/2.0 * self.column.wDir +
                   self.beam.t/2.0 * (-self.beam.uDir)+
                   self.plate.T/2.0 * (-self.beam.uDir))
        #origin4 = self.column.secOrigin + self.weld.T * self.weld.wDir
        
        self.plate.place(plateOrigin, uDir4, wDir4)
        
#        # Weld
        uDir5 = numpy.array([1.0, 0.0, 0])
        wDir5 = numpy.array([0.0, 0.0, 1.0])
        filletWeld1Origin = (plateOrigin + self.plate.T/2.0 *self.weldLeft.vDir + self.weldLeft.L/2.0 * (-self.weldLeft.wDir) )
        self.weldLeft.place(filletWeld1Origin, uDir5, wDir5)
         
         
        uDir555 = numpy.array([0.0, -1.0, 0])
        wDir5 = numpy.array([0.0, 0.0, 1.0])
        filletWeld2Origin = (filletWeld1Origin + self.plate.T * (-self.weldLeft.vDir))
        self.weldRight.place(filletWeld2Origin,uDir555,wDir5)
 
        
 
        # BOLT BODY
        bolt_T = 6.0
        origin51 = (self.plate.secOrigin + (-
                    self.plate.T/2.0 - bolt_T) * self.plate.uDir +
                    self.plate.W/2.0 * self.plate.wDir)
        
        uDir5 = self.plate.wDir
        wDir5 = self.plate.uDir
        
        ## Bolt1
        bolt1 = Bolt(R = self.boltRadius,T = bolt_T, H = 30.0, r = 4.0 )
        bolt1.place(origin51, uDir5, wDir5)
        
        ## Bolt2
        bolt2 = Bolt(R = self.boltRadius, T = bolt_T, H = 30.0, r = 4.0 )
        origin52 = origin51 + 50 *self.plate.vDir
        bolt2.place(origin52, uDir5, wDir5)
        
        ## Bolt3
        bolt3 = Bolt(R = self.boltRadius,T = bolt_T, H = 30.0, r = 4.0 )
        origin53 = origin51 - 50*self.plate.vDir
        bolt3.place(origin53, uDir5, wDir5)
        self.bolts =[bolt1,bolt2,bolt3]
        
        #nutbody = Nut(R = 10.0,T = 10.0,  H = 6.1, innerR1 = 6.0, outerR2 = 8.3)
        # NUTBODY
        ## Nut1
        nut1 = Nut(R = self.nutRadius,T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        uDir = uDir5
        wDir = wDir5
        nut_Origin1 = origin51 + (bolt1.T/2 * self.plate.uDir)+(self.plate.T *self.plate.uDir)+ (self.beam.T/2 * self.plate.uDir)
        nut1.place(nut_Origin1, uDir, wDir)
        
        ## Nut2
        nut2 = Nut(R = self.nutRadius,T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut_Origin2 = origin52 + (bolt1.T/2 * self.plate.uDir)+(self.plate.T *self.plate.uDir)+ (self.beam.T/2 * self.plate.uDir)
        nut2.place(nut_Origin2, uDir, wDir)
        
        ## Nut3
        nut3 =Nut(R = self.nutRadius, T = 10.0,  H = 11, innerR1 = 4.0, outerR2 = 8.3)
        nut_Origin3 = origin53 + (bolt1.T/2 * self.plate.uDir)+(self.plate.T *self.plate.uDir)+ (self.beam.T/2 * self.plate.uDir)
        nut3.place(nut_Origin3, uDir5, wDir5)
        self.nuts = [nut1,nut2,nut3]
        
        
        # Call for createModel
        self.columnModel = self.column.createModel()
        self.beamModel = self.beam.createModel()
        self.plateModel = self.plate.createModel()
        self.weldModelLeft = self.weldLeft.createModel()
        self.weldModelRight = self.weldRight.createModel()
        
        for bolt in self.bolts: 
            self.boltModels.append(bolt.createModel())
        
        #color = Quantity_NOC_SADDLEBROWN,
        for nut in self.nuts:
            self.nutModels.append(nut.createModel())
        
        # memberList  = [iSectionModel1,iSectionModel2,weldModel1,weldModel2,
        #                plateModel] + boltModels + nutModels
        #  objshearfinplate = ShearFinPlate(iSectionModel1,iSectionModel2,)
        # 
        # print("memberList #####")
        # print(len(memberList))
        #return memberList
        
    def get_models(self):
        '''
        '''
        return [self.columnModel,self.beamModel,
                self.weldModelLeft,self.weldModelRight,
                self.plateModel]+self.boltModels + self.nutModels