'''
Created on 11-May-2015

@author: deepa
'''

import numpy
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from bolt import Bolt
from nut import Nut 

import copy
class ColWebBeamWeb(object):
    
    def __init__(self,column,beam,Fweld,plate,boltRadius,nutRadius):
        self.column = column
        self.beam = beam
        self.weld = Fweld
        self.weld2 = copy.deepcopy(Fweld)
        self.plate = plate
        self.boltRadius = boltRadius
        self.nutRadius = nutRadius
        
    
    def create_3dmodel(self):

        # ISection COLUMN
        origin1 = numpy.array([0, 0, 0])
        uDir1 = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 0, 1.0])
        t = 8.9
        weldThick = 8
        
        self.column.place(origin1, uDir1, wDir1)
        
        # ISection BEAM
        uDir2 = numpy.array([0, 1.0, 0])
        wDir2 = numpy.array([1.0, 0, 0.0])
        d = t/2.0 + weldThick
        origin2 = numpy.array([0, 0, 500]) + (d+7.55) * wDir2 
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
        filletWeld1Origin = (plateOrigin + self.plate.T/2.0 *self.weld.vDir + self.weld.L/2.0 * (-self.weld.wDir) )
        self.weld.place(filletWeld1Origin, uDir5, wDir5)
         
         
        uDir555 = numpy.array([0.0, -1.0, 0])
        wDir5 = numpy.array([0.0, 0.0, 1.0])
        filletWeld2Origin = (filletWeld1Origin + self.plate.T * (-self.weld.vDir))
        self.weld2.place(filletWeld2Origin,uDir555,wDir5)

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
        bolt_list =[bolt1,bolt2,bolt3]
        
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
        nut_list = [nut1,nut2,nut3]
        
        # Call for createModel
        iSectionModel1 = self.column.createModel()
        iSectionModel2 = self.beam.createModel()
        
        plateModel = self.plate.createModel()
        weldModel1 = self.weld.createModel()
        weldModel2 = self.weld2.createModel()
        
        boltModels = []
        for bolt in bolt_list: 
            boltModels.append(bolt.createModel())
        
        #color = Quantity_NOC_SADDLEBROWN,
        nutModels = []
        for nut in nut_list:
            nutModels.append(nut.createModel())
        
        memberList  = [iSectionModel1,iSectionModel2,weldModel1,weldModel2,plateModel,boltModels,nutModels]
        
        return memberList